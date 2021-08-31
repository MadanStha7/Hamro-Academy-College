from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from core.models import InstitutionInfo
from user.models import Role, SystemUser

User = get_user_model()


class CommonTestCase(APITestCase):
    ADMINISTRATOR_URL = "/api/v1/"
    STUDENT_URL = "/api/v1/student/"

    @staticmethod
    def setup_common() -> None:
        institution = InstitutionInfo.objects.create(
            name="LA",
            phone_number="9860",
            email="college@gmail.com",
            reg_number="12345",
        )
        user = SystemUser.objects.create(phone="1", institution=institution)
        user.set_password("demo123")
        user.save()
        group = Group.objects.create(name="new")
        group1= Group.objects.create(name="new1")
        Role.objects.create(title="Administrator", group=group, institution=institution)
        Role.objects.create(title="Student", group=group1, institution=institution)

    @staticmethod
    def get_institution():
        institution = InstitutionInfo.objects.get(name="LA")
        return institution

    @staticmethod
    def get_created_by():
        created_by = User.objects.get(phone="1")
        return created_by

    @staticmethod
    def get_administrator_group():
        return Role.objects.get(title="Administrator")

    @staticmethod
    def get_student_group():
        return Role.objects.get(title="Student")
