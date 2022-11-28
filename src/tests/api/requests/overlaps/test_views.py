from datetime import date

import pytest
from model_bakery import baker
from rest_framework import status as status_constants
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from api.requests.overlaps.serializers import OverlapOutputSerializer
from request.constants import MANAGER_TYPE, WORKER_TYPE
from request.models import Request, User


@pytest.mark.django_db
class TestRequestViewList:
    endpoint = "/api/requests/overlaps/"

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.user = baker.make(User, type=MANAGER_TYPE)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_valid(self):
        request = baker.make(
            Request,
            author=self.user,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )

        response = self.client.get(self.endpoint)

        assert response.status_code == status_constants.HTTP_200_OK
        assert response.data == {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [OverlapOutputSerializer(request).data],
        }

    def test_not_logged(self):
        self.client.force_authenticate(None)
        response = self.client.get(self.endpoint)

        assert response.status_code == status_constants.HTTP_401_UNAUTHORIZED
        assert response.data == {
            "detail": ErrorDetail(
                string="Authentication credentials were not provided.",
                code="not_authenticated",
            )
        }

    def test_with_worker(self):
        """A worker should not be able to access this view"""

        self.client = APIClient()
        self.client.force_authenticate(baker.make(User, type=WORKER_TYPE))

        response = self.client.get(self.endpoint)

        assert response.status_code == status_constants.HTTP_403_FORBIDDEN
        assert response.data == {
            "detail": ErrorDetail(
                string="You do not have permission to perform this action.",
                code="permission_denied",
            )
        }
