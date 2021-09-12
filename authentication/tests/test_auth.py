from rest_framework import status
from common.tests.test_common import CommonTestCase


class AuthTestCase(CommonTestCase):
    """
    test case to check if token get api is working
    """

    def setUp(self) -> None:
        self.setup_common()

    def test_get_token(self):
        data = {"phone": self.get_created_by().phone, "password": "demo123"}
        url = self.ADMINISTRATOR_URL + "token/"
        res = self.client.post(path=url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        return res.data.get("token").get("access")

    def get_token(self):
        token = self.test_get_token()
        return token

    def change_role(self):
        role = self.get_administrator_group()
        self.get_created_by().roles.add(role)
        self.get_created_by().save()

    def student_change_role(self):
        role = self.get_student_group()
        self.get_created_by().roles.add(role)
        self.get_created_by().save()

    def teacher_change_role(self):
        role = self.get_teacher_group()
        self.get_created_by().roles.add(role)
        self.get_created_by().save()
