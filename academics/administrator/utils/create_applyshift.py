from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError
from academics.models import Grade, ApplyShift, Faculty, Shift, Section


def create_applyshift(infos, user, institution):
    new_applyshift = []
    updated_applyshift = []

    # for case of update
    for info in infos:
        get_id = info.get("id", None)
        if get_id:
            applyshift = ApplyShift(id=info.get("id"))
            applyshift.faculty = Faculty(id=info.get("faculty"))
            applyshift.grade = Grade(id=info.get("grade"))
            applyshift.shift = Shift(id=info.get("shift"))
            applyshift.section = Section(id=info.get("section"))
            updated_applyshift.append(applyshift)

        # for case of create
        else:
            applyshift = ApplyShift(
                faculty=Faculty(id=info.get("faculty")),
                grade=Grade(id=info.get("grade")),
                shift=Shift(id=info.get("shift")),
                created_by=user,
                institution=institution,
            )

            if info.get("section"):
                applyshift.section = Section(id=info.get("section"))
            new_applyshift.append(applyshift)

    with transaction.atomic():
        try:
            applyshift_create = ApplyShift.objects.bulk_create(new_applyshift)
        except IntegrityError:
            raise ValidationError({"error": ["duplicate applyshift is not allowed"]})

        ApplyShift.objects.bulk_update(
            updated_applyshift,
            [
                "faculty",
                "grade",
                "shift",
            ],
        )
        return {
            "data1": applyshift_create if applyshift_create else [],
            "data2": updated_applyshift if updated_applyshift else [],
        }
