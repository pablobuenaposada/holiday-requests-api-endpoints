from datetime import date

import pytest
from model_bakery import baker
from rest_framework import status as status_constants
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from api.remaining.serializers import RemainingOutputSerializer
from request.domain import remaining_days
from request.models import User


@pytest.mark.django_db
class TestRequestViewList:
    endpoint = "/api/remaining/"

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.user = baker.make(User)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_valid(self):
        response = self.client.get(self.endpoint)

        assert response.status_code == status_constants.HTTP_200_OK
        assert (
            response.data
            == RemainingOutputSerializer(
                {"days": remaining_days(self.user, date.today().year)}
            ).data
        )

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
