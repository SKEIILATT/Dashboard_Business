import pandas as pd
import calendar as c
from database import connect_database
import mysql.connector as msc

#Function for generate querys 

def generate_querys(connection,consult):
    if not connection or not connection.is_connected():
        print("No active database connection. Please connect first.")
        return None
    try:
        cursor = connection.cursor()
        cursor.execute(consult)
        result = cursor.fetchall()
        cursor.close()
        return result
    except msc.Error as e:
        print(f"Error executing query: {e}")
        return None

#Function for generate dataframes based on of querys results
def generate_dataframes(query, list_columnas):
    columnas = list_columnas
    df_generado = pd.DataFrame(query, columns=columnas)
    return df_generado


#Function for the analysis of total sales per month
def analysis_sales_per_month(connection,year):
    query_sales = generate_querys(connection,"SELECT date_of_sale,price FROM sales")

    if query_sales is None:
        print("No data returned from the query")
        return pd.DataFrame()
    
    df_sales = generate_dataframes(query_sales, ["Date", "Price"])

    #Convert the date of sale to date and price to float
    df_sales["Date"] = pd.to_datetime(df_sales["Date"])
    df_sales["Price"] = pd.to_numeric(df_sales["Price"])

    ##Filter the data
    df_filter = df_sales[df_sales["Date"].dt.year == year]
    if df_filter.empty:
        print(f"No sales data for the year {year}")
        return df_filter
    
    df_filter["Month"] = df_filter["Date"].dt.month

    sales_per_mes = df_filter.groupby("Month")["Price"].sum()
    ##Convert to df
    sales_per_mes = sales_per_mes.reset_index()
    sales_per_mes.columns = ["Month","Total Price Sales"]
    sales_per_mes["Month"] = sales_per_mes["Month"].map(lambda x: c.month_name[x])
    return sales_per_mes

def employee_with_more_sales(connection,year):
    query_sales = generate_querys(connection,"SELECT e.first_name,s.price,s.date_of_sale FROM sales s JOIN employee e ON e.id_employee = s.id_employee")
    if query_sales is None:
        print("No data returned from the query")
        return pd.DataFrame()
    
    df_employeesales = generate_dataframes(query_sales,["Employee","Price","Date"])
    #Filter the data
    df_employeesales["Date"] = pd.to_datetime(df_employeesales["Date"])
    df_employeesales["Price"] = pd.to_numeric(df_employeesales["Price"])
    ## Verification the year
    df_filter = df_employeesales[df_employeesales["Date"].dt.year == year]
    if df_filter.empty:
        print(f"No sales data for the year {year}")
        return df_filter
    
    employee_with_more_sales = df_filter.groupby("Employee")["Price"].sum()
    #convert to df
    employee_with_more_sales = employee_with_more_sales.reset_index()
    employee_with_more_sales.columns = ["Employee", "Total Price"]
    employee_with_more_sales.sort_values(by="Total Price", ascending=False)
    return employee_with_more_sales


def best_selling_product(connection,year):
    query_result = generate_querys(connection,"SELECT product, quantity, date_of_sale FROM sales")
    if query_result is None:
        print("No data returned from the query")
        return pd.DataFrame()
    
    df_best_product = generate_dataframes(query_result, ["Product","Quantity","Date"])
    df_best_product["Date"] = pd.to_datetime(df_best_product["Date"])
    df_filter_products = df_best_product[df_best_product["Date"].dt.year==year]
    if df_filter_products.empty:
        print(f"No sales data for the year {year}")
        return df_filter_products

    best_selling_product = df_filter_products.groupby("Product")["Quantity"].sum()
    best_selling_product = best_selling_product.reset_index()
    best_selling_product.columns = ["Product","Quantity"]
    best_selling_product.sort_values(by = "Quantity", ascending = False)
    return best_selling_product








