from django.contrib.auth import get_user_model
from rest_framework import status
from academics.models import  Grade
from authentication.tests.test_auth import AuthTestCase

User = get_user_model()


class SubjectTestCase(AuthTestCase):
    """
    test case for Grade
    CASES tested:
        1. Test Grade model
        2. api to get Grade
        3. api to post Grade
        4. api to delete Grade
        5. api to update Grade
    """

    def setup_grade(self):
        return Grade.objects.create(
            name="11",
            institution=self.get_institution(),
            created_by=self.get_created_by(),
        )

    def setUp(self) -> None:
        self.setup_common()
        self.grade = self.setup_grade()
        self.token = self.get_token()
        self.url = self.ADMINISTRATOR_URL + "grade/"

    def test_created_grade(self):
        qs = Grade.objects.filter(name="11", created_by= self.get_created_by(), institution=self.get_institution())
        self.assertEqual(qs.count(), 1)

    # API TEST
    def test_get_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_grade_with_role(self):
        self.change_role()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


