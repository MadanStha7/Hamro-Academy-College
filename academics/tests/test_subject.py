from django.contrib.auth import get_user_model
from rest_framework import status
from academics.models import Subject
from authentication.tests.test_auth import AuthTestCase

User = get_user_model()


class SubjectTestCase(AuthTestCase):
    """
    test case for Subject
    CASES tested:
        1. Test Subject model
        2. api to get Subject
        3. api to post Subject
        4. api to delete Subject
        5. api to update Subject
    """

    def setup_subject(self):
        return Subject.objects.create(
            name="Physics",
            credit_hour="3.0",
            institution=self.get_institution(),
            created_by=self.get_created_by(),
        )

    def setUp(self) -> None:
        self.setup_common()
        self.subject = self.setup_subject()
        self.token = self.get_token()
        self.url = self.ADMINISTRATOR_URL + "subject/"

    def test_created_subject(self):
        qs = Subject.objects.filter(name="Physics", institution=self.get_institution())
        self.assertEqual(qs.count(), 1)

    # API TEST
    def test_get_subject(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_subject_with_role(self):
        self.change_role()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    #
    # def test_post_subject(self):
    #     # self.change_role()
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
    #     data = {"name": "Computer", "credit_hour": "3.0"}
    #     res = self.client.post(self.url, data, format="json")
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     all_subject = Subject.objects.all()
    #     self.assertEqual(all_subject.count(), 2)
    #
    # def test_delete_subject(self):
    #     # self.change_role()
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
    #     subject = Subject.objects.filter(name="Physics").first()
    #     res = self.client.delete(self.url + str(subject.id) + "/")
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    # def test_update_subject(self):
    #     self.change_role()
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
    #     data = {"name": "English"}
    #     subject = Subject.objects.filter(name="Physics").first()
    #     res = self.client.put(self.url + str(subject.id) + "/", data, format="json")
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    # def test_detail_subject(self):
    #     self.change_role()
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
    #     subject = Subject.objects.filter(name="Physics").first()
    #     res = self.client.get(self.url + str(subject.id) + "/")
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
