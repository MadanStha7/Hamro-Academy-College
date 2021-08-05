from rest_framework.serializers import ValidationError
from django.db import transaction, IntegrityError
from timetable.models import TimeTable
from academics.models import Section, Grade, Subject, Faculty, Shift
from django.contrib.auth import get_user_model
from general.models import AcademicSession

User = get_user_model()


def active_academic_session(institution):
    """
    helper function to get the active academic session
    """
    active_academic_session = AcademicSession.objects.filter(
        status=True, institution=institution
    ).first()
    if active_academic_session:
        return active_academic_session
    raise ValidationError({"error": ["No academic session is currently active"]})


def create_timetable(infos, user, institution):
    """
    api to create a bulk timetable
    """
    new_timetables = []
    updated_timetable = []
    active_session = active_academic_session(institution)
    print("active_session", active_session)
    print("infos", infos)
    # for case of update
    for info in infos:
        print("info", info)
        get_id = info.get("id", None)
        print("get id", get_id)
        if get_id:
            timetable = TimeTable.objects.get(id=info.get("id"))
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
                teacher=User.objects.get(id=info.get("teacher")),
                faculty=info.get("faculty"),
                grade=info.get("grade"),
                shift=info.get("shift"),
                subject=Subject.objects.get(id=info.get("subject")),
                created_by=user,
                institution=institution,
                academic_session=active_session,
            )
            if info.get("section"):
                print("section", info.get("section"))
                timetable.section = info.get("section")
            new_timetables.append(timetable)

    with transaction.atomic():
        try:
            print("new_timetables", type(new_timetables))
            for item in new_timetables:
                print("item day", item)
            timetable_create = TimeTable.objects.bulk_create(new_timetables)
            print("created_timetable#########", timetable_create)
        except IntegrityError:
            raise ValidationError({"error": ["duplicate timetable is not allowed"]})
        return {"timetable_create": timetable_create if timetable_create else []}
