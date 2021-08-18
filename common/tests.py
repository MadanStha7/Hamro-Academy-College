from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from core.models import InstitutionInfo
from user.models import Role

User = get_user_model()


class CommonTestCase(APITestCase):
    ADMINISTRATOR_URL = "/api/v1/"

    @staticmethod
    def setup_common() -> None:
        institution = InstitutionInfo.objects.create(
            name="LA",
            phone_number="9860202020",
            abbreviation="la",
            address="Lalitpur",
            email="school@gmail.com",
            reg_number="12345",
            slogan="focus on yourself"
        )
        user = User.objects.create(username="la", institution=institution)
        user.set_password("kapan123")
        user.save()
        Role.objects.create(name="Administrator", institution=institution)

    @staticmethod
    def get_institution():
        institution = InstitutionInfo.objects.get(name="LA")
        return institution

    @staticmethod
    def get_created_by():
        created_by = User.objects.get(username="la")
        return created_by

    @staticmethod
    def get_administrator_group():
        return Role.objects.get(name="Administrator")

    @staticmethod
    def get_teacher_group():
        return Role.objects.get(name="Teacher")
