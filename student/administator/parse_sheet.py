import pandas as pd
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from permissions.administrator import AdministratorPermission
from student.utils.save_student import save_student


class ParseStudentSheetView(APIView):
    permission_classes = (IsAuthenticated, AdministratorPermission)

    def post(self, request, *args, **kwargs):
        student_sheet_file = self.request.data.get("parse_sheet")
        print(student_sheet_file)
        if student_sheet_file:
            print("abbbbb")
            df = pd.read_excel(student_sheet_file, engine="openpyxl")  # converters
            print(df, "df")
            role = self.request.query_params.get("role")
            try:
                print("parse_sheet")
                save_student(df, request.institution, request.user.id, role)
            except Exception as e:
                print("excepyion")
                raise ValidationError({"error": [e]})
            return Response({"success": ["student were imported successfully"]})
        raise ValidationError(
            {"missing_file": ["please select valid xlxs file to upload"]}
        )
