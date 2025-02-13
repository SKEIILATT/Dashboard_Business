from database import connect_database
import pandas as pd
import calendar as c
#Function for generate querys 
def generate_querys(consult):
    connection = connect_database()
    if (connection):
        cursor = connection.cursor()
        cursor.execute(consult)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    else:
        print("The consultation failed")

#Function for generate dataframes based on of querys results
def generate_dataframes(query, list_columnas):
    columnas = list_columnas
    df_generado = pd.DataFrame(query, columns=columnas)
    return df_generado


#Function for the analysis of total sales per month

def analysis_sales_per_month(year):
    query_sales = generate_querys("SELECT date_of_sale,price FROM sales")
    df_sales = generate_dataframes(query_sales, ["Date", "Price"])
    #Convert the date of sale to date and price to float
    df_sales["Date"] = pd.to_datetime(df_sales["Date"])
    df_sales["Price"] = pd.to_numeric(df_sales["Price"])
    ##Filter the data
    df_filter = df_sales[df_sales["Date"].dt.year == year]
    df_filter["Month"] = df_filter["Date"].dt.month

    sales_per_mes = df_filter.groupby("Month")["Price"].sum()
    ##Convert to df
    sales_per_mes = sales_per_mes.reset_index()
    sales_per_mes.columns = ["Month","Total Price Sales"]
    sales_per_mes["Month"] = sales_per_mes["Month"].map(lambda x: c.month_name[x])
    print(sales_per_mes)






