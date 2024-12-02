from django.db import models
from django.db import connection
from django.contrib.auth.models import User

class SignUp(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.email

class registration_details(models.Model):
    id = models.AutoField(primary_key=True)
    email=models.EmailField(unique=True,default="")
    company_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_development_stage= models.CharField(max_length=100)
    sales= models.CharField(max_length=100)
    unique_selling_proposition = models.CharField(max_length=100)
    website = models.URLField()
    instagram = models.URLField()
    twitter = models.URLField()
    product_photo = models.ImageField(upload_to='static/media/img/product_photos/')
    product_video = models.FileField(upload_to='static/media/img/product_videos/')
    
    def __str__(self):
        return self.company_name
    
class EliminatedUser_Round1(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
     
class Round2_users(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_development_stage = models.CharField(max_length=100)
    sales= models.CharField(max_length=100)
    unique_selling_proposition = models.CharField(max_length=100)
    website = models.URLField()
    instagram = models.URLField()
    twitter = models.URLField()
    
    def __str__(self):
        return self.company_name
    
class financialdetails(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    current_gross_profit_margin = models.CharField(max_length=100)
    current_unit_manufacturing_cost = models.CharField(max_length=100)
    growth_plan_percentage = models.CharField(max_length=100)
    outstanding_debt= models.CharField(max_length=100)
    current_revenue = models.CharField(max_length=100)
    projected_revenue = models.CharField(max_length=100)
    runway = models.CharField(max_length=100)
    previous_funding_round = models.CharField(max_length=100)
    
    def __str__(self):
        return self.company_name
    
class EliminatedUser_Round2(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    
class Round3_users(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_development_stage = models.CharField(max_length=100)
    sales= models.CharField(max_length=100)
    unique_selling_proposition = models.CharField(max_length=100)
    website = models.URLField()
    instagram = models.URLField()
    twitter = models.URLField()
    current_gross_profit_margin = models.CharField(max_length=100)
    current_unit_manufacturing_cost = models.CharField(max_length=100)
    growth_plan_percentage = models.CharField(max_length=100)
    outstanding_debt= models.CharField(max_length=100)
    current_revenue = models.CharField(max_length=100)
    projected_revenue = models.CharField(max_length=100)
    runway = models.CharField(max_length=100)
    previous_funding_round = models.CharField(max_length=100)
    
    def __str__(self):
        return self.company_name

