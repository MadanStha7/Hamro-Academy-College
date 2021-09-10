from django.contrib.auth import get_user_model
from rest_framework import status
from academics.models import Faculty
from authentication.tests.test_auth import AuthTestCase

User = get_user_model()


class SubjectTestCase(AuthTestCase):
    """
    test case for Faculty
    CASES tested:
        1. Test Faculty model
        2. api to get Faculty
        3. api to post Faculty
        4. api to delete Faculty
        5. api to update Faculty
    """

    def setup_faculty(self):
        return Faculty.objects.create(
            name="Science",
            institution=self.get_institution(),
            created_by=self.get_created_by(),
        )

    def setUp(self) -> None:
        self.setup_common()
        self.grade = self.setup_faculty()
        self.token = self.get_token()
        self.url = self.ADMINISTRATOR_URL + "faculty/"

    def test_created_faculty(self):
        qs = Faculty.objects.filter(name="Science", created_by= self.get_created_by(), institution=self.get_institution())
        self.assertEqual(qs.count(), 1)

    # API TEST
    def test_get_faculty(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_faculty_with_role(self):
        self.change_role()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


