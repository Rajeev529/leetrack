from django.shortcuts import render
import os
from .freq import count, tier
from django.http import JsonResponse
import json
import pandas as pd
# Create your views here.

def index(request):
    comp=get_companies(request)
    
    return render(request,"homepage.html", {"tier":tier})

def search_page(request):
    return render(request,"search_page.html")

def company_questions(request, company_name):
    all_file = "5. All.csv"
    comp=get_companies_images(request)
    company_name = company_name.replace("-", " ").title()
    # print("images",comp)
    
    df = read_company_csv(company_name, all_file)
    df = df.to_dict(orient='records')
    for x in df:
        x['val'] = count.get(x["Title"], 0)  # ✅ FIXED
    return render(request, "qlist.html", {"df": df,"company_name": company_name, "imgs":comp.get(company_name)})
def roadmap_30(request, company_name):
    all_file = "2. Three Months.csv"
    comp=get_companies_images(request)
    company_name = company_name.replace("-", " ").title()
    print("images",comp)
    
    df = read_company_csv(company_name, all_file)
    df = df.to_dict(orient='records')
    for x in df:
        x['val'] = count.get(x["Title"], 0)  # ✅ FIXED
    return render(request, "qlist.html", {"df": df,"company_name": company_name, "imgs":comp.get(company_name)})

def get_companies(request):
    BASE_DIR = os.path.join(os.getcwd(), 'logos')
    companies = []
    for file in os.listdir(BASE_DIR):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
            name = os.path.splitext(file)[0]  # remove .png

            companies.append({
                "name": name,
                "logo": f"/logos/{file}"
            })
    print(companies)
    return JsonResponse({"companies": companies})
def searched_item():
    all="5. All.csv"
    df=read_company_csv('Apple', all)
    print(df)


def read_company_csv(company_name, csv_file_name):
    BASE_PATH = "Companies"
    file_path = os.path.join(BASE_PATH, company_name, csv_file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)



def get_companies_images(request):
    BASE_DIR = os.path.join(os.getcwd(), 'logos')
    companies = {}
    for file in os.listdir(BASE_DIR):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
            name = os.path.splitext(file)[0]  # remove .png
            companies[name]=f"/logos/{file}"
    # print(companies)
    return companies