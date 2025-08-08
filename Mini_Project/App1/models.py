from django.db import models
from django.contrib.auth.models import User

class Employee_details(models.Model):
    merge = models.ForeignKey(User,on_delete=models.CASCADE,related_name='Emp')
    Employee_ID = models.IntegerField(unique=True)
    Photo = models.ImageField(upload_to='Employee_profile')
    Name = models.CharField(max_length=50)
    Role = models.CharField(null=True,max_length=50)
    Phone_Number = models.BigIntegerField(unique=True)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10)
    Location = models.CharField(max_length=50)

    def __str__(self):
        return self.Name

class Employee_tasks(models.Model):
    Employees= models.ForeignKey(Employee_details,on_delete=models.CASCADE,related_name='Task')
    Task = models.CharField(max_length=100)
    Status = models.CharField(max_length=50,default='Started')
    StartTime = models.DateTimeField(auto_now_add=True)
    EndTime = models.DateTimeField(null=True)

    def __str__(self):
        return self.Task
    

class Chatbox(models.Model):
    User_details = models.ForeignKey(User,on_delete=models.CASCADE,related_name='Ud') 
    Content = models.TextField()
    Date = models.DateField(auto_now=True)
    
    

    