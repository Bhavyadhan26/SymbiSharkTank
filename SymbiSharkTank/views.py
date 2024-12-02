from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse,HttpResponseRedirect
from .models import SignUp,registration_details,EliminatedUser_Round1,Round2_users,EliminatedUser_Round2,financialdetails,Round3_users
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .tasks import send_mail_after_delay
import os
import pandas as pd
from django.core.mail import send_mail
from django.db.models import Subquery
from django.conf import settings
from datetime import timedelta, datetime

def login_view(request):
    error_occurred = False  
    if request.method == 'POST':
        print("Form submitted")
        email = request.POST['user']
        password = request.POST['pass']    
        # Check if user exists and credentials are valid
        user1 = authenticate(request, username=email, password=password)
        if user1 is not None:
            # Login successful
            login(request, user1)
            next_url = request.GET.get('next', '')  # Get the next URL from the GET parameters
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')  # Redirect to the home page after successful login
        else:
            # Authentication failed
            messages.error(request, 'Invalid email or password.')
            error_occurred = True
    return render(request, 'login.html', {'error_occurred': error_occurred})

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        password = request.POST['password']
        try:
            #save data to mysql also
            SignUp.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                contact_number=contact_number,
                password=password
            )
            # Save data to the database of django for authentication
            user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
            )
            messages.success(request, 'Signup successful. Please log in.')
            return redirect('login')
        except IntegrityError:
            # Handle case where email already exists
            error_message = "Email already exists. Please login to continue"
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')
    
@login_required
def register(request):
    email1 = request.user.email  # Assuming the email is stored in the user model
    if request.method == 'POST':
        email=request.POST['email']
        company_name = request.POST['company_name']
        product_name = request.POST['product_name']
        product_development_stage = request.POST['product_development_stage']
        sales = request.POST['sales']
        unique_selling_proposition = request.POST['unique_selling_proposition']
        website=request.POST['website']
        instagram=request.POST['instagram']
        twitter=request.POST['twitter']
        try:
            #save data to mysql table created automatically by django
            registration_details.objects.create(
                email=email,
                company_name=company_name,
                product_name=product_name,
                product_development_stage=product_development_stage,
                sales=sales,
                unique_selling_proposition = unique_selling_proposition,
                website=website,
                instagram=instagram,
                twitter=twitter
            )
            run_bot_logic_round1()
            return redirect('home')
            # return redirect('registration_success_1')
        except IntegrityError:
            print("error")
    return render(request, 'register_product.html',{'email_user': email1})

#bot-logic round 1
def run_bot_logic_round1():
    # Fetch users from the database and perform checks
    users = registration_details.objects.order_by('-id').last()
    user_dict = {}
    for field_name, field_value in users.__dict__.items():
        # Exclude internal fields starting with underscore and 'id'
        if not field_name.startswith('_') and field_name != 'id':
            user_dict[field_name] = field_value

    # Check conditions for elimination in round1
    condition_met = False
    if user_dict.get('product_development_stage') == "Beta":
        condition_met = True
    # or user.sales == "Retail"
    
    # Perform operations based on the condition
    if condition_met:
        # Create a new record in the EliminatedUser table
        eliminated_user = EliminatedUser_Round1.objects.create(
            company_name=user_dict.get('company_name')
        )
        eliminated_user.save()  # Save the new record

    # Fetch and store data
    fetch_and_store_data_()
    
    # Prepare the email message
    if condition_met:
        message = f"Dear {user_dict.get('company_name')},\n\nWe regret to inform you that you have been eliminated in Round 1."
    else:
        message = f"Dear {user_dict.get('company_name')},\n\nCongratulations! You have advanced to the next round."

    # Schedule the email to be sent after 1 hour (3600 seconds)
    send_mail_after_delay.apply_async(
        (
            user_dict.get('email'),
            message, 
            settings.EMAIL_HOST_USER, 
            settings.EMAIL_HOST_PASSWORD
        ),
        countdown=3#3seconds delay in sending email
    )
    
    print("Elimination of round 1 done successfully. Applicants will be informed within 1 hour.")
    return redirect('/home')


def register_round2(request):
    try:
        # Fetch company name based on the logged-in user's email
        email=email = request.user.email
        registration_detail = registration_details.objects.get(email=email)
        company_name1 = registration_detail.company_name
        round2_user = Round2_users.objects.get(company_name=company_name1)
        # round2_user = Round2_users.objects.get(email=email)
        # company_name1 = round2_user.company_name
    except Round2_users.DoesNotExist:
        # If no Round2_users object is found, redirect to the home page
        return HttpResponseRedirect('/home')  # Adjust the URL as per your project's URL configuration
    if request.method == 'POST':
        company_name11 = request.POST.get('company_name11')
        current_gross_profit_margin = request.POST.get('current_gross_profit_margin')
        current_unit_manufacturing_cost = request.POST.get('current_unit_manufacturing_cost')
        growth_plan_percentage = request.POST.get('growth_plan_percentage')
        outstanding_debt = request.POST.get('outstanding_debt')
        current_revenue = request.POST.get('current_revenue')
        projected_revenue = request.POST.get('projected_revenue')
        runway = request.POST.get('runway')
        previous_funding_round = request.POST.get('previous_funding_round')

        # Save data to FinancialDetails table
        financialdetails.objects.create(
            company_name=company_name1,
            current_gross_profit_margin=current_gross_profit_margin,
            current_unit_manufacturing_cost=current_unit_manufacturing_cost,
            growth_plan_percentage=growth_plan_percentage,
            outstanding_debt=outstanding_debt,
            current_revenue=current_revenue,
            projected_revenue=projected_revenue,
            runway=runway,
            previous_funding_round=previous_funding_round
        )
        run_bot_logic_round2()
        # return redirect('home')
    return render(request, 'round2.html', {'company_name1': company_name1})

#Stores user selected for round2 in Round2_user table (update button)
def fetch_and_store_data_():
    # Fetch names from Table 2
    table2_names = EliminatedUser_Round1.objects.values_list('company_name', flat=True)
    
    # Fetch data from Table 1 for names not existing in Table 2
    source_data = registration_details.objects.exclude(company_name__in=table2_names)
    
    # Iterate through the filtered data and store it in the destination table
    for item in source_data:
        # # Check if the name exists in Table 2 before creating a new record in Table 3
            # Check if the name doesn't already exist in Table 3
            # if not Round2_users.objects.filter(company_name=item.company_name).exists():
            if item.product_development_stage != "Beta" and not Round2_users.objects.filter(company_name=item.company_name).exists():
                # Create a new record in Table 3
                Round2_users.objects.create(
                    company_name=item.company_name,
                    product_name=item.product_name,
                    product_development_stage=item.product_development_stage,
                    sales=item.sales,
                    unique_selling_proposition = item.unique_selling_proposition,
                    website=item.website,
                    instagram=item.instagram,
                    twitter=item.twitter
                )

#round-2 bot logic
def run_bot_logic_round2():
    # Fetch users from the database and perform checks
    users = financialdetails.objects.order_by('-id').last()
    user_dict={}
    for field_name, field_value in users.__dict__.items():
        # Exclude internal fields starting with underscore and 'id'
        if not field_name.startswith('_') and field_name != 'id':
            user_dict[field_name] = field_value

    condition_met = False
    if user_dict.get('current_gross_profit_margin') == "0" or user_dict.get('current_unit_manufacturing_cost') == "Unknown" or user_dict.get('growth_plan_percentage') == "0":
        condition_met = True
        
    if condition_met:
            # Create a new record in the EliminatedUser table
            eliminated_user = EliminatedUser_Round2.objects.create(
                company_name = user_dict.get('company_name')
            )
            eliminated_user.save()  # Save the new record
    fetch_and_store_data_round3()
        
        # Schedule sending emails after an hour
    # send_mail_after_delay.delay(
    #         request.get.mail, 
    #         "Sorry" if not condition_met else "Yes", 
    #         settings.EMAIL_HOST_USER,  # Email host user
    #         settings.EMAIL_HOST_PASSWORD  # Email host password
    #)
    print("Elimination of round 2 done succesfully. Applicants will be informed within 2hrs.")
    return redirect('/home')

# @staff_member_required(login_url='/admin/')
# def display_data_round2_eliminated_users(request):
    # if request.method == 'POST':
    #     # Perform actions when the button is clicked
    #     # data3 = financialdetails.objects.filter(name__in=EliminatedUser_Round2.objects.values_list('company_name', flat=True))
    #     # return render(request, 'displaydata.html', {'data': data3})
    #     company_names = EliminatedUser_Round2.objects.values_list('company_name', flat=True)
    #     all_records = []
    #     # Fetch records from RegistrationDetails and FinancialDetails for each company name
    #     for company_name in company_names:
    #          registration_records = Round2_users.objects.filter(company_name=company_name).values()
    #          financial_records = financialdetails.objects.filter(company_name=company_name).values()
    #          #Combine records for this company into a single set
    #          all_records.extend(list(registration_records) + list(financial_records))
    #     # Now, all_records contains records from both tables for all company names
    #     # Pass all_records to your template
    #     return render(request, 'displaydata.html', {'all_records': all_records})

    # return render(request, 'displaydata.html')

#Stores users selected for round3 in Round3_users table - used in view button round 3
def fetch_and_store_data_round3():
    # Fetch names from EliminatedUser_Round2
    eliminated_company_names = EliminatedUser_Round2.objects.values_list('company_name', flat=True)
    # Fetch financial details for companies not existing in EliminatedUser_Round2
    financial_data = financialdetails.objects.exclude(company_name__in=eliminated_company_names)
    # Iterate through the financial data and store it in the Round3_users table
    for item in financial_data:
        # Fetch corresponding record from Round2_users
        round2_record = Round2_users.objects.filter(company_name=item.company_name).first()
        if round2_record:
            if(item.current_gross_profit_margin !="0" and item.current_unit_manufacturing_cost != "Unknown" and item.growth_plan_percentage != "0" 
               and not Round3_users.objects.filter(company_name=item.company_name).exists()):
            # Create a new record in Round3_users
                Round3_users.objects.create(
                    company_name=round2_record.company_name,
                    product_name=round2_record.product_name,
                    product_development_stage=round2_record.product_development_stage,
                    sales=round2_record.sales,
                    unique_selling_proposition = round2_record.unique_selling_proposition,
                    website=round2_record.website,
                    instagram=round2_record.instagram,
                    twitter=round2_record.twitter,
                    current_gross_profit_margin=item.current_gross_profit_margin,
                    current_unit_manufacturing_cost=item.current_unit_manufacturing_cost,
                    growth_plan_percentage=item.growth_plan_percentage,
                    outstanding_debt=item.outstanding_debt,
                    current_revenue=item.current_revenue,
                    projected_revenue=item.projected_revenue,
                    runway=item.runway,
                    previous_funding_round=item.previous_funding_round,
                )
            
@login_required
def user_profile(request):
    # if request.user.is_authenticated:
        email = request.user.email  # Assuming the email is stored in the user model
        try:
            user_details = SignUp.objects.get(email=email)
        except SignUp.DoesNotExist:
            user_details = None
            
        try:
            registration_user = registration_details.objects.get(email=email)
            company_name = registration_user.company_name
        except registration_details.DoesNotExist:
            company_name = None
            
        return render(request, 'profile.html', {'user_details': user_details,'company_name': company_name})
    
def about(request):
    return render(request,'about.html')

def success_stories(request):
    return render(request,'successstories.html')

def home(request):
    return render(request,'home_page.html')

def meet(request):
    try:
        # Fetch company name based on the logged-in user's email
        email=email = request.user.email
        registration_detail = registration_details.objects.get(email=email)
        company_name1 = registration_detail.company_name
        round3_user = Round3_users.objects.get(company_name=company_name1)
        # round2_user = Round2_users.objects.get(email=email)
        # company_name1 = round2_user.company_name
    except Round3_users.DoesNotExist:
        # If no Round2_users object is found, redirect to the home page
        return HttpResponseRedirect('/home')  # Adjust the URL as per your project's URL configuration
    return render(request,'meeting.html')

def custom_logout(request):
    # Clear session cookies
    request.session.flush()
    # Redirect to the login page
    return redirect('home')






# @staff_member_required(login_url='/admin/')             
def display_data_round3_users(request):
    if request.method == 'POST':
        # Perform actions when the button is clicked
        # For example, fetching data from the database
        data = Round3_users.objects.all()  # Fetch all data from the table
        return render(request, 'displaydata.html', {'data': data})
    return render(request, 'displaydata.html')

# @staff_member_required(login_url='/admin/')
def display_data_round1_users(request):
    if request.method == 'POST':
        # Perform actions when the button is clicked
        # For example, fetching data from the database
        data = registration_details.objects.all()  # Fetch all data from the table
        # Return JSON response with the fetched data
        data_list = list(data.values())  # Convert QuerySet to list for JSON serialization
        return JsonResponse({'data': data_list})
    else:
         return render(request, 'displaydata.html', context={})
     
# @staff_member_required(login_url='/admin/')
def export_data_round1_users(request):
    if request.method == 'POST':
        # Perform actions when the button is clicked
        # For example, fetching data from the database
        # data = registration_details.objects.all()  # Fetch all data from the table
        data = Round2_users.objects.all()
        
        # Create a DataFrame from the queryset
        df = pd.DataFrame(list(data.values()))
        
        # Export DataFrame to Excel
        excel_file_path = 'data.xlsx'
        df.to_excel(excel_file_path, index=False)
        
        # Serve the file as a downloadable response
        with open(excel_file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
            
            # Clean up: Delete the Excel file
        os.remove(excel_file_path)
        
        return response

    # return render(request, 'template.html')

# @staff_member_required(login_url='/admin/')
def display_data_round2_users(request):
    if request.method == 'POST':
        fetch_and_store_data_()
        # Perform actions when the button is clicked
        # For example, fetching data from the database
        data = Round2_users.objects.all()  # Fetch all data from the table
        return render(request, 'displaydata.html', {'data': data})
    return render(request, 'displaydata.html')


# @staff_member_required(login_url='/admin/')
# def display_data_round1_eliminated_users(request):
    # if request.method == 'POST':
    #     # Perform actions when the button is clicked
    #     data1 = registration_details.objects.filter(name__in=EliminatedUser_Round1.objects.values_list('company_name', flat=True))

    #     return render(request, 'displaydata.html', {'data': data1})

    # return render(request, 'displaydata.html')


# @staff_member_required(login_url='/admin/')
def export_data_round2_users(request):
    if request.method == 'POST':
        # Perform actions when the button is clicked
        # For example, fetching data from the database
        # data = financialdetails.objects.exclude(company_name__in=Subquery(EliminatedUser_Round2.objects.values('company_name')))
        excluded_company_names = EliminatedUser_Round2.objects.values_list('company_name', flat=True)

        # Exclude data from financial_details where company name matches Eliminated_User_Round2
        financial_records = financialdetails.objects.exclude(company_name__in=excluded_company_names)

        # Fetch data from round2_users for remaining company names
        round2_users_records = Round2_users.objects.exclude(company_name__in=excluded_company_names)

        # Merge data from both tables
        data = list(round2_users_records.values()) + list(financial_records.values())
        # Create a DataFrame from the queryset
        df = pd.DataFrame(data.values())
        
        # Export DataFrame to Excel
        excel_file_path = 'data.xlsx'
        df.to_excel(excel_file_path, index=False)
        
        # Serve the file as a downloadable response
        with open(excel_file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
        
        os.remove(excel_file_path)
        
        return response