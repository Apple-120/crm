from django.db import models


 
class Employees(models.Model):
    name=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    salary=models.PositiveBigIntegerField()
    email=models.EmailField(unique=True)
    age=models.PositiveIntegerField()
    contact=models.CharField( max_length=20,null=True)
    profile_picture=models.ImageField(upload_to="images",null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    def __str__(self):
        return self.name  
    

# Create your models here.


    # to represent string rep of an object


# Create your models here.
