from common.constant import GRADE_CHOICES


def return_grade_name_of_value(name):

    for grade in GRADE_CHOICES:
        if grade[0] == name:
            return grade[1]
    return None
