from django.contrib.auth import get_user_model
from rest_framework import status
from academics.models import Grade, Section
from authentication.tests.test_auth import AuthTestCase

User = get_user_model()


class SectionTestCase(AuthTestCase):
    """
    test case for Section
    CASES tested:
        1. Test Section model
        2. api to get Section
        3. api to post Section
        4. api to delete Section
        5. api to update Section
    """

    def setup_section(self):
        return Section.objects.create(
            name="  A",
            institution=self.get_institution(),
            created_by=self.get_created_by(),
        )

    def setUp(self) -> None:
        self.setup_common()
        self.section = self.setup_section()
        self.token = self.get_token()
        self.url = self.ADMINISTRATOR_URL + "section/"

    def test_created_section(self):
        qs = Section.objects.filter(name="A", created_by=self.get_created_by(), institution=self.get_institution())
        self.assertEqual(qs.count(), 1)

    # API TEST
    def test_get_section(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_section_with_role(self):
        self.change_role()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


