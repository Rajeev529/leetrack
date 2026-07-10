from django.shortcuts import render, redirect
import os
from .freq import count, tier
from django.http import JsonResponse
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote
from .models import SavedCompany, SolvedQuestion

# Create your views here.

def index(request):
    return render(request,"homepage.html", {"tier":tier})

def search_page(request):
    return render(request,"search_page.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "signup.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("index")

    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # In this implementation, username is the same as email
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect("index")
        else:
            messages.error(request, "Invalid email or password!")
            return render(request, "login.html")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("index")

@login_required
def profile_view(request):
    user = request.user
    solved_count = SolvedQuestion.objects.filter(user=user).count()
    saved_companies = SavedCompany.objects.filter(user=user)
    return render(request, "profile.html", {"user": user, "solved_count": solved_count, "saved_companies": saved_companies})

@login_required
def profile_edit_view(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    return render(request, "profile_edit.html", {"user": request.user})

@login_required
def save_company(request, company_name):
    challenge_type = request.GET.get("type", "All")
    SavedCompany.objects.get_or_create(user=request.user, company_name=company_name, challenge_type=challenge_type)
    messages.success(request, f"{company_name} {challenge_type} challenge saved!")
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def toggle_solve(request, company_name, question_name):
    obj, created = SolvedQuestion.objects.get_or_create(user=request.user, company_name=company_name, question_name=question_name)
    if not created:
        obj.delete()
        solved = False
        msg = f"Unmarked {question_name} as solved."
    else:
        solved = True
        msg = f"Marked {question_name} as solved!"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'solved': solved})

    if not created:
        messages.info(request, msg)
    else:
        messages.success(request, msg)

    return redirect(request.META.get('HTTP_REFERER', 'index'))

def get_company_questions_data(request, company_name, csv_file_name):
    company_name = unquote(unquote(company_name))
    df = read_company_csv(company_name, csv_file_name)
    df = df.to_dict(orient='records')

    solved_questions = set()
    if request.user.is_authenticated:
        solved_questions = set(
            SolvedQuestion.objects.filter(user=request.user, company_name=company_name)
            .values_list('question_name', flat=True)
        )

    for x in df:
        x['val'] = count.get(x["Title"], 0)
        x['is_solved'] = x["Title"] in solved_questions

    return df, company_name

def company_questions(request, company_name):
    all_file = "5. All.csv"
    comp = get_companies_images()

    df, company_name = get_company_questions_data(request, company_name, all_file)

    return render(request, "qlist.html", {
        "df": df,
        "company_name": company_name,
        "imgs": comp.get(company_name),
        "challenge_type": "All"
    })

def roadmap_30(request, company_name):
    all_file = "2. Three Months.csv"
    comp=get_companies_images()

    df, company_name = get_company_questions_data(request, company_name, all_file)

    return render(request, "qlist.html", {
        "df": df,
        "company_name": company_name,
        "imgs":comp.get(company_name),
        "challenge_type": "30 Days Challenge"
    })

def get_companies(request):
    BASE_DIR = os.path.join(os.getcwd(), 'logos')
    companies = []
    for file in os.listdir(BASE_DIR):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
            name = os.path.splitext(file)[0]
            companies.append({
                "name": name,
                "logo": f"/logos/{file}"
            })
    return JsonResponse({"companies": companies})

def read_company_csv(company_name, csv_file_name):
    BASE_PATH = "Companies"
    file_path = os.path.join(BASE_PATH, company_name, csv_file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

def get_companies_images():
    BASE_DIR = os.path.join(os.getcwd(), 'logos')
    companies = {}
    for file in os.listdir(BASE_DIR):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
            name = os.path.splitext(file)[0]
            companies[name]=f"/logos/{file}"
    return companies
