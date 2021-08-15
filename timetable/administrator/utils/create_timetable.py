from rest_framework.serializers import ValidationError
from django.db import transaction, IntegrityError
from rest_framework.response import Response
from django.core.exceptions import BadRequest
from common.utils import active_academic_session
from timetable.models import TimeTable
from academics.models import Section, Grade, Subject, Faculty, Shift
from general.models import AcademicSession
from django.contrib.auth import get_user_model
from itertools import product


User = get_user_model()


def create_timetable(infos, user, institution):
    """
    api to create a bulk timetable
    """
    new_timetables = []
    updated_timetable = []
    active_session = active_academic_session(institution)

    # check the validation
    # valid_timetable = validate_timetable(infos,active_session,user, institution)
    # print("valid timetable",valid_timetable)
    # for case of update
    for info in infos:
        if info.get("start_time") > info.get("end_time"):
            raise ValidationError({"error": ["Start time must be greater than end date"]})
        get_id = info.get("id", None)
        if get_id:
            timetable = TimeTable(id=info.get("id"))
            timetable.teacher = User(id=info.get("teacher"))
            timetable.subject = Subject(id=info.get("subject"))
            timetable.start_time = info.get("start_time")
            timetable.end_time = info.get("end_time")
            timetable.day = info.get("day")
            timetable.faculty = Faculty(id=info.get("faculty").id)
            timetable.grade = Grade(id=info.get("grade").id)
            timetable.shift = Shift(id=info.get("shift").id)
            if info.get("section"):
                timetable.section = Section(id=info.get("section").id)
            updated_timetable.append(timetable)

        # for case of create
        else:
            timetable = TimeTable(
                day=info.get("day"),
                start_time=info.get("start_time"),
                end_time=info.get("end_time"),
                teacher=User(id=info.get("teacher")),
                faculty=info.get("faculty"),
                grade=info.get("grade"),
                shift=info.get("shift"),
                subject=Subject(id=info.get("subject")),
                created_by=user,
                institution=institution,
                academic_session=active_session,
            )
            if info.get("section"):
                timetable.section = info.get("section")
            new_timetables.append(timetable)

    with transaction.atomic():
        try:
            timetable_create = TimeTable.objects.bulk_create(new_timetables)
        except IntegrityError:
            raise ValidationError({"error": ["duplicate timetable is not allowed"]})

        update_timetable_list = TimeTable.objects.bulk_update(
            updated_timetable,
            fields=[
                "teacher",
                "start_time",
                "end_time",
                "day",
                "subject",
                "faculty",
                "grade",
                "shift",
                "section",
            ],
        )
        return {
            "data1": timetable_create if timetable_create else [],
            "data2": updated_timetable if updated_timetable else [],
        }


def create_apply_timetable(data, days, user, institution):
    """
    api to create a multiple timetable at once for multiple days
    """
    with transaction.atomic():
        active_session = active_academic_session(institution)
        # check the validation
        # valid_timetable = validate_timetable(infos,active_session,user, institution)
        
        new_timetables = []
        for item in data:
            if item.get("start_time") > item.get("end_time"):
                raise ValidationError({"error": ["Start time must be greater than end date"]})
            timetable = TimeTable(
                start_time=item.get("start_time"),
                end_time=item.get("end_time"),
                teacher=User.objects.get(id=item.get("teacher")),
                faculty=Faculty.objects.get(id=item.get("faculty").id),
                grade=Grade.objects.get(id=item.get("grade").id),
                shift=Shift.objects.get(id=item.get("shift").id),
                subject=Subject.objects.get(id=item.get("subject")),
                created_by=user,
                institution=institution,
                academic_session=active_session,
            )

            if item.get("section"):
                timetable.section = Section(id=item.get("section").id)
            new_timetables.append(timetable)

        day_id = [day for day in days if days.count(day) > 1]
        if day_id:
            raise ValidationError({"error": ["Similar timetable cannot be assigned"]})
        timetable_create = []
        timetable_dict = {}
        for timetable, day in list(product(new_timetables, days)):
            timetable_data = TimeTable(
                timetable.__dict__, timetable.__dict__.update(day=str(day))
            )
            # print("day",timetable_data.__dict__)
            timetable_dict.update(timetable_data.__dict__["id"])
            final_timetable_data = timetable_dict.copy()
            final_timetable = TimeTable(
                    start_time=final_timetable_data.get("start_time"),
                    end_time=final_timetable_data.get("end_time"),
                    teacher=User(id=final_timetable_data.get("teacher_id")),
                    faculty=Faculty(id=final_timetable_data.get("faculty_id")),
                    grade=Grade(final_timetable_data.get("grade_id")),
                    shift=Shift(final_timetable_data.get("shift_id")),
                    subject=Subject(id=final_timetable_data.get("subject_id")),
                    created_by=user,
                    institution=institution,
                    academic_session=AcademicSession(
                        id=final_timetable_data.get("academic_session_id")
                    ),
                    day=final_timetable_data.get("day"),
                )
            if final_timetable_data.get("section_id"):
                final_timetable.section = Section(id=final_timetable_data.get("section_id"))
            timetable_create.append(final_timetable)
            
    with transaction.atomic():
        try:
            timetable_create_data = TimeTable.objects.bulk_create(timetable_create)
        except IntegrityError:
            raise ValidationError({"error": ["duplicate timetable is not allowed"]})
        return {
            "data": timetable_create_data if timetable_create_data else [],
        }
