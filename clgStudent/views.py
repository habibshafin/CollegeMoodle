from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from clgStudent.forms import StudentInfoForm
from clgStudent.models import StudentInfo, Subjects, validate_image, StudentSubjects


def is_student(request):
    if request.user.is_authenticated:
        if request.user.is_active and not request.user.is_staff:
            return True
    else:
        return False


def is_admin(request):
    if request.user.is_authenticated:
        if request.user.is_active and request.user.is_staff:
            return True
    else:
        return False


def show_student_profile(request):
    # if request.user.is_authenticated and request.user.is_active and not request.user.is_staff :
    #     student = StudentInfo.objects.get(Roll = request.user.username)
    if is_student(request):
        student = StudentInfo.objects.get(Roll=request.user.username)
        return render(request, 'studentprofile.html', {'student': student})
    else:
        return redirect('student:login')
        # return redirect('/login')


def edit_student_details(request):
    if is_student(request):
        roll = request.user.username
        test = StudentInfo.objects.get(Roll=roll)
        if request.method == "POST":
            print('Testing Post Method')
            print(request.FILES['image'])
            form = StudentInfoForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    print('form valid')

                    # test = StudentInfo()
                    test.Name = form.cleaned_data['Name']
                    test.YearStatus = form.cleaned_data['YearStatus']
                    test.Group = form.cleaned_data['Group']
                    test.DOB = form.cleaned_data['DOB']
                    test.Father_Name = form.cleaned_data['Father_Name']
                    test.Mother_Name = form.cleaned_data['Mother_Name']
                    # test.Roll = form.cleaned_data['Roll']
                    test.Guardian_Mobile_No = form.cleaned_data['Guardian_Mobile_No']
                    test.image = form.cleaned_data['image']
                    checkValidImage = validate_image(test.image)
                    if not checkValidImage:
                        return HttpResponse("<h1>Maximum size is 10kb. Please upload image < 10kb and .jpg format</h1>")

                    # print(test.image)
                    # test.Password = make_password(form.cleaned_data['Password'])
                    # test.Password = pbkdf2_sha256.encrypt(form.cleaned_data['Password'], rounds=1100, salt_size=10, )
                    # to verify: pbkdf2_sha256.verify("abc", test.pw)

                    test.Sex = form.cleaned_data['Sex']
                    test.Session = form.cleaned_data['Session']
                    print("test save hoitese")
                    test.save()
                    print("test save hoise")
                    # return redirect('/showStudent')
                    return render(request, 'studentprofile.html', {'student': test})
                except:
                    error = True
                    pass
            else:
                return HttpResponse("<h1>Iinvalid Form</h1>")
        else:
            print('Inside student profile: Sending Form to HTML')
            form = StudentInfoForm()
            return render(request, 'student_edit_form.html', {'form': form, 'student': test})

    else:
        return redirect('student:login')
        # return redirect('/login')


def student_login(request):
    if request.method == "POST":
        user_name = request.POST.get('roll')
        pass_word = request.POST.get('pass')

        user_ref = authenticate(username=request.POST.get(
            'roll'), password=request.POST.get('pass'))
        # print(user_ref.username)
        if user_ref:
            if user_ref.is_active and not user_ref.is_staff:
                login(request, user_ref)
                # student = StudentInfo.objects.get(Roll=user_name)
                if 'next' in request.POST :
                    return redirect(request.POST.get('next'))
                else :
                    return redirect('student:info')
            else:
                return HttpResponse("Inactive account")
        else:
            print("failed login user {} pass {}".format(user_name, pass_word))

            return HttpResponse("!!!Invalid login info!!!",)

    else:
        return render(request, 'login.html')


# @login_required(login_url='/login')
@login_required(login_url='student:login')
def subjectChoice(request):
    if request.method == "POST":
        s = StudentInfo.objects.get(Roll=request.user.username)
        if s.Group == 'S':
            if request.POST["scienceCompulsory"] != 'Select Compulsory Subject':
                print(request.POST["scienceCompulsory"])
                compulsory1 = int(request.POST["scienceCompulsory"])
                compulsory2 = compulsory1 + 1
                optional1 = int(request.POST["scienceOptional"])
                optional2 = optional1 + 1

                try:
                    student = StudentSubjects.objects.get(Roll=s)
                except StudentSubjects.DoesNotExist :
                    print('First time subject choice')
                    student = StudentSubjects()
                    student.Roll = s

                #To retrieve the subject Objects
                comsubcodes = ['174','175','176','177']
                comsubcodes.append(str(compulsory1))
                comsubcodes.append(str(compulsory2))
                compulsorySubs = Subjects.objects.filter(Sub_Code__in = comsubcodes)
                print('compulsory done')
                opsubs = [str(optional1),str(optional2)]
                opt = Subjects.objects.filter(Sub_Code__in=opsubs)
                print('optional done')


                '''physics1 = Subjects.objects.get(Sub_Code='174')
                physics2 = Subjects.objects.get(Sub_Code='175')
                chemistry1 = Subjects.objects.get(Sub_Code='176')
                chemistry2 = Subjects.objects.get(Sub_Code='177')
                com1 = Subjects.objects.get(Sub_Code=str(compulsory1))
                com2 = Subjects.objects.get(Sub_Code=str(compulsory2))'''
                #opt1 = Subjects.objects.get(Sub_Code=str(optional1))
                #opt2 = Subjects.objects.get(Sub_Code=str(optional2))

                '''student.comSub_11 = physics1
                student.comSub_12 = physics2
                student.comSub_21 = chemistry1
                student.comSub_22 = chemistry2
                student.comSub_31 = com1
                student.comSub_32 = com2'''
                student.comSub_11 = compulsorySubs[0]
                student.comSub_12 = compulsorySubs[1]
                student.comSub_21 = compulsorySubs[2]
                student.comSub_22 = compulsorySubs[3]
                student.comSub_31 = compulsorySubs[4]
                student.comSub_32 = compulsorySubs[5]
                student.opSub_11 = opt[0]
                student.opSub_12 = opt[1]
                student.save()

                return redirect('student:selectedSubjects')
            else:
                return HttpResponse("<h1>Choose wisely</h1>")
        elif s.Group == 'C':
            if request.POST["commerceCompulsory"] != 'Select Compulsory Subject':
                compulsory1 = int(request.POST["commerceCompulsory"])
                compulsory2 = compulsory1 + 1
                print(compulsory2)
                optional1 = int(request.POST["commerceOptional"])
                optional2 = optional1 + 1

                try:
                    student = StudentSubjects.objects.get(Roll=s)
                except StudentSubjects.DoesNotExist :
                    print('First time subject choice')
                    student = StudentSubjects()
                    student.Roll = s

                comsubcodes = ['253','254','277','278']
                comsubcodes.append(str(compulsory1))
                comsubcodes.append(str(compulsory2))
                compulsorySubs = Subjects.objects.filter(Sub_Code__in = comsubcodes)
                print('compulsory done')
                opsubs = [str(optional1),str(optional2)]
                opt = Subjects.objects.filter(Sub_Code__in=opsubs)
                print('optional done')


                '''physics1 = Subjects.objects.get(Sub_Code='253')
                physics2 = Subjects.objects.get(Sub_Code='254')
                chemistry1 = Subjects.objects.get(Sub_Code='277')
                chemistry2 = Subjects.objects.get(Sub_Code='278')
                com1 = Subjects.objects.get(Sub_Code=str(compulsory1))
                com2 = Subjects.objects.get(Sub_Code=str(compulsory2))
                opt1 = Subjects.objects.get(Sub_Code=str(optional1))
                opt2 = Subjects.objects.get(Sub_Code=str(optional2))'''
                student.comSub_11 = compulsorySubs[0]
                student.comSub_12 = compulsorySubs[1]
                student.comSub_21 = compulsorySubs[2]
                student.comSub_22 = compulsorySubs[3]
                student.comSub_31 = compulsorySubs[4]
                student.comSub_32 = compulsorySubs[5]
                student.opSub_11 = opt[0]
                student.opSub_12 = opt[1]
                student.save()
                return redirect('student:selectedSubjects')
            else:
                return HttpResponse("<h1>Choose wisely</h1>")
        else:
            if len(request.POST.getlist('humanitiesCompulsary')) == 3 and len(
                    request.POST.getlist('humanitiesOptional')) == 1:
                com1 = int(request.POST.getlist('humanitiesCompulsary')[0])
                com2 = int(request.POST.getlist('humanitiesCompulsary')[1])
                com3 = int(request.POST.getlist('humanitiesCompulsary')[2])
                opt = int(request.POST.getlist('humanitiesOptional')[0])
                '''compulsory1 = Subjects.objects.get(Sub_Code=str(com1))
                compulsory2 = Subjects.objects.get(Sub_Code=str(com1 + 1))
                compulsory3 = Subjects.objects.get(Sub_Code=str(com2))
                compulsory4 = Subjects.objects.get(Sub_Code=str(com2 + 1))
                compulsory5 = Subjects.objects.get(Sub_Code=str(com3))
                compulsory6 = Subjects.objects.get(Sub_Code=str(com3 + 1))
                optional1 = Subjects.objects.get(Sub_Code=str(opt))
                optional2 = Subjects.objects.get(Sub_Code=str(opt + 1))'''

                try:
                    student = StudentSubjects.objects.get(Roll=s)
                except StudentSubjects.DoesNotExist :
                    print('First time subject choice')
                    student = StudentSubjects()
                    student.Roll = s

                comsubcodes = [str(com1),str(com1+1),str(com2),str(com2+1),str(com3),str(com3+1)]
                compulsorySubs = Subjects.objects.filter(Sub_Code__in = comsubcodes)
                print('compulsory done')
                opsubs = [str(opt),str(opt+1)]
                opt = Subjects.objects.filter(Sub_Code__in=opsubs)
                print('optional done')


                student.comSub_11 = compulsorySubs[0]
                student.comSub_12 = compulsorySubs[1]
                student.comSub_21 = compulsorySubs[2]
                student.comSub_22 = compulsorySubs[3]
                student.comSub_31 = compulsorySubs[4]
                student.comSub_32 = compulsorySubs[5]
                student.opSub_11 = opt[0]
                student.opSub_12 = opt[1]
                student.save()

                return redirect('student:selectedSubjects')
            else:
                return HttpResponse("<h1>Dont kid with me mate! Choose All Subjects</h1>")
    else:
        selector = StudentInfo.objects.get(Roll=request.user.username).Group
        return render(request, 'subjectChoice(SBS).html', {'selector': selector})


def selected_subjects(request):
    roll = request.user.username
    # student = StudentInfo.objects.get(Roll=request.user.username) Roll=roll/student dutatei kaj hoi
    mySubjects = StudentSubjects.objects.select_related('Roll', 'comSub_11', 'comSub_12', 'comSub_21', 'comSub_31', 'comSub_32',
                                                        'opSub_11', 'opSub_12', 'comSub_22').get(Roll=roll)
    # print(mySubjects.Roll.Name)
    # print(mySubjects.comSub_11)
    # print(mySubjects.comSub_11.Sub_Name)
    # print(mySubjects.comSub_11.Sub_Code)

    # context={
    #     "com11" : {"SubCode":com11.Sub_Code, "Name":com11.Sub_Name},
    #     "com12": {"SubCode": com12.Sub_Code, "Name": com12.Sub_Name},
    #     "com21": {"SubCode": com21.Sub_Code, "Name": com21.Sub_Name},
    #     "com22": {"SubCode": com22.Sub_Code, "Name": com22.Sub_Name},
    #     "com31": {"SubCode": com31.Sub_Code, "Name": com31.Sub_Name},
    #     "com32": {"SubCode": com32.Sub_Code, "Name": com32.Sub_Name},
    #     "op11": {"SubCode": op11.Sub_Code, "Name": op11.Sub_Name},
    #     "op12": {"SubCode": op12.Sub_Code, "Name": op12.Sub_Name},
    #     "Name": mySubjects.Name
    #     "Roll": roll,
    #     "Group":
    # }
    context = {
        "studentSubs": mySubjects,
        "studentInfo": mySubjects.Roll,
    }
    return render(request, 'selectedSubjects.html', context)
    # return HttpResponse('hello')

