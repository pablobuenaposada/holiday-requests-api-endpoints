import datetime
from datetime import date
from unittest.mock import ANY

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from model_bakery import baker

from request.constants import STATUS_APPROVED, STATUS_PENDING
from request.exceptions import NotEnoughFreeDays, Overlap
from request.models import Request, User


@pytest.mark.django_db
class TestRequest:
    def test_valid(self):
        request = Request.objects.create(
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
            author=baker.make(User),
            resolved_by=baker.make(User),
        )
        expected = {
            "id": ANY,
            "author": request.author,
            "status": STATUS_PENDING,
            "created": request.created,
            "resolved_by": request.resolved_by,
            "vacation_start_date": request.vacation_start_date,
            "vacation_end_date": request.vacation_end_date,
            "modified": ANY,
        }

        for field in {field.name for field in Request._meta.get_fields()}:
            assert getattr(request, field) == expected[field]

    def test_overlapped_requests(self):
        """For the same user cannot be holidays overlapped"""
        user = baker.make(User)
        Request.objects.create(
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
            author=user,
        )
        with pytest.raises(Overlap):
            Request.objects.create(
                vacation_start_date=date(2022, 1, 1),
                vacation_end_date=date(2022, 1, 2),
                author=user,
            )

    def test_wrong_dates(self):
        """Start date cannot be greater than end date"""

        with pytest.raises(ValidationError):
            Request.objects.create(
                vacation_start_date=date(2022, 1, 2),
                vacation_end_date=date(2022, 1, 1),
                author=baker.make(User),
            )

    def test_not_enough_free_days(self):
        """Start date cannot be greater than end date"""
        user = baker.make(User)
        baker.make(
            Request,
            author=user,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 1)
            + datetime.timedelta(days=settings.DAYS_OFF_PER_YEAR),
            status=STATUS_APPROVED,
        )

        with pytest.raises(NotEnoughFreeDays):
            Request.objects.create(
                vacation_start_date=date(2022, 2, 1),
                vacation_end_date=date(2022, 2, 2),
                author=user,
            )
