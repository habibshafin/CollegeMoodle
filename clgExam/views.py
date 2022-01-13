import xlwt as xlwt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from collections import defaultdict
from operator import itemgetter
from tablib import Dataset
from django.contrib import messages
from django.db.models import Q

from clgStudent.views import is_admin
from .forms import CtEditForm, TermFinalEditForm, PracticalEditForm, CtMarkUpdateForm, PracticalMarkUpdateForm
from .models import Term, Exam, CT, TermFinal, Practical, TermFinalMarks, PracticalMarks, CTMarks
from clgStudent.models import Subjects, StudentInfo, StudentSubjects
from .filters import ExamFilter
from django.contrib.auth.decorators import login_required


# ----------------------------- @todo:Rafsani's Part-------------------------------


def CreateExam(request):
    if request.method != "POST":
        return render(request, "Exam.html", {})
    else:
        term = Term.objects.get(TermName=request.POST['TermName'])
        subject = Subjects.objects.get(Sub_Code=request.POST['Subject'])
        print(term.TermId)
        exam = Exam()
        exam.TermId = term
        exam.Sub_Code = subject
        grp = request.POST['Group']
        if grp == "Science":
            exam.Group = "S"
        elif grp == "Commerce":
            exam.Group = "C"
        else:
            exam.Group = "A"
        exam.Session = int(request.POST['Session'])
        ExistingData = Exam.objects.filter(Session=exam.Session, Group=exam.Group, Sub_Code=exam.Sub_Code).count()
        if ExistingData != 0:
            return HttpResponse("<h1> Exam Already Exists... Please EDIT your exam instead of CREATING</h1>")

        exam.save()
        print("EXAM ID:")
        print(exam.ExamID)

        try:
            if request.POST.get('yesct', False) == "on":
                print("CT ache")
                CtCount = int(request.POST['countCt'])
                if request.POST['ctType'] == "same":
                    for i in range(CtCount):
                        ctExam = CT()
                        ctExam.ExamID = exam
                        ctExam.TotalMarks = int(request.POST['ct1'])
                        ctExam.ctPercentage = int(request.POST['percentage1'])
                        ctExam.save()
                elif request.POST['ctType'] == "not_same":
                    for i in range(CtCount):
                        ctExam = CT()
                        ctExam.ExamID = exam
                        total = "ct" + str(i)
                        percent = "percentage" + str(i)
                        ctExam.TotalMarks = int(request.POST[total])
                        ctExam.ctPercentage = int(request.POST[percent])
                        print(ctExam.ctPercentage)
                        ctExam.save()
                    pass

            finalExam = TermFinal()
            finalExam.ExamID = exam
            finalExam.TotalMarks = int(request.POST['TermFinalMark'])
            finalExam.CQ = int(request.POST.get('TermFinalCQMark'))
            if request.POST.get('TermFinalMCQMark') != '':
                finalExam.MCQ = int(request.POST.get('TermFinalMCQMark'))
            else:
                finalExam.MCQ = 0
            finalExam.PassPercentage = int(request.POST.get('TermFinalPasspercent'))
            finalExam.TermFinalPercentage = int(request.POST.get('TermFinalPercent'))
            finalExam.save()

            if request.POST.get('yespractical', False) == "Yes":
                pracExam = Practical()
                pracExam.ExamID = exam
                pracExam.TotalMarks = int(request.POST['PracticalMark'])
                pracExam.PassMarks = int(request.POST['PracticalPassMark'])
                pracExam.PracticalPercentage = int(request.POST['Practicalpercent'])
                pracExam.save()

            print("-- {}  {}  {} ".format(exam.Session, exam.Sub_Code, exam.TermId))
            # return HttpResponse("post")
            return redirect('exam:showexam')

        except Exception as e:
            print(e)
            if exam.ExamID:
                print("DELETING ExamID:{}, SubCode:{}, Term: {}".format(exam.ExamID, exam.Sub_Code, exam.TermId))
                Exam.objects.get(ExamID=exam.ExamID).delete()
                print("EXAM DELETED SUCCESSFULLY")
                return HttpResponse("<h2> BY SOUMMA: PLEASE TRY AGAIN...THERE IS AN EXCEPTION OCCURRED </h2>")
        return HttpResponse("THERE IS AN EXCEPTION OCCURRED and EXAM ID NOT FOUND")


# ----------------------------- @todo:Anik's Part-------------------------------

@login_required(login_url='clgAdmin:login')
def ShowExam(request):
    if is_admin(request):
        exams = Exam.objects.select_related('Sub_Code', 'TermId').all().order_by('-Session', '-Group', '-TermId',
                                                                                 'Sub_Code')
        exam_filter = ExamFilter(request.GET, queryset=exams)
        return render(request, 'ShowExam.html', {'Exams': exam_filter})
    else:
        redirect('clgAdmin:login')


# ----------------------------- @todo:Shaifn's Part-------------------------------


@login_required(login_url='clgAdmin:login')
def marksheet_download(request,examid):
    if is_admin(request):
        if request.method != "POST":
            return HttpResponse('Invalid Request')
        else:
            exam = Exam.objects.select_related('Sub_Code', 'TermId').get(ExamID=examid)
            year = exam.TermId.YearStatus
            group = exam.Group
            subject = exam.Sub_Code.Sub_Code
            print(year)
            session = exam.Session % 100 + 1
            session = session * 100000

            if subject == '101' or subject == '102' or subject == '107' or subject == '108' or subject == '275' or subject == '174' or subject == '175' or subject == '176' or subject == '177' or subject == '253' or subject == '254' or subject == '277' or subject == '278':
                print('common subjects')
                student = StudentInfo.objects.filter(Roll__lte=session, YearStatus=year, Group=group).values(
                    'Roll')  # Roll of eligible students
            else:
                if group == 'S':
                    subjectType = exam.Sub_Code.ScienceType
                elif group == 'C':
                    subjectType = exam.Sub_Code.CommerceType
                else:
                    subjectType = exam.Sub_Code.ArtsType
                if subjectType == 'C':
                    student = StudentSubjects.objects.filter(Q(Roll__Roll__lte=session), Q(Roll__YearStatus=year),
                                                             Q(Roll__Group=group), (Q(comSub_11=subject) | Q(
                            comSub_12=subject) | Q(comSub_21=subject) | Q(comSub_22=subject) | Q(comSub_31=subject) | Q(
                            comSub_32=subject))).values('Roll').values('Roll')
                elif subjectType == 'O':
                    student = StudentSubjects.objects.filter(Q(Roll__Roll__lte=session), Q(Roll__YearStatus=year),
                                                             Q(Roll__Group=group),
                                                             (Q(opSub_11=subject) | Q(opSub_12=subject))).values(
                        'Roll').values('Roll')
                else:
                    print('Both')
                    student = StudentSubjects.objects.filter(Q(Roll__Roll__lte=session), Q(Roll__YearStatus=year),
                                                             Q(Roll__Group=group), (Q(comSub_11=subject) | Q(
                            comSub_12=subject) | Q(comSub_21=subject) | Q(comSub_22=subject) | Q(comSub_31=subject) | Q(
                            comSub_32=subject) | Q(opSub_11=subject) | Q(opSub_12=subject))).values('Roll').values(
                        'Roll')
                    # print('compulsory',len(student1))
                    # print('optional',len(student2))
                    '''d = defaultdict(dict)
                    for l in (student1, student2):
                        for elem in l:
                            d[elem['Roll']].update(elem)
                    student = sorted(d.values(), key=itemgetter("Roll"))'''

            if student:
                if request.POST['sheetType'] == 'TermFinal':
                    tf = TermFinal.objects.get(ExamID=exam)
                    # codes for xlx file generation
                    response = HttpResponse(content_type='application/ms-excel')
                    fname = exam.Sub_Code.Sub_Name + ' ' + exam.TermId.TermName + ' ' + 'Final.xls'
                    response['Content-Disposition'] = 'attachment; filename=%s' % fname  # sets fname as filename
                    wb = xlwt.Workbook(encoding='utf-8')
                    ws = wb.add_sheet('TermFinal', cell_overwrite_ok=True)
                    # Sheet header, first two rows(Header and full marks)

                    style = xlwt.XFStyle()
                    # backgrouund yellow and red font
                    style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
                                        'font: colour red, bold True;')
                    # Uppermost Row containing ExamDetails
                    ws.col(0).width = len(exam.TermId.TermName) * 330
                    ws.write(0, 0, exam.TermId.TermName, style)
                    ws.col(1).width = len('Term Final') * 400
                    ws.write(0, 1, 'Term Final', style)
                    ws.col(2).width = len('Sub_Code: ' + str(exam.Sub_Code.Sub_Code)) * 330
                    ws.write(0, 2, 'Sub_Code: ' + str(exam.Sub_Code.Sub_Code), style)
                    ws.col(3).width = len(exam.Sub_Code.Sub_Name) * 330
                    ws.write(0, 3, exam.Sub_Code.Sub_Name, style)
                    ws.col(4).width = len('Group: ' + exam.Group) * 330
                    ws.write(0, 4, 'Group: ' + exam.Group, style)
                    ws.col(5).width = len('Session: ' + str(exam.Session)) * 330
                    ws.write(0, 5, 'Session: ' + str(exam.Session), style)

                    # Exam and Term Final ID written for verification purpose
                    ws.write(1, 0, 'ExamID:' + str(exam.ExamID), style)
                    ws.write(1, 1, 'TermFinalID:' + str(tf.TermFinalId), style)

                    # black font
                    font_style = xlwt.XFStyle()
                    font_style.font.bold = True

                    # RollNumber||CQ||MCQ
                    row_num = 3
                    ws.write(row_num, 0, 'Roll No', font_style)
                    ws.write(row_num, 1, 'CQ', font_style)
                    if tf.MCQ != 0:
                        ws.write(row_num, 2, 'MCQ', font_style)
                    row_num = row_num + 1
                    ws.write(row_num, 0, 'Full Marks', font_style)
                    ws.write(row_num, 1, tf.CQ, font_style)
                    if tf.MCQ != 0:
                        ws.write(row_num, 2, tf.MCQ, font_style)

                    # writes student Rolls
                    for s in student:
                        row_num = row_num + 1
                        ws.write(row_num, 0, s['Roll'], font_style)

                    wb.save(response)
                    return response

                elif request.POST['sheetType'] == 'ClassTest':
                    ct = CT.objects.filter(ExamID=exam).values('ctId', 'TotalMarks')
                    cts = len(ct)  # ct counts
                    if cts != 0:
                        # codes for xlx file generation
                        response = HttpResponse(content_type='application/ms-excel')
                        fname = exam.Sub_Code.Sub_Name + ' ' + exam.TermId.TermName + ' ' + 'ClassTest.xls'
                        response['Content-Disposition'] = 'attachment; filename=%s' % fname
                        wb = xlwt.Workbook(encoding='utf-8')
                        ws = wb.add_sheet('CTMarks', cell_overwrite_ok=True)
                        # Sheet header, first row
                        style = xlwt.XFStyle()
                        # backgrouund yellow and red font
                        style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
                                            'font: colour red, bold True;')

                        ws.col(0).width = len(exam.TermId.TermName) * 330
                        ws.write(0, 0, exam.TermId.TermName, style)
                        ws.col(1).width = len('ClassTest') * 400
                        ws.write(0, 1, 'ClassTest', style)
                        ws.col(2).width = len('Sub_Code: ' + str(exam.Sub_Code.Sub_Code)) * 330
                        ws.write(0, 2, 'Sub_Code: ' + str(exam.Sub_Code.Sub_Code), style)
                        ws.col(3).width = len(exam.Sub_Code.Sub_Name) * 330
                        ws.write(0, 3, exam.Sub_Code.Sub_Name, style)
                        ws.col(4).width = len('Group: ' + exam.Group) * 330
                        ws.write(0, 4, 'Group: ' + exam.Group, style)
                        ws.col(5).width = len('Session: ' + str(exam.Session)) * 330
                        ws.write(0, 5, 'Session: ' + str(exam.Session), style)

                        # Exam and Term Final ID written for verification purpose
                        ws.write(1, 0, 'ExamID:' + str(exam.ExamID), style)
                        for i in range(cts):
                            ws.write(1, i + 1, 'ClassTestID:' + str(ct[i]['ctId']), style)

                        # black font
                        font_style = xlwt.XFStyle()
                        font_style.font.bold = True

                        row_num = 3
                        ws.write(row_num, 0, 'Roll No', font_style)
                        for i in range(cts):
                            ctstring = 'CT' + str(i + 1)
                            ws.write(row_num, i + 1, ctstring, font_style)
                        row_num = row_num + 1
                        ws.write(row_num, 0, 'Full Marks', font_style)
                        # writes full marks of CTs
                        for i in range(cts):
                            ws.write(row_num, i + 1, ct[i]['TotalMarks'], font_style)

                        for s in student:
                            row_num = row_num + 1
                            ws.write(row_num, 0, s['Roll'], font_style)

                        wb.save(response)
                        return response
                    else:
                        return HttpResponse('No CTs')

                elif request.POST['sheetType'] == 'Practical':
                    # set of dicts containing practicakid and total marks
                    pract = Practical.objects.filter(ExamID=exam).values('PracticalId', 'TotalMarks')
                    if len(pract) != 0:
                        # codes for xlx file generation
                        response = HttpResponse(content_type='application/ms-excel')
                        fname = exam.Sub_Code.Sub_Name + ' ' + exam.TermId.TermName + ' ' + 'Practical.xls'
                        response['Content-Disposition'] = 'attachment; filename=%s' % fname
                        wb = xlwt.Workbook(encoding='utf-8')
                        ws = wb.add_sheet('PracticalMarks', cell_overwrite_ok=True)
                        # backgrouund yellow and red font
                        style = xlwt.XFStyle()
                        style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
                                            'font: colour red, bold True;')

                        ws.col(0).width = len(exam.TermId.TermName) * 330
                        ws.write(0, 0, exam.TermId.TermName, style)
                        ws.col(1).width = len('Term Final') * 400
                        ws.write(0, 1, 'Term Final', style)
                        ws.col(2).width = len('Sub_Code: ' + str(exam.Sub_Code.Sub_Code)) * 330
                        ws.write(0, 2, 'Sub_Code: ' + str(exam.Sub_Code.Sub_Code), style)
                        ws.col(3).width = len(exam.Sub_Code.Sub_Name) * 330
                        ws.write(0, 3, exam.Sub_Code.Sub_Name, style)
                        ws.col(4).width = len('Group: ' + exam.Group) * 330
                        ws.write(0, 4, 'Group: ' + exam.Group, style)
                        ws.col(5).width = len('Session: ' + str(exam.Session)) * 330
                        ws.write(0, 5, 'Session: ' + str(exam.Session), style)

                        # Exam and Term Final ID written for verification purpose
                        ws.write(1, 0, 'ExamID:' + str(exam.ExamID), style)
                        ws.write(1, 1, 'PracticalID:' + str(pract[0]['PracticalId']), style)

                        # black font
                        font_style = xlwt.XFStyle()
                        font_style.font.bold = True

                        row_num = 3
                        ws.write(row_num, 0, 'Roll No', font_style)
                        ws.write(row_num, 1, 'PracticalMarks', font_style)

                        row_num = row_num + 1
                        ws.write(row_num, 0, 'Full Marks', font_style)
                        ws.write(row_num, 1, pract[0]['TotalMarks'], font_style)

                        for s in student:
                            row_num = row_num + 1
                            ws.write(row_num, 0, s['Roll'], font_style)

                        wb.save(response)
                        return response
                    else:
                        return HttpResponse('No Practical')
                else:
                    return HttpResponse('Attendance er marksheet er kaj ta kora lagbe mama')
            else:
                return HttpResponse('No Students Enrolled')

    else:
        redirect('clgAdmin:login')


# ----------------------------- @todo:Soumma's Part-------------------------------
@login_required(login_url='clgAdmin:login')
def detail_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    # print(exam.ExamID)
    print("Exam Detail fuck")
    # if exam.CTs.exists():
    #     print("CT ase mama")
    # else:
    #     print("CT nai mama")
    # exam = Exam.objects.get(ExamID=pk)
    # context = {
    #         "form":form
    #     }
    return render(request, 'examDetail.html', {'exam': exam})


# ----------------------EDIT PART---------------------------
# ----------------------EDIT PART---------------------------
@login_required(login_url='clgAdmin:login')
def edit_ct(request, pk):
    print('CT test')

    if request.method == "GET":
        # @todo: performace issue need to check
        ct = CT.objects.get(pk=pk)
        ExamEditForm = CtEditForm({'TotalMarks': ct.TotalMarks, 'Percentage': ct.ctPercentage,
                                   'isResultEntered': ct.isResultEntered})
        return render(request, 'EditExamForm.html', {"ExamEditForm": ExamEditForm})

    else:
        ExamEditForm = CtEditForm(request.POST)
        exam = CT.objects.get(pk=pk)
        if ExamEditForm.is_valid():

            exam.TotalMarks = ExamEditForm.cleaned_data['TotalMarks']
            exam.ctPercentage = ExamEditForm.cleaned_data['Percentage']
            exam.isResultEntered = ExamEditForm.cleaned_data['isResultEntered']
            exam.save()
        else:
            return HttpResponse("Vul input disos ken")
        # @todo: ct theke ----->examID ..need to check je DB te 2 times hit khai naki..performace issue
        # print(exam.ExamID.ExamID)

        return redirect('exam:detailExam', pk=exam.ExamID.ExamID)


@login_required(login_url='clgAdmin:login')
def edit_term_final(request, pk):
    if request.method == "GET":
        exam = TermFinal.objects.get(pk=pk)
        ExamEditForm = TermFinalEditForm(
            {'CQMarks': exam.CQ, 'MCQMarks': exam.MCQ, 'PassMarksPercentage': exam.PassPercentage,
             'Percentage': exam.TermFinalPercentage,
             'isResultEntered': exam.isResultEntered})
        return render(request, 'EditExamForm.html', {"ExamEditForm": ExamEditForm})

    else:
        ExamEditForm = TermFinalEditForm(request.POST)
        if ExamEditForm.is_valid():
            exam = TermFinal.objects.get(pk=pk)
            exam.CQ = ExamEditForm.cleaned_data['CQMarks']
            exam.MCQ = ExamEditForm.cleaned_data['MCQMarks']
            exam.PassPercentage = ExamEditForm.cleaned_data['PassMarksPercentage']
            exam.isResultEntered = ExamEditForm.cleaned_data['isResultEntered']
            exam.TermFinalPercentage = ExamEditForm.cleaned_data['Percentage']
            exam.save()
        else:
            return HttpResponse("Vul input disos ken")
        return redirect('exam:detailExam', pk=exam.ExamID.ExamID)


@login_required(login_url='clgAdmin:login')
def edit_practical(request, pk):
    print('edit_practical test')
    if request.method == "GET":
        exam = Practical.objects.get(pk=pk)
        ExamEditForm = PracticalEditForm({'TotalMarks': exam.TotalMarks, 'Percentage': exam.PracticalPercentage,
                                          'isResultEntered': exam.isResultEntered, 'PassMarks': exam.PassMarks})
        return render(request, 'EditExamForm.html', {"ExamEditForm": ExamEditForm})

    else:
        ExamEditForm = PracticalEditForm(request.POST)
        if ExamEditForm.is_valid():
            exam = Practical.objects.get(pk=pk)
            exam.TotalMarks = ExamEditForm.cleaned_data['TotalMarks']
            exam.PracticalPercentage = ExamEditForm.cleaned_data['Percentage']
            exam.isResultEntered = ExamEditForm.cleaned_data['isResultEntered']
            exam.PassMarks = ExamEditForm.cleaned_data['PassMarks']
            exam.save()
        else:
            return HttpResponse("Vul input disos ken")
        return redirect('exam:detailExam', pk=exam.ExamID.ExamID)


# ---------------------------DELETE PART--------------------------------
# ---------------------------DELETE PART--------------------------------
@login_required(login_url='clgAdmin:login')
def delete_ct(request, pk):
    print('CT test')
    exam = CT.objects.get(pk=pk)
    exam.delete()
    return redirect('exam:detailExam', pk=exam.ExamID.ExamID)


@login_required(login_url='clgAdmin:login')
def delete_term_final(request, pk):
    print('edit_term_final test')
    exam = TermFinal.objects.get(pk=pk)
    exam.delete()
    return redirect('exam:detailExam', pk=exam.ExamID.ExamID)


@login_required(login_url='clgAdmin:login')
def delete_practical(request, pk):
    exam = Practical.objects.get(pk=pk)
    exam.delete()
    return redirect('exam:detailExam', pk=exam.ExamID.ExamID)


@login_required(login_url='clgAdmin:login')
def delete_exam(request, pk):
    print('delete_exam test')
    Exam.objects.get(pk=pk).delete()
    return redirect('exam:showexam')


# ---------------------------MARK UPLOAD--------------------------------
# @login_required(login_url='clgAdmin:login')
def upload_mark(request,examid):
    if request.method == 'POST':
        # Nazmul er code...
        dataset = Dataset()
        newData = request.FILES['file']
        if not newData.name.endswith('xls'):
            messages.info(request, 'wrong Format')
            return redirect('exam:detailExam', pk=examid)
        imported_data = dataset.load(newData.read(), format='xls')

        if imported_data[0][0] != "" or imported_data[0][1] != "":
            # File theke exam id r tf/ct/practical esb data nissi
            FileExamData = imported_data[0][0].split(':')
            FileExamId = FileExamData[1]
            # print(FileExamId)
            FileType = imported_data[0][1].split(':')
            FileExamType = FileType[0]
            FileExamTypeId = FileType[1]
        else:
            return HttpResponse('Invalid Exam Details i.e invalid examid or tests')

        # print(FileExamTypeId)
        TrueExamId = examid

        # checking examid same kina
        if int(FileExamId) == TrueExamId:
            exam = Exam.objects.select_related('Sub_Code', 'TermId').get(ExamID=int(TrueExamId))
            year = exam.TermId.YearStatus
            group = exam.Group
            subject = exam.Sub_Code.Sub_Code
            # print(year)
            session = exam.Session % 100 + 1
            session = session * 100000

            # student is a list containing studentinfo instance of the students enrolled in the exam
            if subject == '101' or subject == '102' or subject == '107' or subject == '108' or subject == '275' or subject == '174' or subject == '175' or subject == '176' or subject == '177' or subject == '253' or subject == '254' or subject == '277' or subject == '278':
                print('common subjects')
                student = StudentInfo.objects.filter(Roll__lte=session, YearStatus=year,
                                                     Group=group)  # Roll of eligible students
            else:
                student = []
                if group == 'S':
                    subjectType = exam.Sub_Code.ScienceType
                elif group == 'C':
                    subjectType = exam.Sub_Code.CommerceType
                else:
                    subjectType = exam.Sub_Code.ArtsType
                if subjectType == 'C':
                    st = StudentSubjects.objects.select_related('Roll').filter(Q(Roll__Roll__lte=session),
                                                                               Q(Roll__YearStatus=year),
                                                                               Q(Roll__Group=group), (
                                                                                           Q(comSub_11=subject) | Q(
                                                                                       comSub_12=subject) | Q(
                                                                                       comSub_21=subject) | Q(
                                                                                       comSub_22=subject) | Q(
                                                                                       comSub_31=subject) | Q(
                                                                                       comSub_32=subject)))
                    for x in st:
                        student.append(x.Roll)
                elif subjectType == 'O':
                    st = StudentSubjects.objects.select_related('Roll').filter(Q(Roll__Roll__lte=session),
                                                                               Q(Roll__YearStatus=year),
                                                                               Q(Roll__Group=group), (
                                                                                           Q(opSub_11=subject) | Q(
                                                                                       opSub_12=subject)))
                    for x in st:
                        student.append(x.Roll)
                else:
                    # print('Both')
                    st = StudentSubjects.objects.filter(Q(Roll__Roll__lte=session), Q(Roll__YearStatus=year),
                                                        Q(Roll__Group=group), (
                                                                    Q(comSub_11=subject) | Q(comSub_12=subject) | Q(
                                                                comSub_21=subject) | Q(comSub_22=subject) | Q(
                                                                comSub_31=subject) | Q(comSub_32=subject) | Q(
                                                                opSub_11=subject) | Q(opSub_12=subject)))
                    for x in st:
                        student.append(x.Roll)

            # TermFinal Mark Upload korar jonno
            if FileExamType == 'TermFinalID':
                # print('Term Final Marks')
                tf = TermFinal.objects.get(ExamID=exam)
                if tf.TermFinalId == int(FileExamTypeId):
                    fullCQ = tf.CQ
                    fullMCQ = tf.MCQ
                    AllMarks = []

                    if imported_data[3][1] != "":
                        fCQ = int(imported_data[3][1])
                    else:
                        return HttpResponse('No CQ FullMarks Mentioned')
                    if fullMCQ != 0:
                        if imported_data[3][2] != "":
                            fMCQ = int(imported_data[3][2])
                        else:
                            return HttpResponse('No MCQ FullMarks Mentioned')
                    else:
                        fMCQ = 0

                    # full mark gula thik thak ase kina check kore dekhtesi
                    if fullCQ == fCQ and fullMCQ == fMCQ:

                        # prothom mark dhukanor jonno
                        if not tf.isResultEntered:
                            TermFinalMarksList = []
                            for i in range(4, len(imported_data)):
                                if int(imported_data[i][0]) == student[i - 4].Roll:
                                    tfMarks = TermFinalMarks()
                                    tfMarks.TermFinalId = tf
                                    tfMarks.Roll = student[i - 4]
                                    if imported_data[i][1] == "":
                                        return HttpResponse('Empty CQ Marks in Roll ' + imported_data[i][0])
                                    else:
                                        CQ = round(imported_data[i][1])
                                    MCQ = 0
                                    if imported_data[i][2] == "":
                                        return HttpResponse('Empty MCQ Marks in Roll ' + imported_data[i][0])
                                    else:
                                        if fullMCQ != 0:
                                            MCQ = round(imported_data[i][2])

                                    tfMarks.AchievedMarksMCQ = 0
                                    if CQ <= fullCQ:
                                        tfMarks.AchievedMarksCQ = CQ
                                    else:
                                        return HttpResponse(
                                            'CQ Marks greater than Full Marks in Roll ' + imported_data[i][0])
                                    if MCQ <= fullMCQ:
                                        tfMarks.AchievedMarksMCQ = MCQ
                                    else:
                                        return HttpResponse(
                                            'MCQ Marks greater than Full Marks in Roll ' + imported_data[i][0])

                                    TermFinalMarksList.append(tfMarks)
                                else:
                                    return HttpResponse(
                                        'Wrong roll number entered' + imported_data[i][0] + 'is entered where ' + str(
                                            student[i - 4].Roll) + ' is expected')
                            TermFinalMarks.objects.bulk_create(TermFinalMarksList)
                            tf.isResultEntered = True
                            tf.save()
                            return HttpResponse('Marks Saved')
                        else:
                            TermFinalMarksList = TermFinalMarks.objects.select_related('TermFinalId', 'Roll').filter(
                                TermFinalId=tf)
                            TFMList = []
                            for i in range(4, len(imported_data)):
                                if int(imported_data[i][0]) == student[i - 4].Roll:
                                    template = TermFinalMarksList[i - 4]
                                    if imported_data[i][1] == "":
                                        return HttpResponse('Empty CQ Marks in Roll ' + imported_data[i][0])
                                    else:
                                        CQ = round(imported_data[i][1])
                                    MCQ = 0
                                    if imported_data[i][2] == "":
                                        return HttpResponse('Empty MCQ Marks in Roll ' + imported_data[i][0])
                                    else:
                                        if fullMCQ != 0:
                                            MCQ = round(imported_data[i][2])

                                    if CQ != template.AchievedMarksCQ or MCQ != template.AchievedMarksMCQ:
                                        if CQ <= fullCQ:
                                            template.AchievedMarksCQ = CQ
                                        else:
                                            return HttpResponse(
                                                'CQ Marks greater than Full Marks in Roll ' + imported_data[i][0])
                                        if MCQ <= fullMCQ:
                                            template.AchievedMarksMCQ = MCQ
                                        else:
                                            return HttpResponse(
                                                'MCQ Marks greater than Full Marks in Roll ' + imported_data[i][0])
                                        TFMList.append(template)
                                else:
                                    return HttpResponse(
                                        'Wrong roll number entered' + imported_data[i][0] + 'is entered where ' + str(
                                            student[i - 4].Roll) + ' is expected')
                            if len(TFMList) > 0:
                                print('Before bulk update')
                                TermFinalMarks.objects.bulk_update(TFMList, ["AchievedMarksCQ", "AchievedMarksMCQ"])
                                print('After Bulk update')
                                return HttpResponse('Marks updated')
                            else:
                                return HttpResponse('Unchanged Marks')

                    else:
                        return HttpResponse('incorrect full marks in the File')
                else:
                    return HttpResponse('Wrong Term Final ID')

            elif FileExamType == 'PracticalID':
                # print('Practical')
                prac = Practical.objects.get(ExamID=TrueExamId)
                # print(prac.PracticalId)
                if prac.PracticalId == int(FileExamTypeId):
                    fullMarks = prac.TotalMarks
                    if imported_data[3][1] != "":
                        fMarks = int(imported_data[3][1])
                    else:
                        return HttpResponse('No Full Marks Mentioned')
                    PracticalMarksList = []
                    if fullMarks == fMarks:
                        if not prac.isResultEntered:
                            # print('First time result')
                            for i in range(4, len(imported_data)):
                                if int(imported_data[i][0]) == student[i - 4].Roll:
                                    pMarks = PracticalMarks()
                                    pMarks.PracticalId = prac
                                    pMarks.Roll = student[i - 4]
                                    if imported_data[i][1] == "":
                                        return HttpResponse('Empty Marks for Roll ' + imported_data[i][0])
                                    else:
                                        Marks = round(imported_data[i][1])
                                    if Marks <= fullMarks:
                                        pMarks.AchievedMarks = Marks
                                    else:
                                        return HttpResponse(
                                            'Wrong marks: Greater than Full Marks for Roll ' + imported_data[i][0])
                                    PracticalMarksList.append(pMarks)
                                else:
                                    return HttpResponse('Wrong roll number entered in row ' + str(i + 1))
                            PracticalMarks.objects.bulk_create(PracticalMarksList)
                            prac.isResultEntered = True
                            prac.save()
                            return HttpResponse('Practical Marks Saved')
                        else:
                            PracticalMarksList = PracticalMarks.objects.select_related('PracticalId', 'Roll').filter(
                                PracticalId=prac)
                            PMList = []
                            for i in range(4, len(imported_data)):
                                if int(imported_data[i][0]) == student[i - 4].Roll:
                                    template = PracticalMarksList[i - 4]
                                    if imported_data[i][1] == "":
                                        return HttpResponse('Empty Marks for Roll ' + imported_data[i][0])
                                    else:
                                        Marks = round(imported_data[i][1])
                                    if Marks != template.AchievedMarks:
                                        if Marks <= fullMarks:
                                            template.AchievedMarks = Marks
                                        else:
                                            return HttpResponse(
                                                'Wrong marks: Greater than Full Marks for Roll ' + imported_data[i][0])
                                        PMList.append(template)
                                else:
                                    return HttpResponse('Error in Roll Number:' + imported_data[i][0])

                            if len(PMList) > 0:
                                print('Before bulk update')
                                PracticalMarks.objects.bulk_update(PMList, ["AchievedMarks"])
                                print('After Bulk update')
                                return HttpResponse('Marks updated')
                            else:
                                return HttpResponse('Unchanged Marks')
                    else:
                        return HttpResponse('incorrect Full Marks')
                else:
                    return HttpResponse('Wrong Practical ID')
            elif FileExamType == 'ClassTestID':
                print('Class Test')
                FullMarks = []
                ct = CT.objects.filter(ExamID=exam)
                FirstTime = True
                NotAllEntered = False
                for i in range(len(ct)):
                    idFromFile = imported_data[0][i + 1].split(':')[1]
                    if int(idFromFile) != ct[i].ctId:
                        return HttpResponse('Wrong CTID ' + idFromFile)
                    FullMarks.append(ct[i].TotalMarks)
                    if ct[i].isResultEntered and FirstTime:
                        FirstTime = False
                    if not ct[i].isResultEntered:
                        NotAllEntered = True

                for i in range(len(ct)):
                    if imported_data[3][i + 1] == "":
                        return HttpResponse('Full Marks not Mentioned')
                    FileFullMark = int(imported_data[3][i + 1])
                    if FileFullMark != FullMarks[i]:
                        return HttpResponse('Wrong Full Marks Entered ')

                if FirstTime:
                    print('First Time mark upload')
                    ctMarksList = []
                    for i in range(4, len(imported_data)):
                        if int(imported_data[i][0]) == student[i - 4].Roll:
                            for j in range(len(ct)):
                                ctMarks = CTMarks()
                                ctMarks.ctId = ct[j]
                                ctMarks.Roll = student[i - 4]
                                if imported_data[i][j + 1] == "":
                                    return HttpResponse('Marks not entered for Roll ' + imported_data[i][0])
                                Marks = round(imported_data[i][j + 1])
                                if Marks <= FullMarks[j]:
                                    ctMarks.AchievedMarks = Marks
                                else:
                                    return HttpResponse(
                                        'Wrong marks: Greater than Full Marks for Roll ' + imported_data[i][0])
                                ctMarksList.append(ctMarks)
                        else:
                            return HttpResponse('Wrong roll number entered' + imported_data[i][0])

                    CTMarks.objects.bulk_create(ctMarksList)
                    CTlist = []
                    for test in ct:
                        template = test
                        template.isResultEntered = True
                        CTlist.append(template)
                    CT.objects.bulk_update(CTlist, ['isResultEntered'])
                    return HttpResponse('CT Marks Saved')

                elif NotAllEntered:
                    return HttpResponse('Some CT Marks entered previously and Some not.')
                else:
                    print('Mark update')
                    CTHistoryMarks = []
                    for i in range(len(ct)):
                        CTHistoryMarks.append(CTMarks.objects.filter(ctId=ct[i]))

                    ctMarksList = []
                    for i in range(4, len(imported_data)):
                        if int(imported_data[i][0]) == student[i - 4].Roll:
                            for j in range(len(ct)):
                                if imported_data[i][j + 1] == "":
                                    return HttpResponse(
                                        'Empty Marks field for ct' + str(j + 1) + ' in Roll' + imported_data[i][0])
                                Marks = round(imported_data[i][j + 1])
                                if Marks != CTHistoryMarks[j][i - 4].AchievedMarks:
                                    ctMarks = CTHistoryMarks[j][i - 4]
                                    ctMarks.ctId = ct[j]
                                    ctMarks.Roll = student[i - 4]
                                    if Marks <= FullMarks[j]:
                                        ctMarks.AchievedMarks = Marks
                                    else:
                                        return HttpResponse('Wrong marks: Greater than Full Marks')
                                    ctMarksList.append(ctMarks)
                        else:
                            return HttpResponse('Wrong roll number entered')

                    if len(ctMarksList) > 0:
                        CTMarks.objects.bulk_update(ctMarksList, ['AchievedMarks'])
                        return HttpResponse('Marks Updated')
                    else:
                        return HttpResponse('Unchanged marks')
        else:
            return HttpResponse('Wrong Exam Marksheets')

    else:
        return render(request, 'markupload.html')


# ----------------------Show Mark: @todo:Soumma-----------------------
@login_required(login_url='clgAdmin:login')
def ct_mark(request, pk):
    ct = get_object_or_404(CT.objects.select_related('ExamID__TermId'), pk=pk)
    marks = ct.ctmarks_set.select_related('Roll', 'ctId').all()
    # for Mark in marks:
    #     print("Roll:{} --CTmark:{}".format(Mark.Roll.Roll,Mark.AchievedMarks))
    context = {
        'ct': ct,
        'marks': marks
    }
    return render(request, 'mark/ct.html', context)


@login_required(login_url='clgAdmin:login')
def termfinal_mark(request, pk):
    # termFinal = get_object_or_404(TermFinal, pk=pk) #slow hobe jodi ami term theke exam access krte chai tokhon
    # termFinal = get_object_or_404(TermFinal.objects.select_related('ExamID'),
    #                               pk=pk)  # fast ..term relatad exam tao pick kre anbe but termID er info er jnno abar query krbe
    termFinal = get_object_or_404(TermFinal.objects.select_related('ExamID__TermId'),
                                  pk=pk)  # fastest ..1 query te term + exam anbe

    # print(termFinal)
    # print(termFinal.ExamID.TermId) #TermID print

    # ----------V2: using id of termFinal in TermFinalMarks Table directly---faster than v3---  but we need two query 1) marks 2)term and related exam info---
    # marks = TermFinalMarks.objects.select_related('Roll','TermFinalId').filter(TermFinalId=pk)
    # print(marks.TermFinalId.TermFinalId)
    # ------------V3------slow---
    # ekhane student er info access korar jnno extra query hobe,termfinal er jnno same... as select related use krinai
    # marks = termFinal.termfinalmarks_set.all()

    # ------------V4------Fastest---
    # #i dont know why eikhnane related name diye kaj krtesena...so ModelName(lowercase)_set.all() use krsi...select related use krai much faster
    marks = termFinal.termfinalmarks_set.select_related('Roll', 'TermFinalId').all()
    # print(marks)
    # for Mark in marks:
    #     print("Roll:{} --CQ:{} --MCQ:{}".format(Mark.Roll.Roll,Mark.AchievedMarksCQ,Mark.AchievedMarksMCQ))
    context = {
        'termFinal': termFinal,
        'marks': marks
    }
    return render(request, 'mark/termFinal.html', context)


@login_required(login_url='clgAdmin:login')
def practical_mark(request, pk):
    practical = get_object_or_404(Practical.objects.select_related('ExamID__TermId'), pk=pk)
    marks = practical.practicalmarks_set.select_related('Roll', 'PracticalId').all()
    context = {
        'practical': practical,
        'marks': marks
    }
    return render(request, 'mark/practical.html', context)


# ------------ update Studetnt Mark------------
@login_required(login_url='clgAdmin:login')
def update_ctmark(request, ctID, roll):
    if is_admin(request):
        if request.method == "POST":
            form = CtMarkUpdateForm(request.POST)
            print(form)
            if form.is_valid():
                CtMark_instance = get_object_or_404(CTMarks, Roll=roll, ctId=ctID)
                print(CtMark_instance.AchievedMarks)
                print(form.cleaned_data[ctID])
                return HttpResponse("Valid Form")
            else:
                return HttpResponse("Invalid Form")
        else:
            ct = get_object_or_404(CT.objects.select_related('ExamID__TermId'), pk=ctID)
            # print(ct)
            mark = ct.ctmarks_set.select_related('Roll', 'ctId').get(Roll=roll)
            # print(mark.AchievedMarks)
            form = CtMarkUpdateForm({'ctId': ct.ctId, 'AchievedMarks': mark.AchievedMarks})
            print(form)
            context = {
                'ct': ct,
                'mark': mark,
                'form': form,
            }
            return render(request, 'mark/updateCt.html', context)
    else:
        redirect('clgAdmin:login')


@login_required(login_url='clgAdmin:login')
def update_termfinal_mark(request, tfID, roll):
    if is_admin(request):
        if request.method == "POST":
            return
        else:

            context = {

            }
            return render(request, 'mark/update.html', context)
    else:
        redirect('clgAdmin:login')


@login_required(login_url='clgAdmin:login')
def update_practical_mark(request, practicalID, roll):
    if is_admin(request):
        if request.method == "POST":
            return
        else:
            practical = get_object_or_404(Practical.objects.select_related('ExamID__TermId'), pk=practicalID)
            print(practical)
            mark = practical.practicalmarks_set.select_related('Roll', 'PracticalId').get(Roll=roll)
            print(mark.AchievedMarks)
            form = CtMarkUpdateForm({'PracticalId': practical.PracticalId, 'AchievedMarks': mark.AchievedMarks})
            context = {
                'practical': practical,
                'mark': mark,
                'form': form,
            }
            return render(request, 'mark/update.html', context)
    else:
        redirect('clgAdmin:login')


#----------------------------------CT Marksheet------------------------------->
def ct_marksheet(request,pk):
    ct = CT.objects.select_related('ExamID').get(ctId=pk)
    fullMarks = ct.TotalMarks
    exam = ct.ExamID
    print('examid assigned')
    year = exam.TermId.YearStatus
    subject = exam.Sub_Code.Sub_Code
    print('year and subject found')
    group = exam.Group
    session = exam.Session % 100 + 1
    session = session * 100000

    if subject == '101' or subject == '102' or subject == '107' or subject == '108' or subject == '275' or subject == '174' or subject == '175' or subject == '176' or subject == '177' or subject == '253' or subject == '254' or subject == '277' or subject == '278':
        print('common subjects')
        student = StudentInfo.objects.filter(Roll__lte=session, YearStatus=year, Group=group).values(
            'Roll')  # Roll of eligible students
    else:
        if group == 'S':
            subjectType = exam.Sub_Code.ScienceType
        elif group == 'C':
            subjectType = exam.Sub_Code.CommerceType
        else:
            subjectType = exam.Sub_Code.ArtsType
        if subjectType == 'C':
            student = StudentSubjects.objects.filter(Q(Roll__Roll__lte=session), Q(Roll__YearStatus=year),
                                                     Q(Roll__Group=group), (Q(comSub_11=subject) | Q(
                    comSub_12=subject) | Q(comSub_21=subject) | Q(comSub_22=subject) | Q(comSub_31=subject) | Q(
                    comSub_32=subject))).values('Roll').values('Roll')
        elif subjectType == 'O':
            student = StudentSubjects.objects.filter(Q(Roll__Roll__lte=session), Q(Roll__YearStatus=year),
                                                     Q(Roll__Group=group),
                                                     (Q(opSub_11=subject) | Q(opSub_12=subject))).values(
                'Roll').values('Roll')
        else:
            print('Both')
            student = StudentSubjects.objects.filter(Q(Roll__Roll__lte=session), Q(Roll__YearStatus=year),
                                                     Q(Roll__Group=group), (Q(comSub_11=subject) | Q(
                    comSub_12=subject) | Q(comSub_21=subject) | Q(comSub_22=subject) | Q(comSub_31=subject) | Q(
                    comSub_32=subject) | Q(opSub_11=subject) | Q(opSub_12=subject))).values('Roll').values(
                'Roll')
    if len(student)>0:
        # codes for xlx file generation
        response = HttpResponse(content_type='application/ms-excel')
        fname = exam.Sub_Code.Sub_Name + ' ' + exam.TermId.TermName + ' ' + 'ClassTest.xls'
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('CTMarks', cell_overwrite_ok=True)
        # Sheet header, first row
        style = xlwt.XFStyle()
        # backgrouund yellow and red font
        style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
                            'font: colour red, bold True;')
        # black font
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        ws.col(0).width = len(exam.TermId.TermName) * 330
        ws.write(0, 0, exam.TermId.TermName, style)
        ws.col(1).width = len('ClassTest') * 440
        ws.write(0, 1, 'ClassTest', style)
        ws.col(2).width = len('Sub_Code: ' + str(exam.Sub_Code.Sub_Code)) * 330
        ws.write(0, 2, 'Sub_Code: ' + str(exam.Sub_Code.Sub_Code), style)
        ws.col(3).width = len(exam.Sub_Code.Sub_Name) * 330
        ws.write(0, 3, exam.Sub_Code.Sub_Name, style)
        ws.col(4).width = len('Group: ' + exam.Group) * 330
        ws.write(0, 4, 'Group: ' + exam.Group, style)
        ws.col(5).width = len('Session: ' + str(exam.Session)) * 330
        ws.write(0, 5, 'Session: ' + str(exam.Session), style)

        # Exam and Term Final ID written for verification purpose
        ws.write(1, 0, 'ExamID:' + str(exam.ExamID), style)
        ws.write(1, 1, 'ClassTestID:' + str(ct.ctId), style)

        row_num = 3
        ws.write(row_num, 0, 'Roll No', font_style)
        ws.write(row_num, 1, 'Marks', font_style)
        row_num = row_num + 1
        ws.write(row_num, 0, 'Full Marks', font_style)
        # writes full marks of CTs
        ws.write(row_num,  1, ct.TotalMarks, font_style)

        for s in student:
            row_num = row_num + 1
            ws.write(row_num, 0, s['Roll'], font_style)

        wb.save(response)
        return response
    else:
        return HttpResponse('No CTs')


def ct_markupload(request,pk):
    if request.method == 'POST':
        ct = CT.objects.select_related('ExamID').get(ctId=pk)
        exam = ct.ExamID

        fileInputName = 'ctfile'+str(pk)
        print(fileInputName)
        # Nazmul er code...
        dataset = Dataset()
        newData = request.FILES[fileInputName]
        if not newData.name.endswith('xls'):
            messages.info(request, 'wrong Format')
            return redirect('exam:detailExam', pk=exam.ExamID)
        imported_data = dataset.load(newData.read(), format='xls')

        if imported_data[0][0] != "" or imported_data[0][1] != "":
            # File theke exam id r tf/ct/practical esb data nissi
            FileExamData = imported_data[0][0].split(':')
            FileExamId = FileExamData[1]
            # print(FileExamId)
            FileType = imported_data[0][1].split(':')
            FileExamType = FileType[0]
            FileExamTypeId = FileType[1]
        else:
            return HttpResponse('Invalid Exam Details i.e invalid examid or tests')

        if int(FileExamId) == exam.ExamID:
            year = exam.TermId.YearStatus
            group = exam.Group
            subject = exam.Sub_Code.Sub_Code
            # print(year)
            session = exam.Session % 100 + 1
            session = session * 100000

            print('student start')
            # student is a list containing studentinfo instance of the students enrolled in the exam
            if subject == '101' or subject == '102' or subject == '107' or subject == '108' or subject == '275' or subject == '174' or subject == '175' or subject == '176' or subject == '177' or subject == '253' or subject == '254' or subject == '277' or subject == '278':
                print('common subjects')
                student = StudentInfo.objects.filter(Roll__lte=session, YearStatus=year,
                                                     Group=group)  # Roll of eligible students
            else:
                student = []
                if group == 'S':
                    subjectType = exam.Sub_Code.ScienceType
                elif group == 'C':
                    subjectType = exam.Sub_Code.CommerceType
                else:
                    subjectType = exam.Sub_Code.ArtsType
                if subjectType == 'C':
                    st = StudentSubjects.objects.select_related('Roll').filter(Q(Roll__Roll__lte=session),
                                                                               Q(Roll__YearStatus=year),
                                                                               Q(Roll__Group=group), (
                                                                                           Q(comSub_11=subject) | Q(
                                                                                       comSub_12=subject) | Q(
                                                                                       comSub_21=subject) | Q(
                                                                                       comSub_22=subject) | Q(
                                                                                       comSub_31=subject) | Q(
                                                                                       comSub_32=subject)))
                    for x in st:
                        student.append(x.Roll)
                elif subjectType == 'O':
                    st = StudentSubjects.objects.select_related('Roll').filter(Q(Roll__Roll__lte=session),
                                                                               Q(Roll__YearStatus=year),
                                                                               Q(Roll__Group=group), (
                                                                                           Q(opSub_11=subject) | Q(
                                                                                       opSub_12=subject)))
                    for x in st:
                        student.append(x.Roll)
                else:
                    # print('Both')
                    st = StudentSubjects.objects.filter(Q(Roll__Roll__lte=session), Q(Roll__YearStatus=year),
                                                        Q(Roll__Group=group), (
                                                                    Q(comSub_11=subject) | Q(comSub_12=subject) | Q(
                                                                comSub_21=subject) | Q(comSub_22=subject) | Q(
                                                                comSub_31=subject) | Q(comSub_32=subject) | Q(
                                                                opSub_11=subject) | Q(opSub_12=subject)))
                    for x in st:
                        student.append(x.Roll)
            print('student finish')
            if FileExamType == 'ClassTestID':
                print('Class Test')
                if imported_data[3][1] == "":
                    return HttpResponse('Full Marks not Mentioned')
                FileFullMark = int(imported_data[3][1])
                if FileFullMark != ct.TotalMarks:
                    return HttpResponse('Wrong Full Marks Entered ')


                if not ct.isResultEntered:
                    print('First Time mark upload')
                    ctMarksList = []
                    for i in range(4, len(imported_data)):
                        if int(imported_data[i][0]) == student[i - 4].Roll:
                            ctMarks = CTMarks()
                            ctMarks.ctId = ct
                            ctMarks.Roll = student[i - 4]
                            if imported_data[i][1] == "":
                                return HttpResponse('Marks not entered for Roll ' + imported_data[i][0])
                            Marks = round(imported_data[i][1])
                            if Marks <= ct.TotalMarks:
                                ctMarks.AchievedMarks = Marks
                            else:
                                return HttpResponse(
                                    'Wrong marks: Greater than Full Marks for Roll ' + imported_data[i][0])
                            ctMarksList.append(ctMarks)
                        else:
                            return HttpResponse('Wrong roll number entered' + imported_data[i][0])

                    CTMarks.objects.bulk_create(ctMarksList)
                    template = ct
                    template.isResultEntered = True
                    template.save()
                    return HttpResponse('CT Marks Saved')

                else:
                    print('Mark update')
                    #CTHistoryMarks= CTMarks.objects.filter(ctId=ct).iterator()

                    CTHistoryMarks= CTMarks.objects.select_related('Roll').filter(ctId=ct).only('Roll').iterator()
                    #CTHistoryRolls = CTMarks.objects.filter(ctId=ct).values('Roll','AchievedMarks')
                    #CTHistoryRolls = CTMarks.objects.filter(ctId=ct).values('Roll')
                    #CTHistoryAchievedMarks = CTMarks.objects.filter(ctId=ct).values('AchievedMarks')
                    ctMarksList = []
                    print('for loop start')
                    i=4
                    for prev_marks in CTHistoryMarks:
                        if int(imported_data[i][0]) == prev_marks.Roll.Roll:
                        #if int(imported_data[i][0]) == CTHistoryRolls[i-4]['Roll']:
                            print('checked')
                            if imported_data[i][1] == "":
                                return HttpResponse(
                                    'Empty Marks field for Roll' + imported_data[i][0])
                            Marks = round(imported_data[i][1])
                            #if Marks != prev_marks.AchievedMarks:
                            if Marks != CTHistoryRolls[i-4]['AchievedMarks']:
                                ctMarks = prev_marks
                                #ctMarks.ctId = ct
                                #ctMarks.Roll = student[i - 4]
                                if Marks <= ct.TotalMarks:
                                    ctMarks.AchievedMarks = Marks
                                else:
                                    return HttpResponse('Wrong marks: Greater than Full Marks for Roll '+imported_data[i][0])
                                ctMarksList.append(ctMarks)
                            i=i+1
                        else:
                            return HttpResponse('Wrong roll number entered '+imported_data[i][0])
                    '''for i in range(4, len(imported_data)):
                        if int(imported_data[i][0]) == CTHistoryMarks[i - 4].Roll.Roll:
                            #print('checked')
                            if imported_data[i][1] == "":
                                return HttpResponse(
                                    'Empty Marks field for Roll' + imported_data[i][0])
                            Marks = round(imported_data[i][1])
                            if Marks != CTHistoryMarks[i-4].AchievedMarks:
                                ctMarks = CTHistoryMarks[i - 4]
                                #ctMarks.ctId = ct
                                #ctMarks.Roll = student[i - 4]
                                if Marks <= ct.TotalMarks:
                                    ctMarks.AchievedMarks = Marks
                                else:
                                    return HttpResponse('Wrong marks: Greater than Full Marks for Roll '+imported_data[i][0])
                                ctMarksList.append(ctMarks)
                        else:
                            return HttpResponse('Wrong roll number entered '+imported_data[i][0])'''

                    print('for loop end')
                    if len(ctMarksList) > 0:
                        print('before bulk update')
                        CTMarks.objects.bulk_update(ctMarksList, ['AchievedMarks'])
                        return HttpResponse('Marks Updated')
                        print('after bulk update')
                    else:
                        return HttpResponse('Unchanged marks')
        else:
            return HttpResponse('Wrong Exam Marksheets')
