import pandas as pd
from analisis import *
import openpyxl as op
import jinja2 as j

def generate_report_analysis(year):
    df = analysis_sales_per_month(year)
    print(df)
    report_name = input("Enter the file name: ")
    format_report = input("Enter the format (CSV,EXCEL,LATEX): ").lower()
    if (format_report=="excel"):
        return df.to_excel(report_name+".xlsx",index=False)
    elif (format_report=="csv"):
        return df.to_csv(report_name+".csv",index=False)
    elif (format_report=="latex"):
        return df.to_latex(report_name+".tex",index=False)
    else:
        print("Invalid format")
        return None

def generate_report_employee(year):
    df = employee_with_more_sales(year)
    print(df)
    report_name = input("Enter the file name: ")
    format_report = input("Enter the format (CSV,EXCEL,LATEX): ").lower()
    if (format_report=="excel"):
        return df.to_excel(report_name+".xlsx",index=False)
    elif (format_report=="csv"):
        return df.to_csv(report_name+".csv",index=False)
    elif (format_report=="latex"):
        return df.to_latex(report_name+".tex",index=False)
    else:
        print("Invalid format")
        return None

def generate_report_products(year):
    df = best_selling_product(year)
    print(df)
    report_name = input("Enter the file name: ")
    format_report = input("Enter the format (CSV,EXCEL,LATEX): ").lower()
    if (format_report=="excel"):
        return df.to_excel(report_name+".xlsx",index=False)
    elif (format_report=="csv"):
        return df.to_csv(report_name+".csv",index=False)
    elif (format_report=="latex"):
        return df.to_latex(report_name+".tex",index=False)
    else:
        print("Invalid format")
        return None
    





