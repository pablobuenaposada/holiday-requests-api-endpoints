from datetime import date

import pytest
from model_bakery import baker

from api.requests.overlaps.serializers import OverlapOutputSerializer
from api.requests.serializers import RequestOutputSerializer
from request.models import Request


@pytest.mark.django_db
class TestOverlapOutputSerializer:
    def test_valid(self):
        requests = baker.make(
            Request,
            _quantity=2,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )
        # both requests are pending status and overlap between them so if we ask the overlap of any of them
        # we are going to get the other one as an overlap

        assert OverlapOutputSerializer(
            Request.objects.filter(id=requests[0].id), many=True
        ).data == [
            {
                "id": requests[0].id,
                "vacation_start_date": requests[0].vacation_start_date.strftime(
                    "%Y-%m-%d"
                ),
                "vacation_end_date": requests[0].vacation_end_date.strftime("%Y-%m-%d"),
                "overlaps": [RequestOutputSerializer(requests[1]).data],
            }
        ]
