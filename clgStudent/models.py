import os
from pathlib import Path
from uuid import uuid4
from django.contrib.auth.models import User
from .validators import validate_file_size
from django.db import models


def validate_image(image):
    file_size = image.file.size
    limit_kb = 10
    if file_size > limit_kb * 1024:
        print("Max size of file is %s KB" % limit_kb)
        return False
    else:
        return True

    # limit_mb = 8
    # if file_size > limit_mb * 1024 * 1024:
    #    raise ValidationError("Max size of file is %s MB" % limit_mb)


# to rename the uploaded profile picture in a particular directory
def path_and_rename(instance, filename):
    upload_to = 'profile_image'
    print("instance:")
    print(instance)
    print("filename:")
    print(filename)

    ext = filename.split('.')[-1]

    if instance.pk:
        print("if e asche")
        filename = '{}.{}'.format(instance.pk, ext)
        p = os.path.join('media/profile_image', filename)
        my_file = Path(p)
        file_size = instance.image.file.size
        print(file_size)
        validate_image(instance.image)
        if my_file.is_file():
            print("file exists")
            os.remove(p)
            print("image removed")
    # file exists

    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # if os.path.exists(upload_to + filename):
    #   print("file exists")
    # filename = instance.cleaned_data.get("filename", False)
    # if os.path.isfile(destination + filename.name):
    #   print('A file with the name "' + filename+ '" already exists. Please, rename your file and try again.')
    # return the whole path to the file
    print(filename)
    print(os.path.join(upload_to, filename))
    return os.path.join(upload_to, filename)


class StudentInfo(models.Model):
    GenderList = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )

    GroupList = (
        ('S', 'Science'),
        ('A', 'Arts'),
        ('C', 'Commerce'),
    )

    YearStatusList = (
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('P', 'Test Passed'),
    )

    user_ref = models.OneToOneField(User, on_delete=models.CASCADE)

    Roll = models.PositiveIntegerField(primary_key=True, unique=True, verbose_name="College Roll", )
    Name = models.CharField(max_length=50, blank=True, null=True)
    Sex = models.CharField(max_length=1, choices=GenderList, blank=True, null=True)
    Group = models.CharField(max_length=1, choices=GroupList, blank=True, null=True)
    Father_Name = models.CharField(max_length=50, verbose_name="Father's Name", blank=True, null=True)
    Mother_Name = models.CharField(max_length=50, verbose_name="Mother's Name", blank=True, null=True)
    DOB = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    Guardian_Mobile_No = models.CharField(max_length=14, blank=True, null=True)
    Session = models.PositiveIntegerField(null=True)
    YearStatus = models.CharField(max_length=1, choices=YearStatusList, default='1', blank=True, null=True)
    Password = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to=path_and_rename, blank=True, null=True, validators=[validate_file_size])

    class Meta:
        ordering = ['Roll']
    #
    # def __str__(self):
    #     return self.Roll


class BoardResult(models.Model):
    BoardList = (
        ('1', 'Dhaka'),
        ('2', 'Chittagong'),
        ('3', 'Comilla'),
        ('4', 'Rajshahi'),
        ('5', 'Khulna'),
        ('6', 'Rajshahi'),
        ('7', 'Barisal'),
        ('8', 'Dinajpur'),
        ('9', 'Others'),
    )
    Roll = models.OneToOneField(StudentInfo, on_delete=models.CASCADE, primary_key=True, verbose_name="College Roll")
    Registration_No = models.IntegerField(unique=True, verbose_name="Registration No")
    SSC_Roll = models.PositiveIntegerField(verbose_name="SSC Roll")
    SSC_Board = models.CharField(choices=BoardList, max_length=1, verbose_name="SSC Board")
    SSC_Gpa = models.FloatField(verbose_name="SSC GPA")
    JSC_Gpa = models.FloatField(verbose_name="JSC GPA")

    # get_FOO_display()  to display SSC Board

    class Meta:
        ordering = ['Roll']

    # def __str__(self):
    #     return self.Roll


class Subjects(models.Model):
    SubjectCategory = (
        ('C', 'Compulsory'),
        ('O', 'Optional'),
        ('B', 'Compulsory & Optional'),
        ('X', '--'),
        # ('X', '--') means that this subject is not for that group , it works kind of null/NONE/False
    )

    Sub_Code = models.CharField(primary_key=True, unique=True, max_length=3, verbose_name="Subject Code")
    Sub_Name = models.CharField(max_length=50)
    ScienceType = models.CharField(max_length=1, choices=SubjectCategory, default='X', verbose_name="Science Type")
    ArtsType = models.CharField(max_length=1, choices=SubjectCategory, default='X', verbose_name="Arts Type")
    CommerceType = models.CharField(max_length=1, choices=SubjectCategory, default='X', verbose_name="Commerce Type")

    class Meta:
        ordering = ['Sub_Code']

    def __str__(self):
        return self.Sub_Name


# class StudentSubjects(models.Model):
#     Roll = models.OneToOneField(StudentInfo, on_delete=models.CASCADE)
#     Compulsory_Subjects = models.ManyToManyField(Subjects, related_name="CompulsorySubjects")
#     Optional_Subjects = models.ManyToManyField(Subjects, related_name="OptionalSubjects")
#
#     class Meta:
#         ordering = ['Roll']


class StudentSubjects(models.Model):
    Roll = models.OneToOneField(StudentInfo, on_delete=models.CASCADE, primary_key=True)
    comSub_11 = models.ForeignKey(Subjects, related_name="com11", on_delete=models.CASCADE, null=True)
    comSub_12 = models.ForeignKey(Subjects, related_name="com12", on_delete=models.CASCADE, null=True)
    comSub_21 = models.ForeignKey(Subjects, related_name="com21", on_delete=models.CASCADE, null=True)
    comSub_22 = models.ForeignKey(Subjects, related_name="com22", on_delete=models.CASCADE, null=True)
    comSub_31 = models.ForeignKey(Subjects, related_name="com31", on_delete=models.CASCADE, null=True)
    comSub_32 = models.ForeignKey(Subjects, related_name="com32", on_delete=models.CASCADE, null=True)
    opSub_11 = models.ForeignKey(Subjects, related_name="op11", on_delete=models.CASCADE, null=True)
    opSub_12 = models.ForeignKey(Subjects, related_name="op12", on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['Roll']
