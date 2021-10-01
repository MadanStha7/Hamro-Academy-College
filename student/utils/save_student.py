from django.contrib.auth import get_user_model
from django.db import transaction

from core.models import InstitutionInfo
from guardian.models import StudentGuardianInfo
from student.models import StudentInfo, StudentAcademicDetail
from user.models import Role

User = get_user_model()


def save_student(df, institution, created_by, role):
    bulk_user_create = []
    bulk_guardian_create = []
    bulk_student_create = []
    bulk_student_academic_info_create = []
    for record in df.to_records():
        user = User(
            username=record.phone,
            first_name=record.first_name,
            middle_name=record.middle_name,
            last_name=record.last_name,
            email=record.email,
            phone=record.phone,
            institution=InstitutionInfo(id=institution),
        )
        bulk_user_create.append(user)

        guardian = StudentGuardianInfo(
            user=user,
            relation=record.relation,
            institution=InstitutionInfo(id=institution),
        )
        bulk_guardian_create.append(guardian)
        student = StudentInfo(
            user=user,
            guardian=guardian,
            gender=record.gender,
            permanent_address=record.permanent_address,
            temporary_address=record.address,
            institution=InstitutionInfo(id=institution),
            created_by=User(id=created_by),
        )

        student_academic_info = StudentAcademicDetail(
            student=student,
            faculty=record.faculty,
            grade=record.grade,
            section=record.section,
            institution=InstitutionInfo(id=institution),
            created_by=User(id=created_by),
        )
        bulk_student_academic_info_create.append( student_academic_info)
        bulk_student_create.append(student)

    with transaction.atomic():
        users = User.objects.bulk_create(bulk_user_create)
        user_group = Role.objects.get(id=role)
        user_group.user_set.add(*users)
        StudentInfo.objects.bulk_create(bulk_student_create)
        StudentAcademicDetail.objects.bulk_create(bulk_student_academic_info_create)
        return True
