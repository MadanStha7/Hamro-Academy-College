from django.contrib.auth import get_user_model
from rest_framework import status
from academics.models import SubjectGroup, Subject, Grade, Faculty, Section
from authentication.tests.test_auth import AuthTestCase

User = get_user_model()


class SubjectTestCase(AuthTestCase):
    """
    test case for SubjectGroup
    CASES tested:
        1. Test SubjectGroup model
        2. api to get SubjectGroup
        3. api to post SubjectGroup
        4. api to delete SubjectGroup
        5. api to update SubjectGroup
    """

    def setUp(self) -> None:
        self.setup_common()
        self.subject = Subject.objects.create(
            name="Physics",
            credit_hour="3.0",
            created_by=self.get_created_by(),
            institution=self.get_institution(),
        )
        self.grade = Grade.objects.create(
            name="1",
            created_by=self.get_created_by(),
            institution=self.get_institution(),
        )
        self.faculty = Faculty.objects.create(
            name="Science",
            created_by=self.get_created_by(),
            institution=self.get_institution(),
        )
        self.section = Section.objects.create(
            name="SEC1",
            created_by=self.get_created_by(),
            institution=self.get_institution(),
        )
        self.data = {
            "name": "New",
            "grade": self.grade,
            "faculty": self.faculty,
            "description": "desc",
            "created_by": self.get_created_by(),
            "institution": self.get_institution(),
        }
        subject_group = SubjectGroup.objects.create(**self.data)
        subject_group.section.set([self.section])
        subject_group.subject.set([self.subject])

        subject_group.save()
        self.token = self.get_token()
        self.url = self.ADMINISTRATOR_URL + "subject_group/"

    # API TEST
    def test_get_subject_group(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # def test_subject_group_post(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
    #     data = {
    #         "grade": self.grade.id,
    #         "subject": self.subject.id,
    #         "section": self.section.id,
    #         "faculty": self.faculty.id,
    #         "name": "Newname",
    #         "description": "desc",
    #     }
    #     res = self.client.post(self.url, data=data, format="json")
    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    #     res = self.client.post(self.url, data=data, format="json")
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
