from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Employee_details,User,Employee_tasks,Chatbox
import random
from django.contrib.auth.models import User


def is_admin(user):
    return user.is_staff

def is_user(user):
    return not user.is_staff

def app_interface(request):
    return render(request,'App_interface.html')


def Register(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render (request,'Register.html',{'f':form})
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request,username = form.cleaned_data['username'],password = form.cleaned_data['password1'])
            login(request,user)
            request.session['Name'] = form.cleaned_data['username']
            return redirect('Ed')
        else:
            return render(request,'Register.html',{'a':form.errors,'f':form})
        
def Log_in(request):
    if request.method == 'GET':
        return render(request,'Login.html')
    else:
        Name = request.POST['name']
        Password = request.POST['password']
        Emp_id = int(request.POST['Emp_id'])
        user = authenticate(request,username = Name,password = Password)
        if user == None:
            return render (request,'Login.html',{'a':'Incorrect Username or Password'})
        else:
            try:
                get_data = Employee_details.objects.get(Employee_ID = Emp_id,merge__username = Name)
                request.session['Emp_id'] = Emp_id
                login(request,user)
                return redirect('Ui')
            except:
                return render (request,'Login.html',{'a':'Employee ID is Incorrect'})
        
@login_required      
def Emp_details(request):
    get_data = User.objects.get(username = request.session['Name'])
    Emp_id = random.randint(1000,9999)
    if request.method == 'GET':
        return render(request,'Emp_details.html', {'a':get_data,'b':Emp_id})
    else:
        Emp_id = int(request.POST.get('Emp_id'))  
        profile_pic = request.FILES.get('image')
        Name = request.POST.get('name') 
        Role = request.POST.get('role')
        Ph_num = int(request.POST.get('ph'))  
        Age = int(request.POST.get('age'))
        Gender = request.POST.get('gender')
        Location =  request.POST.get('loc')
        set_data = Employee_details(merge = get_data,Employee_ID = Emp_id,Photo = profile_pic, Name = Name,Role = Role, Phone_Number = Ph_num,Age = Age,Gender = Gender,Location = Location)
        set_data.save()
        request.session['Emp_id'] = int(Emp_id)
        return redirect('Ui')
    
@login_required
@user_passes_test(is_user,login_url='App')
def User_interface(request):
    get_data = Employee_details.objects.get(Employee_ID = int(request.session['Emp_id']))
    get_task = Employee_tasks.objects.filter(Employees__Employee_ID = request.session['Emp_id'])
    return render(request,'User_interface.html',{'a':get_data,'b':get_task})


def Admin_login(request):
    if request.method == 'GET':
        return render(request,'Admin_login.html')
    else:
        Adm_name = request.POST['name']
        Password = request.POST['pass']
        user = authenticate(request,username = Adm_name,password = Password)
        if user==None:
            return render(request,'Admin_login.html',{'a':'Password is incorrect'})
        else:
            login(request,user)
            request.session['Name'] = Adm_name
            return redirect('Ai')

@login_required
@user_passes_test(is_admin,login_url='App')
def Admin_interface(request):
    get_data = Employee_details.objects.all()
    datas = {
        'Emps':get_data,
        'Adm_Name':request.session['Name']
    }
    return render (request,'Admin_interface.html',datas)

@login_required
def View_task(request,ids):
    get_task = Employee_tasks.objects.filter(Employees__Employee_ID = int(ids))
    get_data = Employee_details.objects.get(Employee_ID = int(ids))
    datas = {
        'a': get_task,
        'b': get_data
    }
    return render (request,'View_task.html',datas)

@login_required
def Assign_task(request,ids):
    get_data =  Employee_details.objects.get(Employee_ID = int(ids))
    if request.method == 'GET':
        return render (request,'Assign_task.html',{'a':get_data})
    else:
        Id = request.POST['id']
        Task = request.POST['task']
        set_data = Employee_tasks(Employees = get_data,Task = Task)
        set_data.save()
        return render (request,'Assign_task.html',{'b':'Task assigned Successfully','a':get_data})
    
@login_required
def View_employee(request,ids):
    get_data = Employee_details.objects.get(Employee_ID = int(ids))
    return render (request,'View_employee.html',{'a':get_data})

@login_required
def Update_emp(request,ids):
    if request.method == 'GET':
        get_data = Employee_details.objects.get(Employee_ID = int(ids))
        return render(request,'Update_emp.html',{'a': get_data})
    else:
        # a1 = request.FILES.get('image')
        a2 = request.POST.get('name')
        a3 = request.POST.get('role')
        a4 = request.POST.get('ph')
        set = Employee_details.objects.get(Employee_ID = int(ids))
        # set.Photo = a1
        set.Name = a2
        set.Role = a3
        set.Phone_Number = a4
        set.save()
        return redirect('Vt',ids)
    
@login_required
def Delete_emp(request,ids):
    get = Employee_details.objects.get(Employee_ID = int(ids))
    get.delete()
    return redirect('Vt',ids)


@login_required
def Update_task(request,ids):
    if request.method == 'GET':
        get_data = Employee_tasks.objects.get(id = int(ids))
        return render(request,'Update_task.html',{'a': get_data})
    else:
        Status = request.POST['status']
        End_Time = request.POST['end_time']
        set_data = Employee_tasks.objects.get(id =int(ids))
        set_data.Status = Status
        set_data.EndTime = End_Time
        set_data.save()
        return redirect('Ui')
    

@login_required
def Overall_task(request):
    get_data = Employee_tasks.objects.all()
    return render(request,'Overall_task.html',{'a':get_data})

@login_required
def Filter_task(request,task):
    get_data = Employee_tasks.objects.filter(Task = task)
    datas = {
        'a' : get_data,
    }
    return render(request,'Filter_task.html',datas)

@login_required
def My_works(request,name):
    get_data = Employee_tasks.objects.filter(Employees__Name = name)
    return render (request,'My_works.html',{'a':get_data})

@login_required
def Chat_box(request):
    get_data = Chatbox.objects.all()
    if request.method == 'GET':
        return render(request,'Chat_box.html',{'Msgs': get_data,'CU':request.user.username})
    else:
        d1 = request.POST['chats']
        get_user = User.objects.get(username = request.user.username )
        obj = Chatbox(Content = d1,User_details = get_user)
        obj.save()
        return redirect ('Cb')
        


    

        
@login_required
def Log_out(request):
    logout(request)
    return redirect ('App')


    




