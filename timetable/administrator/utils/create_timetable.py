from rest_framework.serializers import ValidationError
from django.db import transaction, IntegrityError
from common.utils import active_academic_session
from timetable.models import TimeTable
from academics.models import Section, Grade, Subject, Faculty, Shift
from django.contrib.auth import get_user_model


User = get_user_model()


def create_timetable(infos, user, institution):
    """
    api to create a bulk timetable
    """
    print("infos", infos)
    new_timetables = []
    updated_timetable = []
    active_session = active_academic_session(institution)

    # check the validation
    # valid_timetable = validate_timetable(infos,active_session,user, institution)
    # print("valid timetable",valid_timetable)
    # for case of update
    for info in infos:
        print("info", infos)
        get_id = info.get("id", None)
        if get_id:
            timetable = TimeTable(id=info.get("id"))
            timetable.teacher = User(id=info.get("teacher"))
            timetable.faculty = Faculty(id=info.get("faculty"))
            timetable.grade = Grade(id=info.get("grade"))
            timetable.shift = Shift(id=info.get("shift"))
            timetable.subject = Subject.objects.get(id=info.get("subject"))
            timetable.day = (info.get("day"),)
            timetable.start_time = (info.get("start_time"),)
            timetable.end_time = (info.get("end_time"),)
            print("dat1", User(id=info.get("teacher")))
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
            print("grade in else", info.get("grade"))
            print("teacher in else", info.get("teacher"))

            if info.get("section"):
                timetable.section = info.get("section")
            new_timetables.append(timetable)

    with transaction.atomic():
        print("updated timetable", updated_timetable)
        try:
            timetable_create = TimeTable.objects.bulk_create(new_timetables)
        except IntegrityError:
            raise ValidationError({"error": ["duplicate timetable is not allowed"]})

        TimeTable.objects.bulk_update(
            updated_timetable,
            [
                "teacher",
                "start_time",
                "end_time",
                "day",
                "subject",
                "faculty",
                "grade",
                "shift",
                "section",
                "subject",
                "academic_session",
            ],
        )
        return {
            "data1": timetable_create if timetable_create else [],
            "data2": updated_timetable if updated_timetable else [],
        }
