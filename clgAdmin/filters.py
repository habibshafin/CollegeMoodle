from clgStudent.models import StudentInfo
from clgExam.filters import session_generate
import django_filters


class StudentFilter(django_filters.FilterSet):
    Name = django_filters.CharFilter(lookup_expr='icontains')
    Session = django_filters.ChoiceFilter(choices=session_generate())

    class Meta:
        model = StudentInfo
        fields = ['Roll', 'Name', 'Group', 'Session', 'YearStatus']
