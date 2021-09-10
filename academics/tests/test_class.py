from rest_framework import status

from academics.models import Grade, Section, Class, Faculty
from authentication.tests.test_auth import AuthTestCase


class ClassTestCase(AuthTestCase):
    def setUp(self) -> None:
        self.setup_common()
        self.institution = self.get_institution()
        self.url = self.ADMINISTRATOR_URL + "class/"
        self.grade = Grade.objects.create(name="1", created_by=self.get_created_by(), institution=self.institution)
        self.section = Section.objects.create(name="A", created_by=self.get_created_by(),  institution=self. institution)
        self.faculty = Faculty.objects.create(
            name="Science",
            created_by=self.get_created_by(),
            institution=self.get_institution(),
        )
        self.data = {
            "grade": self.grade,
            "faculty": self.faculty,
            "institution": self. institution,
            "created_by": self.get_created_by(),
        }
        academic_class = Class.objects.create(**self.data)
        academic_class.section.set([self.section])
        academic_class.save()
        self.detail_url = self.url + str(academic_class.id) + "class/"
        self.token = self.get_token()

    def test_class_get(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_class_post(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        data = {"grade": self.grade.id,"faculty": self.faculty.id,  "section": [self.section.id]}
        res = self.client.post(self.url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.change_role()
        res = self.client.post(self.url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_class_update(self):
        section = Section.objects.create(name="A", institution=self.institution)
        data = {"grade": self.grade.id, "faculty": self.faculty.id, "section": [section.id]}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.put(self.detail_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.change_role()
        res = self.client.put(self.detail_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_class_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.change_role()
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


