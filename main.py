import tkinter as tk
from tkinter import messagebox
from database import connect_database
from analisis import employee_with_more_sales
from database import connection
#Functions
def connect():

    user = entry_user.get()
    password = entry_password.get()
    host = entry_host.get()
    database = entry_database.get()

    if not user or not password or not host or not database:
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    
    connection = connect_database(user,password,host,database)

    if (connection and connection.is_connected()):
        messagebox.showinfo("Success, database conected")
        call_principalwindow()
    else:
        messagebox.showerror("Error, database cant connect")

def call_principalwindow():  
    root_database.destroy()
    root_dashboard = tk.Tk()
    root_dashboard.title("DashBoard Company")
    root_dashboard.geometry("500x500")  
    generate_buttons(root_dashboard)
    root_dashboard.mainloop()


def generate_buttons(root):
    button_employee = tk.Button(root,text="Employee With More Sales", command= show_options_employee)
    button_employee.pack()
    button_sales_per_month = tk.Button(root,text="Analysis sales per month", command= show_options_analysis)
    button_sales_per_month.pack()
    button_bestproduct = tk.Button(root,text="Best selling product", command= show_options_products)
    button_bestproduct.pack()


def show_options_employee():
    root_options = tk.Tk()
    root_options.title("Options")
    root_options.geometry("300x300")
    button_df = tk.Button(root_options,text="View dataframe", command=view_df_employee)
    button_df.pack()
    button_graphic = tk.Button(root_options,text="View Graphic", command=view_graphic_employee)
    button_graphic.pack()
    button_export = tk.Button(root_options,text="Export dataframe", command=export_df_employee)
    button_export.pack()
    root_options.mainloop()

def view_df_employee():
    print("Hola")

def export_df_employee():
    print("Hola")

def view_graphic_employee():
    print("Hola")

def show_options_analysis():
    print("Hola")

def show_options_products():
    print("Hola")

root_database = tk.Tk()
root_database.title("Analysis Dashboard")
root_database.geometry("500x500")

label_message = tk.Label(root_database, text="Enter your credentials to connect your database")
label_message.pack()

label_user = tk.Label(root_database,text="User: ")
label_user.pack()
entry_user = tk.Entry(root_database)
entry_user.pack()


label_password = tk.Label(root_database,text="Password: ")
label_password.pack()
entry_password = tk.Entry(root_database, show="*")
entry_password.pack()


label_host = tk.Label(root_database,text="Host: ")
label_host.pack()
entry_host = tk.Entry(root_database)
entry_host.pack()


label_db = tk.Label(root_database,text="Name Database: ")
label_db.pack()
entry_database = tk.Entry(root_database)
entry_database.pack()

button_connect = tk.Button(root_database,text="Connect database",command=connect)
button_connect.pack()


root_database.mainloop()




