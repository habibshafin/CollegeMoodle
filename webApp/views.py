import xlwt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from passlib.hash import pbkdf2_sha256
from tablib import Dataset

from clgStudent.forms import StudentInfoForm
from clgStudent.models import StudentInfo, Subjects, StudentSubjects
from clgStudent.views import is_admin, is_student
from django.contrib import messages

'''
INSIDE THIS ARE CURRENTLY NOT IN USE AS I MIGRATE THEM IN TO OTHER APPS
-----BY SOUMMA-------------

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
        return redirect('/login')


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
                        return HttpResponse("Invalid image uploaded")

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
                return HttpResponse("<h1>invalid form</h1>")
        else:
            print('AAAA')
            form = StudentInfoForm()
            return render(request, 'student_edit_form.html', {'form': form, 'test': test})

    else:
        return redirect('/login')


def user_login(request):
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
                return redirect('/profile')
            else:
                return HttpResponse("Inactive account")
        else:
            print("failed login user {} pass {}".format(user_name, pass_word))
            return HttpResponse("!!!Invalid login info!!!")

    else:
        return render(request, 'login.html')

@login_required(login_url='/login')
def subjectChoice(request):
    if request.method == "POST":
        # @TODO:Rafsani your code here
        group = StudentInfo.objects.get(Roll=request.user.username).Group
        if group == 'S':
            if request.POST["scienceCompulsory"] != 'Select Compulsory Subject':
                print(request.POST["scienceCompulsory"])
                compulsory1 = int(request.POST["scienceCompulsory"])
                compulsory2 = compulsory1 + 1
                optional1 = int(request.POST["scienceOptional"])
                optional2 = optional1 + 1

                try:
                    student = StudentSubjects.objects.get(Roll=StudentInfo.objects.get(Roll=request.user.username))
                except StudentSubjects.DoesNotExist:
                    print('here')
                    student = StudentSubjects()
                    student.Roll = StudentInfo.objects.get(Roll=request.user.username)
                    student.save()

                physics1 = Subjects.objects.get(Sub_Code='174')
                physics2 = Subjects.objects.get(Sub_Code='175')
                chemistry1 = Subjects.objects.get(Sub_Code='176')
                chemistry2 = Subjects.objects.get(Sub_Code='177')
                com1 = Subjects.objects.get(Sub_Code=str(compulsory1))
                com2 = Subjects.objects.get(Sub_Code=str(compulsory2))
                student.Compulsory_Subjects.add(physics1)
                student.Compulsory_Subjects.add(physics2)
                student.Compulsory_Subjects.add(chemistry1)
                student.Compulsory_Subjects.add(chemistry2)
                student.Compulsory_Subjects.add(com1)
                student.Compulsory_Subjects.add(com2)
                opt1 = Subjects.objects.get(Sub_Code=str(optional1))
                opt2 = Subjects.objects.get(Sub_Code=str(optional2))
                student.Optional_Subjects.add(opt1)
                student.Optional_Subjects.add(opt2)
                student.save()

                return HttpResponse("<h1>Science Subjects saved </h1>")
            else:
                return HttpResponse("<h1>Choose wisely</h1>")
        elif group == 'C':
            if request.POST["scienceCompulsory"] != 'Select Compulsory Subject':
                compulsory1 = int(request.POST["commerceCompulsory"])
                compulsory2 = compulsory1 + 1
                print(compulsory2)
                optional1 = int(request.POST["commerceOptional"])
                optional2 = optional1 + 1

                try:
                    student = StudentSubjects.objects.get(Roll=StudentInfo.objects.get(Roll=request.user.username))
                except StudentSubjects.DoesNotExist:
                    student = StudentSubjects()
                    student.Roll = StudentInfo.objects.get(Roll=request.user.username)
                    student.save()
                physics1 = Subjects.objects.get(Sub_Code='253')
                physics2 = Subjects.objects.get(Sub_Code='254')
                chemistry1 = Subjects.objects.get(Sub_Code='277')
                chemistry2 = Subjects.objects.get(Sub_Code='278')
                com1 = Subjects.objects.get(Sub_Code=str(compulsory1))
                com2 = Subjects.objects.get(Sub_Code=str(compulsory2))
                student.Compulsory_Subjects.add(physics1)
                student.Compulsory_Subjects.add(physics2)
                student.Compulsory_Subjects.add(chemistry1)
                student.Compulsory_Subjects.add(chemistry2)
                student.Compulsory_Subjects.add(com1)
                student.Compulsory_Subjects.add(com2)
                opt1 = Subjects.objects.get(Sub_Code=str(optional1))
                opt2 = Subjects.objects.get(Sub_Code=str(optional2))
                student.Optional_Subjects.add(opt1)
                student.Optional_Subjects.add(opt2)
                student.save()
                return HttpResponse("<h1>Commerce Subject Added</h1>")
            else:
                return HttpResponse("<h1>Choose wisely</h1>")
        else:
            if len(request.POST.getlist('humanitiesCompulsary')) == 3 and len(
                    request.POST.getlist('humanitiesOptional')) == 1:
                com1 = int(request.POST.getlist('humanitiesCompulsary')[0])
                com2 = int(request.POST.getlist('humanitiesCompulsary')[1])
                com3 = int(request.POST.getlist('humanitiesCompulsary')[2])
                opt = int(request.POST.getlist('humanitiesCompulsary')[0])
                compulsory1 = Subjects.objects.get(Sub_Code=str(com1))
                compulsory2 = Subjects.objects.get(Sub_Code=str(com1 + 1))
                compulsory3 = Subjects.objects.get(Sub_Code=str(com2))
                compulsory4 = Subjects.objects.get(Sub_Code=str(com2 + 1))
                compulsory5 = Subjects.objects.get(Sub_Code=str(com3))
                compulsory6 = Subjects.objects.get(Sub_Code=str(com3 + 1))
                optional1 = Subjects.objects.get(Sub_Code=str(opt))
                optional2 = Subjects.objects.get(Sub_Code=str(opt + 1))

                try:
                    student = StudentSubjects.objects.get(Roll=StudentInfo.objects.get(Roll=request.user.username))
                except StudentSubjects.DoesNotExist:
                    student = StudentSubjects()
                    student.Roll = StudentInfo.objects.get(Roll=request.user.username)
                    student.save()
                student.Compulsory_Subjects.add(compulsory1)
                student.Compulsory_Subjects.add(compulsory2)
                student.Compulsory_Subjects.add(compulsory3)
                student.Compulsory_Subjects.add(compulsory4)
                student.Compulsory_Subjects.add(compulsory5)
                student.Compulsory_Subjects.add(compulsory6)
                student.Optional_Subjects.add(optional1)
                student.Optional_Subjects.add(optional2)
                student.save()

                return HttpResponse("<h1>Arts Subjects saved</h1>")
            else:
                return HttpResponse("<h1>Dont kid with me mate! Choose All Subjects</h1>")
    else:
        selector = StudentInfo.objects.get(Roll=request.user.username).Group
        return render(request, 'subjectChoice.html', {'selector': selector})

def load_save_student_info_form(request):
    if is_admin(request):

        if request.method == "POST":
            print('Testing Post Method')
            print(request.FILES['image'])

            form = StudentInfoForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    print('form valid')
                    test = StudentInfo()

                    # For login_test using django core User model
                    user_data = User()
                    user_data.username = form.cleaned_data['Roll']
                    user_data.set_password(form.cleaned_data['Password'])
                    user_data.email = form.cleaned_data['email']
                    user_data.save()

                    # user = authenticate(username=form.cleaned_data['Roll'],password=form.cleaned_data['Password'])
                    # # login(request,user)
                    # if user:
                    #     print("hoise")
                    # else:
                    #     print("baal")

                    # test is the studenInfo Table entry
                    test.user_ref = user_data
                    test.Name = form.cleaned_data['Name']
                    test.YearStatus = form.cleaned_data['YearStatus']
                    test.Group = form.cleaned_data['Group']
                    test.DOB = form.cleaned_data['DOB']
                    test.Father_Name = form.cleaned_data['Father_Name']
                    test.Mother_Name = form.cleaned_data['Mother_Name']
                    test.Roll = form.cleaned_data['Roll']
                    test.Guardian_Mobile_No = form.cleaned_data['Guardian_Mobile_No']
                    test.image = form.cleaned_data['image']
                    print(test.image)
                    # test.Password = make_password(form.cleaned_data['Password'])
                    test.Password = pbkdf2_sha256.encrypt(
                        form.cleaned_data['Password'], rounds=1100, salt_size=10, )
                    # to verify: pbkdf2_sha256.verify("abc", test.pw)
                    test.Sex = form.cleaned_data['Sex']
                    test.Session = form.cleaned_data['Session']

                    # LoginData is the entry for login details table
                    # LoginData = StudentLoginDetails()
                    # LoginData.Roll = form.cleaned_data['Roll']
                    # LoginData.Password = pbkdf2_sha256.encrypt(form.cleaned_data['Password'], rounds=1100, salt_size=10, )
                    # LoginData.RegisterTime =datetime.datetime.now(tz=get_current_timezone())
                    # LoginData.save()
                    test.save()
                    return redirect('/showStudent')

                except:
                    error = True
                    pass
        else:
            print('AAAA')
            form = StudentInfoForm()
            return render(request, 'form.html', {'form': form})
    else:
        return redirect('/admins')


def show_StudentInfoForm(request):
    if is_admin(request):
        students = StudentInfo.objects.all
        return render(request, 'show.html', {'students': students})
    else:
        return redirect('/admins')


def admin_login(request):
    if request.method == "POST":
        user_name = request.POST.get('id')
        pass_word = request.POST.get('pass')

        user_ref = authenticate(username=user_name, password=pass_word, )

        # print(user_ref.username)
        # print(user_ref.is_staff)
        if user_ref:
            if user_ref.is_active and user_ref.is_staff:
                login(request, user_ref)
                collegeAdmin = User.objects.get(username=user_name)
                # return render(request, 'adminDashboard.html', {'collegeAdmin': collegeAdmin})
                return redirect('/adminDashboard')
            else:
                return HttpResponse("Inactive account")
        else:
            print("failed login user {} pass {}".format(user_name, pass_word))
            return HttpResponse("!!!Invalid Admin login info!!!")

    else:
        return render(request, 'adminLogin(2).html')


@login_required(login_url='/admins')
def adminDashboard(request):
    if is_admin(request):
        collegeAdmin = User.objects.get(pk=request.user.pk)
        return render(request, 'adminDashboard.html', {'collegeAdmin': collegeAdmin})
    else:
        return redirect('/admins')


@login_required(login_url='/admins')
def addSession(request):
    if is_admin(request):

        if request.method == "POST":
            s = int(request.POST['session']) % 100
            sroll = s * 100000 + 1001
            hroll = sroll + 1000
            croll = hroll + 1000

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="rollandpass.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('rollandpass', cell_overwrite_ok=True)
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            ws.write(row_num, 0, 'Roll No', font_style)
            ws.write(row_num, 1, 'Password', font_style)
            font_style = xlwt.XFStyle()
            row_num = row_num + 1

            # Creating Sciece students
            for i in range(int(request.POST['science'])):
                # For login_test using django core User model
                # print('hello')
                user_data = User()
                user_data.username = sroll
                passw = User.objects.make_random_password(length=8)
                user_data.set_password(passw)
                user_data.save()
                info = StudentInfo()
                info.user_ref = user_data
                info.Roll = user_data.username
                info.Password = passw
                info.Group = 'S'
                info.save()
                ws.write(row_num, 0, sroll, font_style)
                ws.write(row_num, 1, passw, font_style)
                sroll = sroll + 1
                row_num = row_num + 1

            # Creating Humanities students
            for i in range(int(request.POST['humanities'])):
                # For login_test using django core User model
                user_data = User()
                user_data.username = hroll
                passw = User.objects.make_random_password(length=8)
                user_data.set_password(passw)
                user_data.save()

                info = StudentInfo()
                info.user_ref = user_data
                info.Roll = user_data.username
                info.Password = passw
                info.Group = 'A'
                info.save()

                ws.write(row_num, 0, hroll, font_style)
                ws.write(row_num, 1, passw, font_style)
                hroll = hroll + 1
                row_num = row_num + 1

            # Creating Commerce students
            for i in range(int(request.POST['commerce'])):
                # For login_test using django core User model
                user_data = User()
                user_data.username = croll
                passw = User.objects.make_random_password(length=8)
                user_data.set_password(passw)
                user_data.save()

                info = StudentInfo()
                info.user_ref = user_data
                info.Roll = user_data.username
                info.Password = passw
                info.Group = 'C'
                info.save()

                ws.write(row_num, 0, croll, font_style)
                ws.write(row_num, 1, passw, font_style)
                croll = croll + 1
                row_num = row_num + 1

            wb.save(response)
            return response

        else:
            return render(request, 'addSession.html')
    else:
        return redirect('/admins')


# @login_required(login_url='/login')
def admin_register(request):
    if is_admin(request):

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            # User.objects.create_user('john', email='lennon@thebeatles.com', password='johnpassword', is_staff=True)
            user_data = User()
            user_data.username = username
            user_data.set_password(password)
            user_data.email = email
            user_data.is_staff = True
            user_data.save()
            print('New Admin Created')
            print('UserName:' + username)
            print('Password:' + password)
            return redirect('/admins')
        else:
            print("Sending Register Requset")
            return render(request, 'adminReg.html')
    else:
        return redirect('/admins')


@login_required(login_url='/admins')
def addStudent(request):
    if is_admin(request):
        if request.method == "POST":
            session = int(request.POST.get('session')) % 100
            print(request.POST.get('session'))
            group = int(request.POST.get('group'))
            if group == 1:
                g = 'S'
            elif group == 2:
                g = 'A'
            else:
                g = 'C'
            nums = int(request.POST.get('nums'))
            roll1 = session * 100000 + group * 1000
            roll2 = roll1 + 1000
            try:
                student = StudentSubjects.objects.get(Roll=StudentInfo.objects.get(Roll=request.user.username))
                roll = student.Roll + 1
            except StudentSubjects.DoesNotExist:
                roll = roll1 + 1

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="newRegister.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('newRegister', cell_overwrite_ok=True)
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            ws.write(row_num, 0, 'Roll No', font_style)
            ws.write(row_num, 1, 'Password', font_style)
            font_style = xlwt.XFStyle()
            row_num = row_num + 1

            for i in range(nums):
                user_data = User()
                user_data.username = roll
                passw = User.objects.make_random_password(length=8)
                user_data.set_password(passw)
                user_data.save()

                info = StudentInfo()
                info.user_ref = user_data
                info.Roll = user_data.username
                info.Password = passw
                info.Group = g
                info.save()
                ws.write(row_num, 0, roll, font_style)
                ws.write(row_num, 1, passw, font_style)
                roll = roll + 1
                row_num = row_num + 1

            wb.save(response)
            return response
        else:
            return render(request, 'addStudent.html')
    else:
        return redirect('/admins')

'''


def index(request):
    print("I am index")
    # need to update

    #Checking Message
    # from django.contrib import messages
    # messages.info(request, 'This is the info message!')
    # messages.error(request, 'ERROR! ERROR!')
    # messages.success(request, 'You registered succesfully')
    messages.warning(request, 'Be careful!')

    return render(request, 'index.html')




@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    print('eikhane asche')
    return render(request, 'index.html')


def UploadExcelFile(request):
    if request.method == 'POST':
        # commonSubjectsResource=CommonSubjectsResources()
        dataset = Dataset()
        newData = request.FILES['file']
        if not newData.name.endswith('xlsx'):
            messages.info(request, 'wrong Format')
            return render(request, 'profile_upload_excel.html')
        imported_data = dataset.load(newData.read(), format='xlsx')
        # for data in imported_data:
        #    if data[0] in (None,"") and data[1] in (None,""):
        #       messages.error(request, 'None Row exist.Please insert not null row files')
        #      return render(request,'profile_upload_excel.html')
        for data in imported_data:
            print(data)
            if data[0] in (None, "") and data[1] in (None, ""):
                continue
            value = Subjects(data[0], data[1], data[2], data[3], data[4])
            value.save()
    return render(request, 'profile_upload_excel.html')




