from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms.models import model_to_dict
from django_extensions.db.models import TimeStampedModel

from api.requests.validators import dates_validator
from request.constants import (MANAGER_TYPE, STATUS, STATUS_PENDING,
                               USER_TYPES, WORKER_TYPE)
from request.exceptions import NotEnoughFreeDays, Overlap


class User(AbstractUser):
    # TODO: this model should placed somewhere else
    type = models.CharField(choices=USER_TYPES, max_length=7, default=WORKER_TYPE)

    REQUIRED_FIELDS = ["type"]


class Request(TimeStampedModel):
    status = models.CharField(choices=STATUS, max_length=8, default=STATUS_PENDING)
    vacation_start_date = models.DateField()
    vacation_end_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="manager",
        limit_choices_to={"type": MANAGER_TYPE[0]},
        null=True,
        blank=True,
    )

    @property
    def overlaps(self):
        from request.domain import find_overlaps

        return find_overlaps(self.vacation_start_date, self.vacation_end_date, self.id)

    def save(self, **kwargs):
        from request.domain import find_overlaps, remaining_days

        dates_validator(model_to_dict(self))

        if not self.pk:  # if is new
            if find_overlaps(
                self.vacation_start_date,
                self.vacation_end_date,
                author_id=self.author.id,
            ).exists():
                raise Overlap

        for year in range(
            self.vacation_start_date.year, self.vacation_end_date.year + 1
        ):
            if remaining_days(self.author, year) < 1:
                raise NotEnoughFreeDays

        super().save(**kwargs)
