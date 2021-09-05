#
# from rest_framework import status
#
# from common.tests.auth.test_auth import AuthTestCase
#
#
# class GeneralInfoTestCase(AuthTestCase):
#     """
#     tested cases
#         1. create institution
#         2. get institution
#         3. update institution
#         4. delete institution
#     """
#
#     def setUp(self) -> None:
#         self.setup_common()
#         self.url = self.ADMINISTRATOR_URL + "institution/"
#         self.token = self.get_token()
#         self.institution = self.get_institution()
#         self.detail_url = self.url + str(self.institution.id) + "/"
#
#     def test_create_institution(self):
#         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
#         res = self.client.post(self.url)
#         self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_get_institution(self):
#         self.change_role()
#         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
#         res = self.client.get(self.detail_url)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#     def test_update_institution(self):
#         self.change_role()
#         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
#         data = {
#
#             "logo": None,
#             "name": "LA ",
#             "address": "Lalitpur",
#             "phone_number": "987654321",
#             "email": "la@gmail.com",
#             "abbreviation": "la",
#             "slogan": "Best",
#             "school_reg_number": "90678453",
#         }
#         res = self.client.put(self.detail_url, data, format="json")
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         data = {
#             "logo": None,
#             "name": "LA ",
#             "address": "Dhobhighat,Lalitpur",
#             "phone_number": "9860202020",
#             "email": "la@gmail.com",
#             "abbreviation": "la",
#             "slogan": "Best",
#             "school_reg_number": "90678453",
#         }
#         res = self.client.put(self.detail_url, data, format="json")
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#     def test_delete_institution(self):
#         self.change_role()
#         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
#         res = self.client.delete(self.detail_url)
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
