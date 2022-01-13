from django.db import models
from clgStudent.models import Subjects, StudentInfo


class Term(models.Model):
    YearStatusList = (
        ('1', 'First Year'),
        ('2', 'Second Year'),
    )
    TermId = models.AutoField(primary_key=True, unique=True, )
    TermName = models.CharField(max_length=40, verbose_name="Term Name", )
    YearStatus = models.CharField(max_length=1, choices=YearStatusList, default='1', )

    def __str__(self):
        return self.TermName


class Exam(models.Model):
    ExamID = models.AutoField(primary_key=True, unique=True, verbose_name="Exam ID", )
    TermId = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="TermExams", )
    Sub_Code = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name="SubjectExams", )
    Examiner = models.CharField(max_length=50, verbose_name="Examiner Name", null=True)
    Session = models.PositiveIntegerField(null=True)
    Group = models.CharField(max_length=12, null=True)

    # @TODO: NEED TO CHEK % AS individula % has been added to each subExams
    # ctPercentage = models.PositiveIntegerField(max_length=3, default=0,)
    # TermFinalPercentage = models.PositiveIntegerField(max_length=3,)
    # PracticalPercentage = models.PositiveIntegerField(max_length=3, )

    class Meta:
        # order descending. Latest Exams will be on Top
        ordering = ['-ExamID']


ReasonList = (
    ('1', 'Absent'),
    ('2', 'Non Collegiate'),
)


class CT(models.Model):
    ctId = models.AutoField(primary_key=True, unique=True, )
    ExamID = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="CTs", )
    TotalMarks = models.PositiveIntegerField(null=True)
    isResultEntered = models.BooleanField(null=True)
    ctPercentage = models.PositiveIntegerField(null=True)
    CT_Marks = models.ManyToManyField(StudentInfo, through='CTMarks',
                                      through_fields=('ctId', 'Roll'), related_name='allCtMarks')
    CT_Absent = models.ManyToManyField(StudentInfo, through='CTAbsent',
                                       through_fields=('ctId', 'Roll'), related_name='CTAbsents')

    class Meta:
        ordering = ['-ExamID', 'ctId']


class CTMarks(models.Model):
    ctId = models.ForeignKey(CT, on_delete=models.CASCADE)
    Roll = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    AchievedMarks = models.PositiveIntegerField()

    class Meta:
        ordering = ['-ctId', 'Roll']


class CTAbsent(models.Model):
    ctId = models.ForeignKey(CT, on_delete=models.CASCADE)
    Roll = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    Reason = models.CharField(max_length=1, choices=ReasonList, default='1', )

    class Meta:
        ordering = ['-ctId', 'Roll']


class Practical(models.Model):
    ExamID = models.OneToOneField(Exam, on_delete=models.CASCADE, )
    PracticalId = models.AutoField(primary_key=True, unique=True, )
    TotalMarks = models.PositiveIntegerField(default=25, )
    PassMarks = models.PositiveIntegerField(null=True)
    isResultEntered = models.BooleanField(null=True)
    PracticalPercentage = models.PositiveIntegerField(null=True)
    Practical_Marks = models.ManyToManyField(StudentInfo, through='PracticalMarks',
                                             through_fields=('PracticalId', 'Roll'), related_name='allPracticalMarks')
    Practical_Absent = models.ManyToManyField(StudentInfo, through='PracticalAbsent',
                                              through_fields=('PracticalId', 'Roll'), related_name='PracticalAbsents')

    class Meta:
        ordering = ['-ExamID', 'PracticalId']


class PracticalMarks(models.Model):
    PracticalId = models.ForeignKey(Practical, on_delete=models.CASCADE)
    Roll = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    AchievedMarks = models.PositiveIntegerField()

    class Meta:
        ordering = ['-PracticalId', 'Roll']


class PracticalAbsent(models.Model):
    PracticalId = models.ForeignKey(Practical, on_delete=models.CASCADE)
    Roll = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    Reason = models.CharField(max_length=1, choices=ReasonList, default='1', )

    class Meta:
        ordering = ['-PracticalId', 'Roll']


class TermFinal(models.Model):
    ExamID = models.OneToOneField(Exam, on_delete=models.CASCADE, )
    TermFinalId = models.AutoField(primary_key=True, unique=True, )
    TotalMarks = models.PositiveIntegerField(null=True)
    CQ = models.PositiveIntegerField(null=True)#
    MCQ = models.PositiveIntegerField(null=True)#
    PassPercentage = models.PositiveIntegerField(null=True, blank=True)#
    isResultEntered = models.BooleanField(null=True)
    TermFinalPercentage = models.PositiveIntegerField(null=True)
    TermFinal_Marks = models.ManyToManyField(StudentInfo, through='TermFinalMarks',
                                             through_fields=('TermFinalId', 'Roll'), related_name="allTermFinalMarks")
    TermFinal_Absent = models.ManyToManyField(StudentInfo, through='TermFinalAbsent',
                                              through_fields=('TermFinalId', 'Roll'), related_name='TermFinalAbsents')

    class Meta:
        ordering = ['-ExamID', 'TermFinalId']


class TermFinalMarks(models.Model):
    TermFinalId = models.ForeignKey(TermFinal, on_delete=models.CASCADE)
    Roll = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    AchievedMarksCQ = models.PositiveIntegerField()
    AchievedMarksMCQ = models.PositiveIntegerField()

    class Meta:
        ordering = ['-TermFinalId', 'Roll']


class TermFinalAbsent(models.Model):
    TermFinalId = models.ForeignKey(TermFinal, on_delete=models.CASCADE)
    Roll = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    Reason = models.CharField(max_length=1, choices=ReasonList, default='1', )

    class Meta:
        ordering = ['-TermFinalId', 'Roll']


class CustomExam(models.Model):
    CustomExamId = models.AutoField(primary_key=True, unique=True, )
    ExamID = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="CustomExams", )
    ExamName = models.CharField(max_length=40, verbose_name="Exam Name", )
    TotalMarks = models.PositiveIntegerField()
    CQ = models.PositiveIntegerField()
    MCQ = models.PositiveIntegerField()
    PassMarksCQ = models.PositiveIntegerField()
    PassMarksMCQ = models.PositiveIntegerField()
    isResultEntered = models.BooleanField()
    CustomExamPercentage = models.PositiveIntegerField()
    CustomExam_Marks = models.ManyToManyField(StudentInfo, through='CustomExamMarks',
                                              through_fields=('CustomExamId', 'Roll'),
                                              related_name='allCustomExamMarks')
    CustomExam_Absent = models.ManyToManyField(StudentInfo, through='CustomExamAbsent',
                                               through_fields=('CustomExamId', 'Roll'),
                                               related_name='CustomExamAbsents')

    class Meta:
        ordering = ['-ExamID', 'CustomExamId']


class CustomExamMarks(models.Model):
    CustomExamId = models.ForeignKey(CustomExam, on_delete=models.CASCADE)
    Roll = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    AchievedMarksCQ = models.PositiveIntegerField()
    AchievedMarksMCQ = models.PositiveIntegerField(default=0, )

    class Meta:
        ordering = ['-CustomExamId', 'Roll']


class CustomExamAbsent(models.Model):
    CustomExamId = models.ForeignKey(CustomExam, on_delete=models.CASCADE)
    Roll = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    Reason = models.CharField(max_length=1, choices=ReasonList, default='1', )

    class Meta:
        ordering = ['-CustomExamId', 'Roll']
