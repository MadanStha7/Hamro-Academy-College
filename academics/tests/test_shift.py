from rest_framework import status

from academics.models import Faculty, Shift
from authentication.tests.test_auth import AuthTestCase


class ShiftTestCase(AuthTestCase):
    def setUp(self) -> None:
        self.setup_common()
        self.institution = self.get_institution()
        self.url = self.ADMINISTRATOR_URL + "shift/"
        self.faculty = Faculty.objects.create(
            name="Science",
            created_by=self.get_created_by(),
            institution=self.get_institution(),
        )
        self.data = {
           "name":"Morning",
           "faculty": self.faculty,
           "start_time":"10:00",
           "end_time":"11:22",
           "institution": self. institution,
           "created_by": self.get_created_by(),
        }
        shift = Shift.objects.create(**self.data)
        shift.save()
        self.detail_url = self.url + str(shift.id) + "shift/"
        self.token = self.get_token()

    def test_shift_get(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_shift_post(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        data = {"name": "Morning", "faculty": self.faculty.id}
        res = self.client.post(self.url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.change_role()
        res = self.client.post(self.url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_shift_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.change_role()
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

