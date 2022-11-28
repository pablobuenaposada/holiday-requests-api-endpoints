import datetime
from datetime import date
from unittest.mock import ANY

import pytest
from django.conf import settings
from model_bakery import baker
from rest_framework import status as status_constants
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from api.requests.serializers import RequestOutputSerializer
from request.constants import (MANAGER_TYPE, STATUS, STATUS_APPROVED,
                               STATUS_PENDING, WORKER_TYPE)
from request.models import Request, User


@pytest.mark.django_db
class TestRequestViewGet:
    endpoint = "/api/requests/"

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.user = baker.make(User)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_valid_as_worker(self):
        request_1 = baker.make(
            Request,
            author=self.user,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )
        request_2 = baker.make(
            Request,
            author=self.user,
            vacation_start_date=date(2022, 1, 2),
            vacation_end_date=date(2022, 1, 3),
        )

        response = self.client.get(self.endpoint)

        assert response.status_code == status_constants.HTTP_200_OK
        assert response.data == {
            "count": len({request_1, request_2}),
            "next": None,
            "previous": None,
            "results": [
                RequestOutputSerializer(request).data
                for request in {request_1, request_2}
            ],
        }

    def test_valid_as_manager(self):
        request_worker_1 = baker.make(
            Request,
            author=self.user,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )
        user2 = baker.make(User)
        request_worker_2 = baker.make(
            Request,
            author=user2,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )
        self.client.force_authenticate(baker.make(User, type=MANAGER_TYPE))

        response = self.client.get(self.endpoint)

        assert response.status_code == status_constants.HTTP_200_OK
        assert response.data == {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                RequestOutputSerializer(request).data
                for request in {request_worker_1, request_worker_2}
            ],
        }

    def test_no_requests(self):
        request = baker.make(
            Request,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )  # a request but not related to the logged user

        assert request.author != self.user
        assert Request.objects.exists() is True

        response = self.client.get(self.endpoint)

        assert response.status_code == status_constants.HTTP_200_OK
        assert response.data == {
            "count": 0,
            "next": None,
            "previous": None,
            "results": [],
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

    def test_filter_by_status(self):
        for idx, status in enumerate(STATUS):
            baker.make(
                Request,
                author=self.user,
                status=status[0],
                vacation_start_date=date(2022, 1, 1 + idx),
                vacation_end_date=date(2022, 1, 2 + idx),
            )

            response = self.client.get(self.endpoint, data={"status": status[0]})

            assert response.status_code == status_constants.HTTP_200_OK
            assert response.data["count"] == 1
            assert response.data["results"][0]["status"] == status[0]

    def test_filter_by_author(self):
        baker.make(
            Request,
            author=self.user,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )
        user2 = baker.make(User)
        baker.make(
            Request,
            author=user2,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )
        self.client.force_authenticate(baker.make(User, type=MANAGER_TYPE))

        for user in {self.user, user2}:
            response = self.client.get(self.endpoint, data={"author": user.id})

            assert response.status_code == status_constants.HTTP_200_OK
            assert response.data["count"] == 1
            assert response.data["results"][0]["author"] == user.id


@pytest.mark.django_db
class TestRequestViewPost:
    endpoint = "/api/requests/"

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.user = baker.make(User)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_valid(self):
        response = self.client.post(
            self.endpoint,
            data={
                "vacation_start_date": date(2022, 1, 1),
                "vacation_end_date": date(2022, 1, 2),
            },
        )

        assert response.status_code == status_constants.HTTP_201_CREATED
        assert response.data == {
            "id": ANY,
            "request_created_at": ANY,
            "resolved_by": None,
            "status": STATUS_PENDING,
            "author": self.user.id,
            "vacation_start_date": date(2022, 1, 1).strftime("%Y-%m-%d"),
            "vacation_end_date": date(2022, 1, 2).strftime("%Y-%m-%d"),
        }
        assert Request.objects.count() == 1

    def test_not_free_days_off(self):
        baker.make(
            Request,
            author=self.user,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 1)
            + datetime.timedelta(days=settings.DAYS_OFF_PER_YEAR),
            status=STATUS_APPROVED,
        )

        response = self.client.post(
            self.endpoint,
            data={
                "vacation_start_date": date(2022, 2, 1),
                "vacation_end_date": date(2022, 2, 2),
            },
        )

        assert response.status_code == status_constants.HTTP_409_CONFLICT
        assert response.data == {
            "detail": ErrorDetail(string="Not enough free days", code="free_days")
        }
        assert Request.objects.count() == 1

    def test_overlap(self):
        baker.make(
            Request,
            author=self.user,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )

        response = self.client.post(
            self.endpoint,
            data={
                "vacation_start_date": date(2022, 1, 1),
                "vacation_end_date": date(2022, 1, 2),
            },
        )

        assert response.status_code == status_constants.HTTP_409_CONFLICT
        assert response.data == {
            "detail": ErrorDetail(
                string="This request overlaps with an existing one", code="overlap"
            )
        }
        assert Request.objects.count() == 1

    def test_validation_error(self):
        response = self.client.post(
            self.endpoint,
            data={
                "vacation_start_date": date(2022, 1, 1).strftime("%Y-%m-%d"),
                "vacation_end_date": date(2022, 1, 1).strftime("%Y-%m-%d"),
            },
        )

        assert response.status_code == status_constants.HTTP_400_BAD_REQUEST
        assert response.data == {
            "non_field_errors": [
                ErrorDetail(
                    string="vacation_start_date should be earlier than vacation_end_date",
                    code="invalid",
                )
            ]
        }
        assert Request.objects.count() == 0

    def test_not_logged(self):
        self.client.force_authenticate(None)
        response = self.client.post(self.endpoint)

        assert response.status_code == status_constants.HTTP_401_UNAUTHORIZED
        assert response.data == {
            "detail": ErrorDetail(
                string="Authentication credentials were not provided.",
                code="not_authenticated",
            )
        }


@pytest.mark.django_db
class TestRequestViewPatch:
    endpoint = "/api/requests/"

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.user = baker.make(User, type=MANAGER_TYPE)
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.request = baker.make(
            Request,
            author=self.user,
            vacation_start_date=date(2022, 1, 1),
            vacation_end_date=date(2022, 1, 2),
        )

    def test_valid(self):
        assert self.request.resolved_by is None
        assert self.request.status == STATUS_PENDING

        response = self.client.patch(
            f"{self.endpoint}{self.request.id}/", data={"status": STATUS_APPROVED}
        )

        assert response.status_code == status_constants.HTTP_200_OK
        assert response.data == {
            "id": self.request.id,
            "request_created_at": ANY,
            "resolved_by": self.user.id,
            "status": STATUS_APPROVED,
            "author": self.user.id,
            "vacation_start_date": self.request.vacation_start_date.strftime(
                "%Y-%m-%d"
            ),
            "vacation_end_date": self.request.vacation_end_date.strftime("%Y-%m-%d"),
        }
        self.request.refresh_from_db()
        assert self.request.resolved_by == self.user
        assert self.request.status == STATUS_APPROVED

    def test_with_worker(self):
        """A worker should not be able to access this view"""

        self.client = APIClient()
        self.client.force_authenticate(baker.make(User, type=WORKER_TYPE))

        response = self.client.patch(f"{self.endpoint}{self.request.id}/")

        assert response.status_code == status_constants.HTTP_403_FORBIDDEN
        assert response.data == {
            "detail": ErrorDetail(
                string="You do not have permission to perform this action.",
                code="permission_denied",
            )
        }
