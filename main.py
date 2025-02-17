import tkinter as tk
from tkinter import messagebox, ttk
from database import connect_database
from analisis import employee_with_more_sales, analysis_sales_per_month, best_selling_product
from graphics import *
from reportes import *
#Functions

connection = None
def connect():
    global connection
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
    options = [
        ("Employee With More Sales", "employee"),
        ("Analysis Sales Per Month", "sales"),
        ("Best Selling Product", "products"),
    ]

    for text, analysis_type in options:
        button = tk.Button(root, text=text, command=lambda at=analysis_type: show_options(at))
        button.pack()

def show_options(analysis_type):
    root_options = tk.Tk()
    root_options.title("Options")
    root_options.geometry("300x300")

    actions = [
        ("View DataFrame", view_df),
        ("View Graphic", view_graphic),
        ("Export DataFrame", export_df)
    ]

    for text, action in actions:
        button = tk.Button(root_options, text=text, command=lambda a=action, at=analysis_type: a(at))
        button.pack()

    root_options.mainloop()

def create_year_window():
    year_window = tk.Toplevel()  # Usamos Toplevel para evitar otra ventana principal
    year_window.title("Enter year")

    label_year = tk.Label(year_window, text="Enter the year: ")
    label_year.pack()

    entry_year = tk.Entry(year_window)
    entry_year.pack()

    return year_window, entry_year  # Retornamos la ventana y la entrada

def validate_year(year):
    if not year.isdigit():
        messagebox.showerror("The entry not is a year")
        return False
    return True

def create_df(analysis_type,year):
    if analysis_type == "employee":
        return employee_with_more_sales(connection,year)
    elif analysis_type == "sales":
        return analysis_sales_per_month(connection,year)
    elif analysis_type == "products":
        return best_selling_product(connection,year)
    else:
        messagebox.showerror("Error", "Invalid analysis type")
        return None

def create_graphic(analysis_type,df):
    if analysis_type == "employee":
        graphic_employee(df)
    elif analysis_type == "sales":
        graphics_sales(df)
    elif analysis_type == "products":
        graphic_best_product(df)
    else:
        messagebox.showerror("Error", "Invalid analysis type")
        return None


def validate_df(analysis_type,df,year):
    if not df.empty:
        df_window = tk.Toplevel()
        df_window.title(f"Dataframe for {analysis_type} in {year}")
        df_window.geometry("500x300")
        table = ttk.Treeview(df_window, columns=list(df.columns), show = "headings")
        for col in df.columns:
            table.heading(col,text =col)
            table.column(col,width=100)
        for index, row in df.iterrows():
            table.insert("","end",values = row.tolist())    
        table.pack(expand=True,fill="both")
        df_window.mainloop()
    else:
        messagebox.showerror("Error", "No data to show.")


def view_df(analysis_type):
    year_window, entry_year = create_year_window()
    def submit_year():
        year = entry_year.get()
        if not validate_year(year):
            return 
        year = int(year)
        year_window.destroy()
        df = create_df(analysis_type,year)
        validate_df(analysis_type,df,year)
    button_submit = tk.Button(year_window,text = "Submit", command = submit_year)
    button_submit.pack()
    year_window.mainloop()

def view_graphic(analysis_type):
    year_window, entry_year = create_year_window()
    def submit_year():
        year = entry_year.get()
        if not validate_year(year):
            return 
        year = int(year)
        year_window.destroy()
        df = create_df(analysis_type,year)
        if df.empty or df is None:
            messagebox.showerror("Error", "No database to show")
            return
        create_graphic(analysis_type, df)
    button_submit = tk.Button(year_window,text = "Submit", command = submit_year)
    button_submit.pack()
    year_window.mainloop()


def export_df(analysis_type):
    year_window, entry_year = create_year_window()
    
    def submit_year():
        year = entry_year.get()
        if not validate_year(year):
            return 
        year = int(year)
        year_window.destroy()
        
        df = create_df(analysis_type, year)
        if df.empty or df is None:
            messagebox.showerror("Error", "No data available for the selected year")
            return
        
        # Crear ventana para elegir formato
        export_window = tk.Toplevel()
        export_window.title("Choose Export Format")
        export_window.geometry("300x200")
        
        # Variables para cada formato
        var_excel = tk.BooleanVar()
        var_csv = tk.BooleanVar()
        var_latex = tk.BooleanVar()
        
        # Crear los checkbuttons para elegir el formato
        chk_excel = tk.Checkbutton(export_window, text="Excel", variable=var_excel)
        chk_excel.pack()
        chk_csv = tk.Checkbutton(export_window, text="CSV", variable=var_csv)
        chk_csv.pack()
        chk_latex = tk.Checkbutton(export_window, text="Latex", variable=var_latex)
        chk_latex.pack()
        
        def generate_report():
            formats = []
            if var_excel.get():
                formats.append("excel")
            if var_csv.get():
                formats.append("csv")
            if var_latex.get():
                formats.append("latex")
            
            if not formats:
                messagebox.showerror("Error", "Please select at least one format.")
                return
            
            # Llamar a las funciones de reportes.py según el tipo de análisis
            report_name = "report_" + str(year)  # Nombre del archivo (puedes personalizarlo más)
            
            if analysis_type == "employee":
                for format in formats:
                    generate_report_employee(df, report_name, format)
            elif analysis_type == "sales":
                for format in formats:
                    generate_report_analysis(df, report_name, format)
            elif analysis_type == "products":
                for format in formats:
                    generate_report_products(df, report_name, format)
            else:
                messagebox.showerror("Error", "Invalid analysis type")
                return None
            messagebox.showinfo("Success", f"Reports generated successfully for {formats} format(s)")

        # Botón para generar el reporte
        btn_generate = tk.Button(export_window, text="Generate Report", command=generate_report)
        btn_generate.pack()

    button_submit = tk.Button(year_window, text="Submit", command=submit_year)
    button_submit.pack()
    year_window.mainloop()

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




