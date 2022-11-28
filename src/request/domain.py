import datetime
from datetime import date

from django.conf import settings

from request.constants import STATUS_APPROVED, STATUS_PENDING
from request.models import Request, User


def remaining_days(user: User, year: int):
    """
    Get the remaining free days off from specific user and year
    """
    requests = Request.objects.filter(
        author=user, vacation_end_date__gt=date(year, 1, 1), status=STATUS_APPROVED
    )  # get all the requests approved that have at least one day from requested year
    days = 0
    for request in requests:
        # clean the date range, so we are only interested in the days within the selected year,
        # so start and end date are trimmed to fit within the year, the days outside this we don't care
        if request.vacation_end_date > date(year, 12, 31):
            end_date = date(year, 12, 31) + datetime.timedelta(days=1)
        else:
            end_date = request.vacation_end_date
        start_date = max(date(year, 1, 1), request.vacation_start_date)
        delta = end_date - start_date
        days += delta.days
    # if for some reason the number is negative just return 0
    return max(settings.DAYS_OFF_PER_YEAR - days, 0)


def find_overlaps(
    start_date: date, end_date: date, exclude_id: int = None, author_id: int = None
):
    queryset = Request.objects.filter(
        vacation_end_date__gt=start_date,
        vacation_start_date__lt=end_date,
        status__in=[STATUS_APPROVED, STATUS_PENDING],
    )
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    if author_id:
        queryset = queryset.filter(author=author_id)
    return queryset
