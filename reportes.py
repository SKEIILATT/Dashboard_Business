import pandas as pd

def generate_report_analysis(df, report_name, format_report):
    if format_report == "excel":
        return df.to_excel(report_name + ".xlsx", index=False)
    elif format_report == "csv":
        return df.to_csv(report_name + ".csv", index=False)
    elif format_report == "latex":
        return df.to_latex(report_name + ".tex", index=False)
    else:
        print("Invalid format")
        return None

def generate_report_employee(df, report_name, format_report):
    if format_report == "excel":
        return df.to_excel(report_name + ".xlsx", index=False)
    elif format_report == "csv":
        return df.to_csv(report_name + ".csv", index=False)
    elif format_report == "latex":
        return df.to_latex(report_name + ".tex", index=False)
    else:
        print("Invalid format")
        return None

def generate_report_products(df, report_name, format_report):
    if format_report == "excel":
        return df.to_excel(report_name + ".xlsx", index=False)
    elif format_report == "csv":
        return df.to_csv(report_name + ".csv", index=False)
    elif format_report == "latex":
        return df.to_latex(report_name + ".tex", index=False)
    else:
        print("Invalid format")
        return None





