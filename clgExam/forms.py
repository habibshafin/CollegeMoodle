from datetime import datetime
from django import forms
from clgExam.models import CT, Practical

"""
def generate_year_choice_list():
    currentYear = datetime.now().year - 2
    NextYear = currentYear + 1
    YearChoice = []
    for i in range(5):
        YearChoice.append((currentYear, str(currentYear + "-" + NextYear)))
        currentYear = currentYear + 1
    return YearChoice
"""
"""
class ExamEditForm(forms.Form):
    Examiner = forms.CharField(max_length=50, required=False, label="Examiner's Name")
    Session = forms.ChoiceField(required=True, choices=generate_year_choice_list(), label="Exam's Session:")
"""


class CtEditForm(forms.Form):
    TotalMarks = forms.IntegerField(required=True, label='Total Mark of this CT')
    Percentage = forms.IntegerField(required=True, label='Percentage of this CT')
    isResultEntered = forms.BooleanField(required=False, label='Do You Upload Your CT Marks? :')


class PracticalEditForm(forms.Form):
    TotalMarks = forms.IntegerField(label='Total Mark of Practical')
    PassMarks = forms.IntegerField(label='Pass Mark of Practical')
    Percentage = forms.IntegerField(label='Percentage of Practical')
    isResultEntered = forms.BooleanField(required=False, label='Do You Upload Your Practical Marks? :')


class TermFinalEditForm(forms.Form):
    CQMarks = forms.IntegerField(label='Total Mark of CQ')
    MCQMarks = forms.IntegerField(required=False, label='Total Mark of MCQ(if you have any)')
    PassMarksPercentage = forms.IntegerField(label='Pass Mark Percentage(%) of TermFinal', initial=33)
    Percentage = forms.IntegerField(label='Percentage of TermFinal')
    isResultEntered = forms.BooleanField(required=False, label='Do You Upload Your TermFinal Marks? :')


class CtMarkUpdateForm(forms.Form):
    ctId = forms.IntegerField(label='CT ID:', required=False, disabled=True)
    AchievedMarks = forms.IntegerField(label="Update Student's Mark:")

    def clean_achieved_mark(self):
        ctID = self.cleaned_data['ctID']
        ct = CT.objects.get(pk=ctID)
        mark = self.cleaned_data['AchievedMarks']
        if mark > ct.TotalMarks:
            raise forms.ValidationError("Given Mark Is Greater Than Full Mark({})".format(ct.TotalMarks))


class PracticalMarkUpdateForm(forms.Form):
    PracticalId = forms.IntegerField(disabled=True, label='Practical ID:', widget=forms.HiddenInput(), )
    AchievedMarks = forms.IntegerField(label="Update Student's Mark:")

    def clean_achieved_mark(self):
        PracticalId = self.cleaned_data['PracticalId']
        practical = Practical.objects.get(pk=PracticalId)
        mark = self.cleaned_data['AchievedMarks']
        if mark > practical.TotalMarks:
            raise forms.ValidationError("Given Mark Is Greater Than Full Mark({})".format(practical.TotalMarks))
