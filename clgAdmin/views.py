import xlwt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from clgStudent.views import is_admin
from clgStudent.models import StudentInfo, StudentSubjects
from clgStudent.forms import StudentInfoForm
from passlib.hash import pbkdf2_sha256
from .filters import StudentFilter


def admin_login(request):
    if request.method == "POST":
        user_name = request.POST.get('id')
        pass_word = request.POST.get('pass')

        user_ref = authenticate(username=user_name, password=pass_word, )

        if user_ref:
            if user_ref.is_active and user_ref.is_staff:
                login(request, user_ref)
                collegeAdmin = User.objects.get(username=user_name)
                # return render(request, 'adminDashboard.html', {'collegeAdmin': collegeAdmin})
                # return redirect('/adminDashboard')
                if 'next' in request.POST :
                    return redirect(request.POST.get('next'))
                else :
                    return redirect('clgAdmin:dashboard')
            else:
                return HttpResponse("Inactive account")
        else:
            print("failed login user {} pass {}".format(user_name, pass_word))
            return HttpResponse("!!!Invalid Admin login info!!!")

    else:
        return render(request, 'adminLogin(2).html')


@login_required(login_url='clgAdmin:login')
def add_new_student(request):
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
                    # return redirect('/showStudent')
                    return redirect('clgAdmin:studentList')
                except:
                    error = True
                    pass
        else:
            print('Inside Admin: Creating Add New Student Form')
            form = StudentInfoForm()
            return render(request, 'AddStudentForm.html', {'form': form})
    else:
        redirect('clgAdmin:login')
        # return redirect('/login')

@login_required(login_url='clgAdmin:login')
def add_admin(request):
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
            return redirect('clgAdmin:login')
        else:
            print("Sending Register Requset")
            return render(request, 'AddAdminForm.html')
    else:
        redirect('clgAdmin:login')
        # return redirect('/admins')


# @login_required(login_url='/admins')
@login_required(login_url='clgAdmin:login')
def admin_dashboard(request):
    if is_admin(request):
        collegeAdmin = User.objects.get(pk=request.user.pk)
        return render(request, 'adminDashboard.html', {'collegeAdmin': collegeAdmin})
    else:
        redirect('clgAdmin:login')
        # return redirect('/admins')


@login_required(login_url='clgAdmin:login')
def student_list(request):
    if is_admin(request):
        students = StudentInfo.objects.all()
        std_filter = StudentFilter(request.GET, queryset=students)
        return render(request, 'studentList.html', {'students': std_filter})
    else:
        redirect('clgAdmin:login')
        # return redirect('/admins')


# @login_required(login_url='/admins')
@login_required(login_url='clgAdmin:login')
def add_new_session(request):
    if is_admin(request):

        if request.method == "POST":
            s = int(request.POST['session']) % 100
            sroll = s * 100000 + 1001
            hroll = sroll + 1000
            croll = hroll + 1000

            StudentList = []
            UserList = []

            response = HttpResponse(content_type='application/ms-excel')
            fname = 'New Session '+ request.POST['session']+'.xls'
            response['Content-Disposition'] = 'attachment; filename=%s' % fname  # sets fname as filename
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('rollandpass', cell_overwrite_ok=True)
            # Sheet header, first row

            style = xlwt.XFStyle()
            style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
                                'font: colour red, bold True;')

            ws.col(0).width = len('Science Group') * 330
            ws.write(0, 0, 'Science Group' , style)
            ws.col(1).width = len('Password  ') * 330
            row_num = 1
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            ws.write(row_num, 0, 'Roll No', font_style)
            ws.write(row_num, 1, 'Password', font_style)
            font_style = xlwt.XFStyle()
            row_num = row_num + 1

            rollStart = sroll-1

            # Creating Sciece students
            for i in range(int(request.POST['science'])):
                # For login_test using django core User model
                # print('hello')
                user_data = User()
                user_data.username = sroll
                passw = User.objects.make_random_password(length=8)
                user_data.set_password(passw)
                #user_data.save()
                UserList.append(user_data)
                info = StudentInfo()
                #info.user_ref = UserList[counter]
                #counter = counter+1
                info.Roll = user_data.username
                info.Password = passw
                info.Group = 'S'
                info.Session = int(request.POST['session'])
                #info.save()
                StudentList.append(info)

                ws.write(row_num, 0, sroll, font_style)
                ws.write(row_num, 1, passw, font_style)
                sroll = sroll + 1
                row_num = row_num + 1

            row_num = row_num + 2
            ws.write(row_num, 0, 'Humanities Group' , style)
            row_num = row_num + 1
            ws.write(row_num, 0, 'Roll No', font_style)
            ws.write(row_num, 1, 'Password', font_style)
            row_num = row_num + 1

            # Creating Humanities students
            for i in range(int(request.POST['humanities'])):
                # For login_test using django core User model
                user_data = User()
                user_data.username = hroll
                passw = User.objects.make_random_password(length=8)
                user_data.set_password(passw)
                #user_data.save()
                UserList.append(user_data)
                info = StudentInfo()
                #info.user_ref = user_data
                info.Roll = user_data.username
                info.Password = passw
                info.Group = 'A'
                info.Session = int(request.POST['session'])
                #info.save()
                StudentList.append(info)


                ws.write(row_num, 0, hroll, font_style)
                ws.write(row_num, 1, passw, font_style)
                hroll = hroll + 1
                row_num = row_num + 1

            row_num = row_num + 2
            ws.write(row_num, 0, 'Commerce Group' , style)
            row_num = row_num + 1
            ws.write(row_num, 0, 'Roll No', font_style)
            ws.write(row_num, 1, 'Password', font_style)
            row_num = row_num + 1

            # Creating Commerce students
            for i in range(int(request.POST['commerce'])):
                # For login_test using django core User model
                user_data = User()
                user_data.username = croll
                passw = User.objects.make_random_password(length=8)
                user_data.set_password(passw)
                #user_data.save()
                UserList.append(user_data)
                info = StudentInfo()
                #info.user_ref = UserList[counter]
                #counter = counter+1
                info.Roll = user_data.username
                info.Password = passw
                info.Group = 'C'
                info.Session = int(request.POST['session'])
                #info.save()
                StudentList.append(info)

                ws.write(row_num, 0, croll, font_style)
                ws.write(row_num, 1, passw, font_style)
                croll = croll + 1
                row_num = row_num + 1

            finishroll = croll + 1

            User.objects.bulk_create(UserList)
            users = User.objects.filter(username__gte=rollStart,username__lte = finishroll).order_by('username')
            iter =0;
            for u in users:
                StudentList[iter].user_ref = u
                iter = iter + 1
                print(u.username)
            StudentInfo.objects.bulk_create(StudentList)

            wb.save(response)
            return response

        else:
            return render(request, 'addNewSession.html')
    else:
        redirect('clgAdmin:login')
        # return redirect('/admins')


@login_required(login_url='clgAdmin:login')
def add_in_previous_session(request):
    if is_admin(request):
        if request.method == "POST":
            session = int(request.POST.get('session')) % 100
            group = int(request.POST.get('group'))
            yearstatus = int(request.POST.get('YearStatus'))
            if group == 1:
                g = 'S'
            elif group == 2:
                g = 'A'
            else:
                g = 'C'
            nums = int(request.POST.get('nums'))
            roll1 = session * 100000 + group * 1000
            roll2 = roll1 + 1000

            student = StudentInfo.objects.filter(Roll__gte = roll1, Roll__lte = roll2 ).order_by('-Roll').first()

            if not student:
                roll = roll1 + 1
            else:
                roll = student.Roll + 1
            rollStart = roll
            #print(roll)
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

            UserList = []
            StudentList = []

            for i in range(nums):
                user_data = User()
                user_data.username = roll
                passw = User.objects.make_random_password(length=8)
                user_data.set_password(passw)
                #user_data.save()
                UserList.append(user_data)

                info = StudentInfo()
                #info.user_ref = user_data
                info.Roll = user_data.username
                info.Password = passw
                info.Group = g
                info.YearStatus = yearstatus
                info.Session = int(request.POST.get('session'))
                StudentList.append(info)

                #info.save()
                ws.write(row_num, 0, roll, font_style)
                ws.write(row_num, 1, passw, font_style)
                roll = roll + 1
                row_num = row_num + 1

            User.objects.bulk_create(UserList)
            users = User.objects.filter(username__gte=rollStart,username__lte = roll).order_by('username')
            iter =0;
            for u in users:
                StudentList[iter].user_ref = u
                iter = iter + 1
                print(u.username)
            StudentInfo.objects.bulk_create(StudentList)

            wb.save(response)
            return response
        else:
            return render(request, 'addPreSession.html')
    else:
        redirect('clgAdmin:login')
        # return redirect('/admins')

@login_required(login_url='clgAdmin:login')
def download_student_password(request):
    if is_admin(request):
        if request.method == "POST":
            if request.POST['Clicked']=='Session':
                session = request.POST['session']
                Studentdata = StudentInfo.objects.filter(Session = session).values('Roll','Password')

                if len(Studentdata) >0:
                    response = HttpResponse(content_type='application/ms-excel')
                    fname = str(session) + '.xls'
                    response['Content-Disposition'] = 'attachment; filename=%s' %fname
                    wb = xlwt.Workbook(encoding='utf-8')
                    ws = wb.add_sheet('rollandpass', cell_overwrite_ok=True)
                    # Sheet header, first row
                    row_num = 0
                    font_style = xlwt.XFStyle()
                    font_style.font.bold = True
                    ws.write(row_num, 0, 'Roll No', font_style)
                    ws.write(row_num, 1, 'Password', font_style)
                    font_style = xlwt.XFStyle()

                    for s in Studentdata:
                        row_num = row_num + 1
                        ws.write(row_num, 0, s['Roll'], font_style)
                        ws.write(row_num, 1, s['Password'], font_style)

                    wb.save(response)
                    return response
                else :
                    errortxt = 'No Students Enrolled in the session'
                    return render(request, 'DownloadStudentPassword.html',{'errortxt': errortxt})

            else :
                roll = int(request.POST['roll'])

                passw = StudentInfo.objects.filter(Roll=roll).values('Password')
                if len(passw)!=0:
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

                    ws.write(1, 0, roll , font_style)
                    ws.write(1, 1, passw[0]['Password'] , font_style)

                    wb.save(response)
                    return response
                else:
                    errortxt = 'Invalid Roll Number'
                    return render(request, 'DownloadStudentPassword.html',{'errortxt': errortxt})

        else:
            return render(request, 'DownloadStudentPassword.html')
    else:
        redirect('clgAdmin:login')


# def edit_student(request):
