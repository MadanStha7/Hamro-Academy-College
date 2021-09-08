import base64
import uuid
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from common.constant import (
    GRADE_CHOICES,
    SUBJECT_TYPES,
    SELECT_GENDER,
    SELECT_MARK_TYPE,
    SELECT_MARITAL_STATUS,
)
from general.models import AcademicSession
from rest_framework.response import Response
from staff.models import StaffAcademicInfo


def return_grade_name_of_value(name):
    for grade in GRADE_CHOICES:
        if grade[0] == name:
            return grade[1]
    return None


def get_subject_type_name_of_value(name):
    for subject_type in SUBJECT_TYPES:
        if subject_type[0] == name:
            return subject_type[1]
    return None


def validate_unique_name(model, value, institution, instance):
    if instance:
        if model.objects.filter(
            ~Q(id=instance.id), name=value.title(), institution=institution
        ).exists():
            raise ValidationError(
                {"message": [f"{model.__name__} with this name already exists"]}
            )
    else:
        if model.objects.filter(name=value.title(), institution=institution).exists():
            raise ValidationError(
                {"message": [f"{model.__name__} with this name already exists"]}
            )

    return value


def validate_unique_role(model, title, institution, instance):
    if instance:
        if model.objects.filter(
            ~Q(id=instance.id), title=title, institution=institution
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this Group already exists."
            )
    else:
        if model.objects.filter(title=title, institution=institution).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this Group already exists."
            )

    return title


@csrf_exempt
def encode_image(request):
    import base64
    from PIL import Image
    from io import BytesIO, StringIO

    image = request.FILES.get("document")
    im = Image.open(image)
    buffered = BytesIO()
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    im.save(buffered, format="JPEG")
    encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse(
        {"encoded_binary_data": "data:image/jpeg;base64," + encoded.decode("utf-8")}
    )


def to_internal_value(data):
    """
    helper function to convert base64 file into corresponding file
    """
    format, data = data.split(";base64,")
    data = bytes(data, encoding="utf-8")
    decoded_file = base64.b64decode(data)
    file_name = str(uuid.uuid4())[:12]
    file_extension = format.split("/")[-1]
    complete_file_name = "%s.%s" % (
        file_name,
        file_extension,
    )
    data = ContentFile(decoded_file, name=complete_file_name)
    return data


def validate_unique_faculty_grade(model, value, institution, instance):
    if instance:
        if model.objects.filter(
            ~Q(id=instance.id),
            faculty=value["faculty"],
            grade=value["grade"],
            institution=institution,
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this faculty and grade already exists"
            )
    else:
        if model.objects.filter(
            faculty=value["faculty"], grade=value["grade"], institution=institution
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this faculty and grade already exists"
            )

    return value


def validate_unique_phone(model, phone, institution, instance):

    if instance:
        if model.objects.filter(
            ~Q(id=instance.user.id), phone=phone, institution=institution
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this phone number already exists"
            )
    else:
        if model.objects.filter(phone=phone, institution=institution).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this phone number already exists"
            )

    return phone


def active_academic_session(institution):
    """
    helper function to get the active academic session
    """
    academic_session = AcademicSession.objects.filter(
        status=True, institution=institution
    ).first()
    if academic_session:
        return academic_session
    raise ValidationError({"error": ["No academic session is currently active"]})


def validate_unique_email(model, email, institution, instance):
    if instance:
        if model.objects.filter(
            ~Q(id=instance.user.id), email=email, institution=institution
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this email already exists"
            )
    else:
        if model.objects.filter(email=email, institution=institution).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this email already exists"
            )

    return email


def return_gender_value(name):
    for gender in SELECT_GENDER:
        if gender[0] == name:
            return gender[1]
    return None


def return_marks_types_value(name):
    for marks_types in SELECT_MARK_TYPE:
        if marks_types[0] == name:
            return marks_types[1]
    return None


def return_marital_status_value(name):
    for marital_status in SELECT_MARITAL_STATUS:
        if marital_status[0] == name:
            return marital_status[1]
    return None


def validate_unique_mobile_number(model, phone, institution, instance):
    if instance:

        if model.objects.filter(
            ~Q(id=instance.id), contact_number=phone, institution=institution
        ).exists():
            raise serializers.ValidationError("phone number already exists")
    else:
        if model.objects.filter(contact_number=phone, institution=institution).exists():
            raise serializers.ValidationError("phone number already exists")

    return phone


def validate_Inquery_unique_email(model, email, institution, instance):
    if instance:
        if model.objects.filter(
            ~Q(id=instance.id), email=email, institution=institution
        ).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this email already exists"
            )
    else:
        if model.objects.filter(email=email, institution=institution).exists():
            raise serializers.ValidationError(
                f"{model.__name__} with this email already exists"
            )

    return email


def validate_object(model, obj_id, institution):
    """Function to check if the database object  exist or not"""
    try:
        model_obj = model.objects.get(id=obj_id, institution=institution)
        return model_obj
    except model.DoesNotExist:
        raise serializers.ValidationError(f"{model.__name__} doesn't exist")


def return_designation_name(staff_id):
    """
    function return the designation name
    """
    try:
        designation = StaffAcademicInfo.objects.values_list(
            "designation__name", flat=True
        ).get(staff__id=staff_id)
        return designation
    except StaffAcademicInfo.DoesNotExist:
        designation = None
