from django.shortcuts import render

# Create your views here.
from django.db.models import Max
from .models import user_login

def index(request):
    return render(request, './myapp/index.html')


def about(request):
    return render(request, './myapp/about.html')


def contact(request):
    return render(request, './myapp/contact.html')

def test_page(request):
    return render(request, './myapp/test.html')

######################################## Admin ###########################
def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='admin')

        if len(ul) == 1:
            request.session['admin_name'] = ul[0].uname
            request.session['admin_id'] = ul[0].id
            return render(request,'./myapp/admin_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/admin_login.html',context)


def admin_home(request):
    try:
        uname = request.session['admin_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/admin_home.html')


def admin_logout(request):
    try:
        del request.session['admin_name']
        del request.session['admin_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['admin_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='admin')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)

def admin_feature_pending(request):
    context = {'msg':'Feature not enabled'}
    return render(request, './myapp/admin_messages.html', context)

from .models import designation_type
def admin_designation_settings_add(request):
    if request.method == "POST":
        designation = request.POST.get('designation')
        dg = designation_type(designation = designation)
        dg.save()
        context = {'msg':'New Designation Added'}
        return render(request, './myapp/admin_designation_settings_add.html',context)
    else:
        return render(request, './myapp/admin_designation_settings_add.html')

def admin_designation_settings_view(request):
    designation_list = designation_type.objects.all()
    context = {'designation_list':designation_list}
    return render(request, './myapp/admin_designation_settings_view.html',context)

def admin_designation_settings_delete(request):
    id = request.GET.get('id')
    print('id = '+id)
    cg = designation_type.objects.get(id=int(id))
    cg.delete()
    msg = 'Designation Removed'

    designation_list = designation_type.objects.all()
    context = {'designation_list': designation_list, 'msg':msg}
    return render(request, './myapp/admin_designation_settings_view.html', context)

def admin_designation_settings_edit(request):
    if request.method == 'POST':
        e_id = request.POST.get('e_id')
        designation = request.POST.get('designation')
        dp = designation_type.objects.get(id=int(e_id))
        dp.designation = designation
        dp.save()

        msg = 'Designation Record Updated'
        designation_list = designation_type.objects.all()
        context = {'designation_list': designation_list, 'msg': msg}
        return render(request, './myapp/admin_designation_settings_view.html', context)
    else:
        id = request.GET.get('id')
        ds = designation_type.objects.get(id=int(id))
        context = {'designation': ds.designation, 'e_id': ds.id}
        return render(request, './myapp/admin_designation_settings_edit.html',context)


from .models import staff_details
def admin_staff_details_add(request):
    if request.method == 'POST':
        #3. staff_details - id, user_id, desg_id, fname, lname, addr, pin, email, contact, status
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        desg_id = int(request.POST.get('desg_id'))
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname = email
        #dt = datetime.today().strftime('%Y-%m-%d')
        #tm = datetime.today().strftime('%H:%M:%S')
        status = 'new'

        ul = user_login(uname=uname, passwd=password, u_type='staff')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        staff_obj = staff_details(
            user_id=user_id,fname=fname, lname=lname,
            desg_id=desg_id,addr=addr, pin=pin, contact=contact, email=email,
            status=status)

        staff_obj.save()

        print(user_id)
        context = {'msg': 'New Staff Registered'}
        return render(request, 'myapp/admin_messages.html',context)

    else:
        designation_list = designation_type.objects.all()
        context = {'designation_list': designation_list}
        return render(request, 'myapp/admin_staff_details_add.html', context)

def admin_staff_details_view(request):
    staff_list = staff_details.objects.all()
    designation_list = designation_type.objects.all()
    context = {'staff_list': staff_list,'designation_list':designation_list}
    return render(request, './myapp/admin_staff_details_view.html', context)

def admin_staff_details_delete(request):
    try:
        uname = request.session['admin_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    staff_obj = staff_details.objects.get(id=int(id))
    user_id = staff_obj.user_id
    staff_obj.delete()
    user_obj = user_login.objects.get(id=int(user_id))
    user_obj.delete()

    msg = 'Staff Record Deleted'

    staff_list = staff_details.objects.all()
    designation_list = designation_type.objects.all()
    context = {'staff_list': staff_list, 'designation_list': designation_list, 'msg':msg}
    return render(request, './myapp/admin_staff_details_view.html', context)

def admin_staff_details_edit(request):
    if request.method == 'POST':
        e_id = request.POST.get('e_id')

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        desg_id = int(request.POST.get('desg_id'))
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')

        staff_obj = staff_details.objects.get(id=int(e_id))
        staff_obj.fname = fname
        staff_obj.lname = lname
        staff_obj.desg_id = desg_id
        staff_obj.addr = addr
        staff_obj.pin = pin
        staff_obj.email = email
        staff_obj.contact = contact
        staff_obj.save()

        msg = 'Staff Record Updated'

        context = { 'msg': msg}
        return render(request, './myapp/admin_messages.html', context)
    else:
        id = request.GET.get('id')
        staff_obj = staff_details.objects.get(id=int(id))
        designation_list = designation_type.objects.all()
        context = {'staff_obj': staff_obj, 'e_id': staff_obj.id, 'designation_list':designation_list}
        return render(request, './myapp/admin_staff_details_edit.html',context)

def admin_staff_search(request):
    if request.method == 'POST':
        app_name = request.POST.get('app_name')
        filter = request.POST.get('filter')
        if filter == 'fname':
            staff_list = staff_details.objects.filter(fname__contains=app_name)
            designation_list = designation_type.objects.all()
            context = {'staff_list': staff_list, 'designation_list': designation_list}
            return render(request, './myapp/admin_staff_details_view.html', context)
        elif filter == 'lname':
            staff_list = staff_details.objects.filter(lname__contains=app_name)
            designation_list = designation_type.objects.all()
            context = {'staff_list': staff_list, 'designation_list': designation_list}
            return render(request, './myapp/admin_staff_details_view.html', context)
        else:
            staff_list = staff_details.objects.all()
            designation_list = designation_type.objects.all()
            context = {'staff_list': staff_list, 'designation_list': designation_list}
            return render(request, './myapp/admin_staff_details_view.html', context)

    else:
        return render(request, 'myapp/admin_staff_search.html')


from .models import student_details
def admin_student_details_add(request):
    if request.method == 'POST':
        #4. student_details -  id, user_id, rollno, fname, lname, dob, gender, addr, pin, email, contact, status
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        rollno = request.POST.get('rollno')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname = rollno
        #dt = datetime.today().strftime('%Y-%m-%d')
        #tm = datetime.today().strftime('%H:%M:%S')
        status = 'new'

        ul = user_login(uname=uname, passwd=password, u_type='student')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        student_obj = student_details(
            user_id=user_id,fname=fname, lname=lname, rollno=rollno,
            gender=gender, dob=dob, addr=addr, pin=pin,
            contact=contact, email=email, status=status)

        student_obj.save()

        print(user_id)
        context = {'msg': 'New Student Registered'}
        return render(request, 'myapp/admin_messages.html',context)

    else:
        context = {}
        return render(request, 'myapp/admin_student_details_add.html', context)

def admin_student_details_view(request):
    student_list = student_details.objects.all()
    context = {'student_list': student_list}
    return render(request, './myapp/admin_student_details_view.html', context)

def admin_student_details_delete(request):
    try:
        uname = request.session['admin_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    student_obj = student_details.objects.get(id=int(id))
    user_id = student_obj.user_id
    student_obj.delete()
    user_obj = user_login.objects.get(id=int(user_id))
    user_obj.delete()

    msg = 'Student Record Deleted'

    context = {'msg':msg}
    return render(request, './myapp/admin_messages.html', context)

def admin_student_details_edit(request):
    if request.method == 'POST':
        e_id = request.POST.get('e_id')
        # user_id, rollno, fname, lname, dob, gender, addr, pin, email, contact, status
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        rollno = request.POST.get('rollno')
        dob = int(request.POST.get('dob'))
        gender = int(request.POST.get('gender'))
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')

        student_obj = student_details.objects.get(id=int(e_id))
        student_obj.fname = fname
        student_obj.lname = lname
        #student_obj.rollno = rollno
        student_obj.dob = dob
        student_obj.gender = gender
        student_obj.addr = addr
        student_obj.pin = pin
        student_obj.email = email
        student_obj.contact = contact

        student_obj.save()

        msg = 'Student Record Updated'

        context = { 'msg': msg}
        return render(request, './myapp/admin_messages.html', context)
    else:
        id = request.GET.get('id')
        student_obj = student_details.objects.get(id=int(id))

        context = {'student_obj': student_obj, 'e_id': student_obj.id}
        return render(request, './myapp/admin_student_details_edit.html',context)


def admin_student_search(request):
    if request.method == 'POST':
        app_name = request.POST.get('app_name')
        filter = request.POST.get('filter')
        if filter == 'fname':
            student_list = student_details.objects.filter(fname__contains=app_name)
            context = {'student_list': student_list}
            return render(request, './myapp/admin_student_details_view.html', context)
        elif filter == 'lname':
            student_list = student_details.objects.filter(lname__contains=app_name)
            context = {'student_list': student_list}
            return render(request, './myapp/admin_student_details_view.html', context)
        elif filter == 'rollno':
            student_list = student_details.objects.filter(rollno__contains=app_name)
            context = {'student_list': student_list}
            return render(request, './myapp/admin_student_details_view.html', context)
        else:
            student_list = student_details.objects.all()
            context = {'student_list': student_list}
            return render(request, './myapp/admin_student_details_view.html', context)

    else:
        return render(request, 'myapp/admin_student_search.html')


from .models import staff_student_map
def admin_batch_student_details_add(request):
    if request.method == 'POST':
        # 5. staff_student_map - id, staff_id, student_id
        student_id= int(request.POST.get('student_id'))
        staff_id = int(request.POST.get('staff_id'))
        ud = staff_student_map(student_id=student_id,staff_id=staff_id)
        ud.save()

        print(staff_id)
        student_list = []
        student_temp_list = student_details.objects.all()
        for stud in student_temp_list:
            try:
                stud_obj = staff_student_map.objects.get(student_id=stud.user_id)
            except:
                student_list.append(stud)

        context = {'msg': 'Student Allocated','student_list':student_list,'staff_id':staff_id}
        return render(request, 'myapp/admin_batch_student_details_add.html',context)

    else:
        staff_id = int(request.GET.get('staff_id'))
        #b_m = batch.objects.get(id=batch_id)
        #student_list = student_details.objects.all()
        student_list = []
        student_temp_list = student_details.objects.all()
        for stud in student_temp_list:
            try:
                stud_obj = staff_student_map.objects.get(student_id=stud.user_id)
            except:
                student_list.append(stud)
        if len(student_list) == 0 :
            context = {'msg':'All students already allocated'}
            return render(request, 'myapp/admin_messages.html', context)

        context ={'student_list':student_list,'staff_id':staff_id}
        return render(request, 'myapp/admin_batch_student_details_add.html',context)


def admin_batch_student_details_delete(request):
    id = request.GET.get('id')
    staff_id = int(request.GET.get('staff_id'))
    print('id = '+id)
    sd = staff_student_map.objects.get(id=int(id))
    sd.delete()
    msg = 'Record Deleted'
    batch_list = staff_student_map.objects.filter(staff_id=staff_id)
    student_list = student_details.objects.all()
    context = {'student_list': student_list,'batch_list':batch_list,
               'staff_id':staff_id ,'msg':msg}
    return render(request, './myapp/admin_batch_student_details_view.html',context)


def admin_batch_student_details_view(request):
    staff_id = int(request.GET.get('staff_id'))
    batch_list = staff_student_map.objects.filter(staff_id=staff_id)
    student_list = student_details.objects.all()
    context = {'student_list': student_list, 'batch_list': batch_list,
               'staff_id': staff_id, 'msg': ''}
    return render(request, './myapp/admin_batch_student_details_view.html', context)


from .models import data_set
# data_set - id, text,type_name
def admin_dataset_add(request):
    if request.method == 'POST':

        type_name = request.POST.get('type_name')
        text = request.POST.get('text')

        dm = data_set(type_name=type_name,text=text)
        dm.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_dataset_add.html', context)
    else:
        return render(request, './myapp/admin_dataset_add.html')

def admin_dataset_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        type_name = request.POST.get('type_name')
        text = request.POST.get('text')
        dm = data_set.objects.get(id=int(s_id))
        dm.type_name = type_name
        dm.text = text
        dm.save()
        msg = 'Record Updated'
        dm_l = data_set.objects.all()
        context = {'data_list': dm_l, 'msg': msg}
        return render(request, './myapp/admin_dataset_view.html', context)
    else:
        id = request.GET.get('id')
        dm = data_set.objects.get(id=int(id))
        context = {'type_name':dm.type_name,'text':dm.text,'s_id':dm.id}
        return render(request, './myapp/admin_dataset_edit.html',context)

def admin_dataset_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    dm = data_set.objects.get(id=int(id))
    dm.delete()
    msg = 'Record Deleted'
    dm_l = data_set.objects.all()
    context = {'data_list': dm_l,'msg':msg}
    return render(request, './myapp/admin_dataset_view.html',context)

def admin_dataset_view(request):

    dm_l = data_set.objects.all()
    context = {'data_list':dm_l}
    return render(request, './myapp/admin_dataset_view.html',context)

import os
from .text_classification import TextClassification
from project.settings import BASE_DIR
# data_set - id, text,type_name

def admin_train_model(request):
    ##########training model############
    data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
    # os.remove(data_file_path)

    obj_list = data_set.objects.all()
    f = open(data_file_path, "w")
    f.write('text,label')
    f.write("\n")
    for obj in obj_list:

        f.write(f'{obj.text.replace(",", " ")},{obj.type_name}')
        f.write("\n")
    f.close()
    data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
    data_file_label_path = os.path.join(BASE_DIR, 'data/data_set_label.dat')
    tfid_file_path = os.path.join(BASE_DIR, 'data/data_set_tfid.dat')
    model_file_path = os.path.join(BASE_DIR, 'data/data_set_svm.model')

    obj = TextClassification()
    txt_result = obj.text_processing(data_file_path, data_file_label_path)
    obj.train_model(txt_result, tfid_file_path, model_file_path, 'svm')
    context = {'msg':'Training done and model created'}
    return render(request, './myapp/admin_train_model.html', context)
    ################

#######################################################################################
#################### STAFF ###############################################
def staff_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='staff')
        print(len(ul))
        if len(ul) == 1:
            request.session['staff_id'] = ul[0].id
            request.session['staff_code'] = ul[0].uname
            staff_obj = staff_details.objects.get(user_id=ul[0].id)
            context = {'uname': f'{staff_obj.fname} {staff_obj.lname}'}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/staff_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/staff_login.html',context)
    else:
        return render(request, 'myapp/staff_login.html')

def staff_home(request):
    staff_id = request.session['staff_id']
    staff_obj = staff_details.objects.get(user_id=int(staff_id))
    context = {'uname': f'{staff_obj.fname} {staff_obj.lname}'}
    return render(request,'./myapp/staff_home.html',context)
    #send_mail("heoo", "hai", '@gmail.com')

def staff_profile_view(request):
    user_id = request.session['staff_id']
    staff_obj = staff_details.objects.get(user_id=int(user_id))
    desg_list = designation_type.objects.all()
    context = {'staff_obj': staff_obj, 'e_id': staff_obj.id, 'desg_list':desg_list}
    return render(request, './myapp/staff_profile_view.html',context)

def staff_changepassword(request):
    if request.method == 'POST':
        uname = request.session['staff_code']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)
            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/staff_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/staff_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/staff_changepassword.html', context)
    else:
        return render(request, './myapp/staff_changepassword.html')

def staff_logout(request):
    try:
        del request.session['staff_code']
        del request.session['staff_id']
    except:
        return staff_login_check(request)
    else:
        return staff_login_check(request)

def staff_staff_details_view(request):
    staff_list = staff_details.objects.all()
    designation_list = designation_type.objects.all()
    context = {'staff_list': staff_list,'designation_list':designation_list}
    return render(request, './myapp/staff_staff_details_view.html', context)


def staff_feature_pending(request):
    context = {'msg':'Feature not enabled'}
    return render(request, './myapp/staff_messages.html', context)

def staff_batch_student_details_view(request):
    staff_id = int(request.session['staff_id'])
    staff_obj = staff_details.objects.get(user_id=staff_id)
    staff_id = staff_obj.id
    print(staff_id)
    batch_list = staff_student_map.objects.filter(staff_id=staff_id)
    student_list = student_details.objects.all()
    context = {'student_list': student_list, 'batch_list': batch_list,
               'staff_id': staff_id, 'msg': ''}
    return render(request, './myapp/staff_batch_student_details_view.html', context)

def staff_student_assignment_view(request):
    staff_id = int(request.session['staff_id'])
    staff_obj = staff_details.objects.get(user_id=staff_id)
    staff_id = staff_obj.id
    print(staff_id)
    batch_list = staff_student_map.objects.filter(staff_id=staff_id)
    sa_list = []
    for batch_obj in batch_list:
        student_id = batch_obj.student_id
        sa_list_temp = student_assignment.objects.filter(student_id=int(student_id))
        if len(sa_list_temp) > 0:
            sa_list.extend(sa_list_temp)
    student_list = student_details.objects.all()
    context = {'sa_list': sa_list, 'student_list': student_list, 'msg': ''}
    return render(request, 'myapp/staff_student_assignment_view.html', context)

def staff_student_assignment_pending_view(request):
    staff_id = int(request.session['staff_id'])
    staff_obj = staff_details.objects.get(user_id=staff_id)
    staff_id = staff_obj.id
    print(staff_id)
    batch_list = staff_student_map.objects.filter(staff_id=staff_id)
    sa_list = []
    for batch_obj in batch_list:
        student_id = batch_obj.student_id
        sa_list_temp = student_assignment.objects.filter(student_id=int(student_id), status='pending')
        if len(sa_list_temp) > 0:
            sa_list.extend(sa_list_temp)
    student_list = student_details.objects.all()
    context = {'sa_list': sa_list, 'student_list': student_list, 'msg': ''}
    return render(request, 'myapp/staff_student_assignment_view.html', context)

def staff_student_assignment_details_view(request):
    assignment_id = request.GET.get('assignment_id')
    sa_obj = student_assignment.objects.get(id=int(assignment_id))
    if sa_obj.type_id == 1:
        ad1_list = assignment_details_1.objects.filter(assignment_id=int(assignment_id))
        #student_list = student_details.objects.all()
        context = {'ad1_list': ad1_list,  'msg': ''}
        return render(request, 'myapp/staff_student_assignment_details_1_view.html', context)

    elif sa_obj.type_id == 2:
        ad2_list = assignment_details_2.objects.filter(assignment_id=int(assignment_id))
        # student_list = student_details.objects.all()
        context = {'ad2_list': ad2_list, 'msg': ''}
        return render(request, 'myapp/staff_student_assignment_details_2_view.html', context)

    elif sa_obj.type_id == 3:
        ad3_list = assignment_details_3.objects.filter(assignment_id=int(assignment_id))
        # student_list = student_details.objects.all()
        context = {'ad3_list': ad3_list, 'msg': ''}
        return render(request, 'myapp/staff_student_assignment_details_3_view.html', context)

    else:
        context = { 'msg': 'Invalid Details'}
        return render(request, 'myapp/student_messages.html', context)

from project.settings import BASE_DIR
import os
from .doc_support import get_url, getText
from .html_support import get_html_text
from .plag_score import compare_text
def staff_student_assignment_analysis(request):
    assignment_id = request.GET.get('assignment_id')
    sa_obj = student_assignment.objects.get(id=int(assignment_id))

    if sa_obj.type_id == 1:
        ad1_obj = assignment_details_1.objects.get(assignment_id=int(assignment_id))
        doc_file = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{ad1_obj.file}')
        doc_text = getText(doc_file)
        doc_urls = get_url(doc_file)
        url_text = ''
        for doc_url in doc_urls:
            url_text = get_html_text(doc_url)
        print(doc_text, url_text)
        #student_list = student_details.objects.all()
        data = compare_text(doc_text, url_text)
        ####################TEXT PREDICTION##############
        obj = TextClassification()
        result = obj.input_text_processing(doc_text)
        data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
        data_file_label_path = os.path.join(BASE_DIR, 'data/data_set_label.dat')
        tfid_file_path = os.path.join(BASE_DIR, 'data/data_set_tfid.dat')
        model_file_path = os.path.join(BASE_DIR, 'data/data_set_svm.model')

        model = obj.load_data(model_file_path)
        Tfidf_vect = obj.load_data(tfid_file_path)
        p = obj.get_prediction(model, result, Tfidf_vect)
        label = obj.load_data(data_file_label_path)
        label = sorted(label)
        print(f'result = {label[p[0]]}')
        final_label = label[p[0]]
        ############################
        print(data)
        d2 = list(data)
        print(d2[0][2])
        score = float(d2[0][2])*100
        ad1_obj.status = 'analysed'
        ad1_obj.analysis_score = 'Analysed Score {0:.0%}'.format(d2[0][2])
        ad1_obj.save()
        sa_obj = student_assignment.objects.get(id=int(assignment_id))
        status = ''
        if score > 65:
            status = 'Copied Content'
        elif score > 45:
            status = 'Partial Match'
        else:
            status = 'Clean'
        sa_obj.status = status + ',' + final_label
        sa_obj.save()
        context = {'msg': 'Analysed Score {0:.0%}'.format(d2[0][2])}
        return render(request, 'myapp/staff_messages.html', context)

    elif sa_obj.type_id == 2:
        ad2_obj = assignment_details_2.objects.get(assignment_id=int(assignment_id))
        doc_file = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{ad2_obj.file}')
        doc_text = getText(doc_file)
        doc_urls = ad2_obj.links.split(',')
        url_text = ''
        for doc_url in doc_urls:
            url_text = get_html_text(doc_url)
        print(doc_text, url_text)
        data = compare_text(doc_text, url_text)
        ####################TEXT PREDICTION##############
        obj = TextClassification()
        result = obj.input_text_processing(doc_text)
        data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
        data_file_label_path = os.path.join(BASE_DIR, 'data/data_set_label.dat')
        tfid_file_path = os.path.join(BASE_DIR, 'data/data_set_tfid.dat')
        model_file_path = os.path.join(BASE_DIR, 'data/data_set_svm.model')

        model = obj.load_data(model_file_path)
        Tfidf_vect = obj.load_data(tfid_file_path)
        p = obj.get_prediction(model, result, Tfidf_vect)
        label = obj.load_data(data_file_label_path)
        label = sorted(label)
        print(f'result = {label[p[0]]}')
        final_label = label[p[0]]
        ############################
        print(data)
        d2 = list(data)
        print(d2[0][2])
        score = float(d2[0][2]) * 100
        ad2_obj.status = 'analysed'
        ad2_obj.analysis_score = 'Analysed Score {0:.0%}'.format(d2[0][2])
        ad2_obj.save()
        sa_obj = student_assignment.objects.get(id=int(assignment_id))
        status = ''
        if score > 65:
            status = 'Copied Content'
        elif score > 45:
            status = 'Partial Match'
        else:
            status = 'Clean'
        sa_obj.status = status + ',' + final_label
        sa_obj.save()

        context = {'msg': 'Analysed Score {0:.0%}'.format(d2[0][2])}
        return render(request, 'myapp/staff_messages.html', context)

    elif sa_obj.type_id == 3:
        ad3_obj = assignment_details_3.objects.get(assignment_id=int(assignment_id))

        doc_text = ad3_obj.content
        url_text = ad3_obj.links_content
        data = compare_text(doc_text, url_text)
        ####################TEXT PREDICTION##############
        obj = TextClassification()
        result = obj.input_text_processing(doc_text)
        data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
        data_file_label_path = os.path.join(BASE_DIR, 'data/data_set_label.dat')
        tfid_file_path = os.path.join(BASE_DIR, 'data/data_set_tfid.dat')
        model_file_path = os.path.join(BASE_DIR, 'data/data_set_svm.model')

        model = obj.load_data(model_file_path)
        Tfidf_vect = obj.load_data(tfid_file_path)
        p = obj.get_prediction(model, result, Tfidf_vect)
        label = obj.load_data(data_file_label_path)
        label = sorted(label)
        print(f'result = {label[p[0]]}')
        final_label = label[p[0]]
        ############################
        print(data)
        d2 = list(data)
        print(d2[0][2])
        score = float(d2[0][2]) * 100


        ad3_obj.status = 'analysed'
        ad3_obj.analysis_score = 'Analysed Score {0:.0%}'.format(d2[0][2])
        ad3_obj.save()
        sa_obj = student_assignment.objects.get(id=int(assignment_id))
        status = ''
        if score > 65:
            status = 'Copied Content'
        elif score > 45:
            status = 'Partial Match'
        else:
            status = 'Clean'
        sa_obj.status = status + ',' + final_label
        sa_obj.save()

        context = {'msg': 'Analysed Score {0:.0%}'.format(d2[0][2])}
        return render(request, 'myapp/staff_messages.html', context)
    else:
        context = { 'msg': 'Invalid Details'}
        return render(request, 'myapp/student_messages.html', context)

from .models import staff_messages
#6. staff_messages - id, staff_id, sub, msg, dt, tm, status
def staff_messages_add(request):
    if request.method == 'POST':

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        sub = request.POST.get('sub')
        msg = request.POST.get('msg')

        staff_id=int(request.session['staff_id'])
        ####################
        sm_obj = staff_messages(staff_id=staff_id,sub=sub, msg=msg, dt=dt, tm=tm,status='new')
        sm_obj.save()
        context = {'msg': 'Message posted'}
        return render(request, 'myapp/staff_messages.html', context)
    else:

        context = {}

        return render(request, 'myapp/staff_messages_add.html',context)

def staff_messages_delete(request):
    id = request.GET.get('id')
    print("id=" + id)
    sm_obj = staff_messages.objects.get(id=int(id))
    sm_obj.delete()

    staff_id = int(request.session['staff_id'])
    sm_list = staff_messages.objects.filter(staff_id=staff_id)
    staff_list = staff_details.objects.all()

    context = {'message_list': sm_list, 'staff_list': staff_list,'msg':'Deleted'}
    return render(request, 'myapp/staff_messages_view.html', context)

def staff_messages_view(request):
    staff_id = int(request.session['staff_id'])
    sm_list = staff_messages.objects.filter(staff_id=staff_id)
    staff_list = staff_details.objects.all()

    context = {'message_list': sm_list, 'staff_list': staff_list,'msg':''}
    return render(request, 'myapp/staff_messages_view.html', context)

#########################################################################################
############################ STUDENT ##################################################
def student_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')
        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='student')
        print(len(ul))
        if len(ul) == 1:
            request.session['student_id'] = ul[0].id
            request.session['adm_no'] = ul[0].uname
            student_obj = student_details.objects.get(user_id=ul[0].id)
            context = {'uname': f'{student_obj.fname} {student_obj.lname}'}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/student_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/student_login.html',context)
    else:
        return render(request, 'myapp/student_login.html')


def student_home(request):
    student_id = request.session['student_id']
    student_obj = student_details.objects.get(user_id=int(student_id))
    context = {'uname': f'{student_obj.fname} {student_obj.lname}' }
    return render(request,'./myapp/student_home.html',context)
    #send_mail("heoo", "hai", '@gmail.com')

def student_changepassword(request):
    if request.method == 'POST':
        uname = request.session['adm_no']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))
        try:
            ul = user_login.objects.get(uname=uname, passwd=current_password)
            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/student_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/student_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/student_changepassword.html', context)
    else:
        return render(request, './myapp/student_changepassword.html')


def student_logout(request):
    try:
        del request.session['adm_no']
        del request.session['student_id']

    except:
        return student_login_check(request)
    else:
        return student_login_check(request)

def student_profile_view(request):
    user_id = request.session['student_id']
    student_obj = student_details.objects.get(user_id=int(user_id))
    context = {'student_obj': student_obj, 'e_id': student_obj.id}
    return render(request, './myapp/student_profile_view.html',context)



from .models import student_assignment, assignment_details_1
from django.core.files.storage import FileSystemStorage
from datetime import datetime
#8. assignment_details_1 - id, assignment_id, file, analysis_score, status
#7. student_assignment - id, student_id, title, remarks, dt, tm, type_id, status
def student_assignment_details_1_add(request):
    if request.method == 'POST':
        student_id = request.session['student_id']
        title = request.POST.get('title')
        remarks = request.POST.get('remarks')
        type_id = 1
        status = 'pending'
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)

        file= file_path
        analysis_score = '0.0'

        sa_obj = student_assignment(student_id=int(student_id),title=title,
                                remarks=remarks, dt=dt,tm=tm, type_id=type_id, status=status)
        sa_obj.save()

        assignment_id = student_assignment.objects.all().aggregate(Max('id'))['id__max']

        ad1_obj = assignment_details_1(assignment_id=assignment_id, file=file,
                                    analysis_score=analysis_score, status=status)
        ad1_obj.save()
        context = {'msg':'Assignment Submitted'}
        return render(request, 'myapp/student_messages.html',context)

    else:

        context = {'msg':''}
        return render(request, 'myapp/student_assignment_details_1_add.html',context)

# def official_safe_house_pics_delete(request):
#     id = request.GET.get('id')
#     house_id = request.GET.get('house_id')
#     print("id="+id)
#     pp = safe_house_pics.objects.get(id=int(id))
#     pp.delete()
#
#     pp_l = safe_house_pics.objects.filter(house_id=int(house_id))
#     context ={'pic_list':pp_l,'house_id': house_id,'msg':'Picture deleted'}
#     return render(request,'myapp/official_safe_house_pics_view.html',context)

def student_assignment_view(request):
    student_id = request.session['student_id']
    sa_list = student_assignment.objects.filter(student_id=int(student_id))
    student_list = student_details.objects.all()
    context = {'sa_list': sa_list, 'student_list': student_list, 'msg': ''}
    return render(request, 'myapp/student_assignment_view.html', context)

def student_assignment_details_view(request):
    assignment_id = request.GET.get('assignment_id')
    sa_obj = student_assignment.objects.get(id=int(assignment_id))
    if sa_obj.type_id == 1:
        ad1_list = assignment_details_1.objects.filter(assignment_id=int(assignment_id))
        #student_list = student_details.objects.all()
        context = {'ad1_list': ad1_list,  'msg': ''}
        return render(request, 'myapp/student_assignment_details_1_view.html', context)

    elif sa_obj.type_id == 2:
        ad2_list = assignment_details_2.objects.filter(assignment_id=int(assignment_id))
        # student_list = student_details.objects.all()
        context = {'ad2_list': ad2_list, 'msg': ''}
        return render(request, 'myapp/student_assignment_details_2_view.html', context)

    elif sa_obj.type_id == 3:
        ad3_list = assignment_details_3.objects.filter(assignment_id=int(assignment_id))
        # student_list = student_details.objects.all()
        context = {'ad3_list': ad3_list, 'msg': ''}
        return render(request, 'myapp/student_assignment_details_3_view.html', context)

    else:
        context = { 'msg': 'Invalid Details'}
        return render(request, 'myapp/student_messages.html', context)

from .models import assignment_details_2
#9. assignment_details_2 - id, assignment_id, file, links, analysis_score, status
def student_assignment_details_2_add(request):
    if request.method == 'POST':
        student_id = request.session['student_id']
        title = request.POST.get('title')
        remarks = request.POST.get('remarks')
        type_id = 2
        status = 'pending'
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)

        file= file_path
        analysis_score = '0.0'
        links = request.POST.get('links')
        sa_obj = student_assignment(student_id=int(student_id),title=title,
                                remarks=remarks, dt=dt,tm=tm, type_id=type_id, status=status)
        sa_obj.save()

        assignment_id = student_assignment.objects.all().aggregate(Max('id'))['id__max']

        ad1_obj = assignment_details_2(assignment_id=assignment_id, file=file,
                                       links=links, analysis_score=analysis_score,
                                       status=status)
        ad1_obj.save()
        context = {'msg':'Assignment Submitted'}
        return render(request, 'myapp/student_messages.html',context)

    else:

        context = {'msg':''}
        return render(request, 'myapp/student_assignment_details_2_add.html',context)

from .models import assignment_details_3
#10. assignment_details_3 - id, assignment_id, content, links_content, analysis_score, status
def student_assignment_details_3_add(request):
    if request.method == 'POST':
        student_id = request.session['student_id']
        title = request.POST.get('title')
        remarks = request.POST.get('remarks')
        type_id = 3
        status = 'pending'
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        #uploaded_file = request.FILES['document']
        #fs = FileSystemStorage()
        #file_path = fs.save(uploaded_file.name, uploaded_file)

        #file= file_path
        analysis_score = '0.0'
        content = request.POST.get('content')
        links_content = request.POST.get('links_content')
        sa_obj = student_assignment(student_id=int(student_id),title=title,
                                remarks=remarks, dt=dt,tm=tm, type_id=type_id, status=status)
        sa_obj.save()

        assignment_id = student_assignment.objects.all().aggregate(Max('id'))['id__max']

        ad1_obj = assignment_details_3(assignment_id=assignment_id, content=content,
                                       links_content=links_content, analysis_score=analysis_score,
                                       status=status)
        ad1_obj.save()
        context = {'msg':'Assignment Submitted'}
        return render(request, 'myapp/student_messages.html',context)

    else:

        context = {'msg':''}
        return render(request, 'myapp/student_assignment_details_3_add.html',context)


def student_staff_messages_view(request):
    student_id = int(request.session['student_id'])
    ssm_obj = staff_student_map.objects.get(student_id=student_id)
    sd_obj = staff_details.objects.get(id=ssm_obj.staff_id)
    staff_id = sd_obj.user_id
    sm_list = staff_messages.objects.filter(staff_id=staff_id)
    staff_list = staff_details.objects.all()

    context = {'message_list': sm_list, 'staff_list': staff_list,'msg':''}
    return render(request, 'myapp/student_staff_messages_view.html', context)


def student_staff_details_view(request):
    student_id = int(request.session['student_id'])
    ssm_obj = staff_student_map.objects.get(student_id=student_id)

    staff_list = staff_details.objects.filter(id=ssm_obj.staff_id)
    designation_list = designation_type.objects.all()
    context = {'staff_list': staff_list,'designation_list':designation_list}
    return render(request, './myapp/student_staff_details_view.html', context)

#####################################################################################
################################## UNUSED ############################################
from .models import user_details

def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/user_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)
    #send_mail("heoo", "hai", 'snehadavisk@gmail.com')

def user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        gender = request.POST.get('gender')
        age = request.POST.get('age')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname=email
        #status = "new"

        ul = user_login(uname=uname, passwd=password, u_type='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id,fname=fname, lname=lname, gender=gender, age=age,addr=addr, pin=pin, contact=contact, email=email )
        ud.save()

        print(user_id)
        context = {'msg': 'User Registered'}
        return render(request, 'myapp/user_login.html',context)

    else:
        return render(request, 'myapp/user_details_add.html')

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)

            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/user_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/user_changepassword.html', context)
    else:
        return render(request, './myapp/user_changepassword.html')



def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)


########################################################
def test_doc(request):
    return render(request, './myapp/doc.html')

