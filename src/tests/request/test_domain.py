import datetime
from datetime import date

import pytest
from django.conf import settings
from model_bakery import baker

from request.constants import STATUS_APPROVED, STATUS_PENDING, STATUS_REJECTED
from request.domain import find_overlaps, remaining_days
from request.models import Request, User


@pytest.mark.django_db
class TestRemainingDays:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.user = baker.make(User)

    @pytest.mark.parametrize(
        "requests, year, expected",
        (
            (
                [],
                2022,
                settings.DAYS_OFF_PER_YEAR,
            ),  # no requests so all the days available
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 1),
                        "vacation_end_date": date(2022, 1, 2),
                        "status": STATUS_APPROVED,
                    },
                ],
                2022,
                settings.DAYS_OFF_PER_YEAR - 1,
            ),  # one request of one day
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 1),
                        "vacation_end_date": date(2022, 1, 2),
                        "status": STATUS_APPROVED,
                    },
                    {
                        "vacation_start_date": date(2022, 1, 2),
                        "vacation_end_date": date(2022, 1, 4),
                        "status": STATUS_APPROVED,
                    },
                ],
                2022,
                settings.DAYS_OFF_PER_YEAR - 3,
            ),  # two request of one and two days each
            (
                [
                    {
                        "vacation_start_date": date(2021, 1, 1),
                        "vacation_end_date": date(2021, 1, 2),
                        "status": STATUS_APPROVED,
                    },
                ],
                2022,
                settings.DAYS_OFF_PER_YEAR,
            ),  # one request of one day but from last year
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 1),
                        "vacation_end_date": date(2022, 1, 2),
                        "status": STATUS_REJECTED,
                    },
                ],
                2022,
                settings.DAYS_OFF_PER_YEAR,
            ),  # one request of one day but not approved
            (
                [
                    {
                        "vacation_start_date": date(2022, 12, 31),
                        "vacation_end_date": date(2023, 1, 2),
                        "status": STATUS_APPROVED,
                    },
                ],
                2022,
                settings.DAYS_OFF_PER_YEAR - 1,
            ),  # a request with one day from current year and another one from following year
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 1),
                        "vacation_end_date": date(2022, 1, 1)
                        + datetime.timedelta(days=settings.DAYS_OFF_PER_YEAR + 1),
                        "status": STATUS_APPROVED,
                    },
                ],
                2022,
                0,
            ),  # a request with more than allowed days off
            (
                [
                    {
                        "vacation_start_date": date(2021, 12, 30),
                        "vacation_end_date": date(2022, 1, 2),
                        "status": STATUS_APPROVED,
                    },
                ],
                2022,
                settings.DAYS_OFF_PER_YEAR - 1,
            ),  # a request starting in a previous year than remaining year requested
        ),
    )
    def test_remaining_days(self, requests, year, expected):
        for request in requests:
            baker.make(
                Request,
                author=self.user,
                vacation_start_date=request["vacation_start_date"],
                vacation_end_date=request["vacation_end_date"],
                status=request["status"],
            )

        assert remaining_days(self.user, year) == expected


@pytest.mark.django_db
class TestFindOverlaps:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.user = baker.make(User)

    @pytest.mark.parametrize(
        "requests, start_date, end_date, found",
        (
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 1),
                        "vacation_end_date": date(2022, 1, 2),
                    },
                ],
                date(2022, 1, 3),
                date(2022, 1, 4),
                False,
            ),  # found one request after
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 3),
                        "vacation_end_date": date(2022, 1, 4),
                    },
                ],
                date(2022, 1, 1),
                date(2022, 1, 2),
                False,
            ),  # found one request before
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 1),
                        "vacation_end_date": date(2022, 1, 4),
                    },
                ],
                date(2022, 1, 2),
                date(2022, 1, 3),
                True,
            ),  # found one request that wraps the requested
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 2),
                        "vacation_end_date": date(2022, 1, 3),
                    },
                ],
                date(2022, 1, 1),
                date(2022, 1, 4),
                True,
            ),  # found one request inside the requested
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 1),
                        "vacation_end_date": date(2022, 1, 2),
                    },
                ],
                date(2022, 1, 1),
                date(2022, 1, 2),
                True,
            ),  # exactly the same request
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 1),
                        "vacation_end_date": date(2022, 1, 3),
                    },
                ],
                date(2022, 1, 2),
                date(2022, 1, 4),
                True,
            ),  # found one half overlapped by the start
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 2),
                        "vacation_end_date": date(2022, 1, 4),
                    },
                ],
                date(2022, 1, 1),
                date(2022, 1, 3),
                True,
            ),  # found one half overlapped by the end
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 1),
                        "vacation_end_date": date(2022, 1, 2),
                    },
                ],
                date(2022, 1, 2),
                date(2022, 1, 3),
                False,
            ),  # found one request just after
            (
                [
                    {
                        "vacation_start_date": date(2022, 1, 2),
                        "vacation_end_date": date(2022, 1, 3),
                    },
                ],
                date(2022, 1, 1),
                date(2022, 1, 2),
                False,
            ),  # found one request just before
        ),
    )
    def test_find_overlaps(self, requests, start_date, end_date, found):
        for request in requests:
            baker.make(
                Request,
                author=self.user,
                vacation_start_date=request["vacation_start_date"],
                vacation_end_date=request["vacation_end_date"],
                status=STATUS_APPROVED,
            )

        assert find_overlaps(start_date, end_date).exists() is found

    @pytest.mark.parametrize(
        "status, found",
        (
            (STATUS_APPROVED, True),
            (STATUS_PENDING, True),
            (STATUS_REJECTED, False),
        ),
    )
    def test_status_find_overlaps(self, status, found):
        """Status rejected is not counted for finding overlaps"""

        baker.make(
            Request,
            author=self.user,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
            status=status,
        )

        assert find_overlaps(date(2022, 1, 1), date(2022, 1, 2)).exists() is found
