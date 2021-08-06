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

    # for case of update
    for info in infos:
        get_id = info.get("id", None)
        if get_id:
            timetable = TimeTable(id=info.get("id"))
            timetable.teacher = User(id=info.get("teacher"))
            timetable.faculty = Faculty(id=info.get("faculty"))
            timetable.grade = Grade(id=info.get("grade"))
            timetable.shift = Shift(id=info.get("shift"))
            timetable.subject = Subject(id=info.get("subject"))
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
        return {"timetable_create": timetable_create if timetable_create else []}
