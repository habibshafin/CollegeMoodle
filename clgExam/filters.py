from .models import Exam
import django_filters
from datetime import datetime

Group_CHOICES = (
    ('S', 'Science'),
    ('C', 'Commerce',),
    ('A', 'Arts',),
)


def session_generate():
    currentYear = datetime.now().year - 2
    NextYear = currentYear + 1
    # print(str(currentYear) + "-" + str(NextYear))
    YearChoice = []
    # YearChoice.append((currentYear, str(currentYear)+"-"+str(NextYear)))
    # print(YearChoice)
    for i in range(5):
        YearChoice.append((currentYear, str(currentYear) + "-" + str(NextYear)))
        currentYear = currentYear + 1
        NextYear = NextYear + 1
    # print(YearChoice)
    return YearChoice


class ExamFilter(django_filters.FilterSet):
    Group = django_filters.ChoiceFilter(choices=Group_CHOICES)
    Session = django_filters.ChoiceFilter(choices=session_generate())

    class Meta:
        model = Exam
        fields = ['TermId', 'Sub_Code']
