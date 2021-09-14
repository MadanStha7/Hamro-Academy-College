from uuid import UUID
from academics import models as orm


class SubjectGroupRepository:
    def __init__(self) -> None:
        pass

    def get(self, institution: UUID, pk=None):
        subject_groups = orm.SubjectGroup.objects.filter(institution=institution)
        return subject_groups
