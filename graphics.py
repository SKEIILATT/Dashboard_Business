import matplotlib.pyplot as plt
#  analysis_sales_per_month
ERROR_EMPTY_DF = "Error: DataFrame is empty. Check the data source."
ERROR_NONE_DF = "Error: DataFrame is None. Verify data loading."

def graphics_sales (df):
    if df is None:
        print(ERROR_NONE_DF)
        return
    if df.empty:
        print(ERROR_EMPTY_DF)
        return
    
    df.plot(x="Month", y="Total Price Sales", kind="line",marker="o", color="blue")
    plt.title("Analysis sales per month")
    plt.xlabel("Months")
    plt.ylabel("Solds")
    plt.show()

# employee_with_more_sales
def graphic_employee(df):
    if df is None:
        print(ERROR_NONE_DF)
        return
    if df.empty:
        print(ERROR_EMPTY_DF)
        return
    
    df.plot(x="Employee",y="Total Price",kind = "barh", color="blue")
    plt.title("Employee with more sales")
    plt.xlabel("Employees")
    plt.ylabel("Total Prices Sales")
    plt.show()

#best_selling_product
def graphic_best_product(df):
    if df is None:
        print(ERROR_NONE_DF)
        return
    if df.empty:
        print(ERROR_EMPTY_DF)
        return
    
    df.plot(x="Product",y="Quantity",kind = "bar", color="blue")
    plt.title("Best selling products")
    plt.xlabel("Products")
    plt.ylabel("Quantity")
    plt.show()


