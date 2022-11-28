from datetime import date

import pytest
from django.utils.timezone import get_current_timezone
from model_bakery import baker

from api.requests.serializers import (RequestInputSerializer,
                                      RequestOutputSerializer,
                                      RequestUpdateInputSerializer)
from request.constants import STATUS_APPROVED, STATUS_PENDING, STATUS_REJECTED
from request.models import Request


@pytest.mark.django_db
class TestRequestOutputSerializer:
    def test_valid(self):
        request = baker.make(
            Request,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )

        assert RequestOutputSerializer(request).data == {
            "id": request.id,
            "author": request.author.id,
            "status": request.status,
            "resolved_by": request.resolved_by,
            "request_created_at": request.created.astimezone(
                tz=get_current_timezone()
            ).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "vacation_start_date": request.vacation_start_date.strftime("%Y-%m-%d"),
            "vacation_end_date": request.vacation_end_date.strftime("%Y-%m-%d"),
        }


class TestRequestInputSerializer:
    def test_valid(self):
        assert (
            RequestInputSerializer(
                data={
                    "vacation_start_date": date(2022, 1, 1),
                    "vacation_end_date": date(2022, 1, 2),
                }
            ).is_valid()
            is True
        )


class TestRequestUpdateInputSerializer:
    @pytest.mark.parametrize(
        "status, expected",
        ((STATUS_APPROVED, True), (STATUS_REJECTED, True), (STATUS_PENDING, False)),
    )
    def test_valid(self, status, expected):
        assert (
            RequestUpdateInputSerializer(data={"status": status}).is_valid() is expected
        )
