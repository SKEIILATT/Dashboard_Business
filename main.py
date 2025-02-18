import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
from database import connect_database
from analisis import employee_with_more_sales, analysis_sales_per_month, best_selling_product
from graphics import *
from reportes import *

STYLE_FONT = ("Arial", 12)
STYLE_BUTTON = {"width": 20, "height": 2, "font": ("Arial", 10, "bold"), "bg": "#FF4081", "fg": "white", "relief": "flat", "bd": 0, "activebackground": "#FF80AB", "activeforeground": "white", "highlightthickness": 1, "highlightcolor": "#FF4081"}
STYLE_LABEL = {"font": ("Arial", 12), "bg": "#121212", "fg": "#F5F5F5"}
STYLE_ENTRY = {"font": ("Arial", 12), "bd": 0, "relief": "flat", "width": 30, "bg": "#1F1F1F", "fg": "white", "insertbackground": "white", "highlightthickness": 1, "highlightcolor": "#FF4081"}
STYLE_WINDOW = {"bg": "#121212"}
STYLE_FRAME = {"bg": "#1F1F1F", "padx": 10, "pady": 10}
STYLE_TREEVIEW = {"font": ("Arial", 10), "background": "#2C2C2C", "foreground": "#F5F5F5", "height": 8}
STYLE_OPTION_BUTTON = {"width": 20, "height": 2, "font": ("Arial", 10, "bold"), "bg": "#4CAF50", "fg": "white", "relief": "flat", "bd": 0, "activebackground": "#81C784", "activeforeground": "white", "highlightthickness": 1, "highlightcolor": "#4CAF50", "borderwidth": 2}

# Functions
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
    
    connection = connect_database(user, password, host, database)

    if connection and connection.is_connected():
        messagebox.showinfo("Success", "Database connected!")
        call_principalwindow()
    else:
        messagebox.showerror("Error", "Database can't connect!")

def call_principalwindow():  
    root_database.destroy()
    root_dashboard = tk.Tk()
    root_dashboard.title("Dashboard Company")
    
    root_dashboard.geometry("800x600")
    root_dashboard.config(bg="#121212")
    generate_buttons(root_dashboard)
    root_dashboard.mainloop()

def generate_buttons(root):

    employee_icon = PhotoImage(file="img\\icon_employee.png").subsample(4)
    sales_icon = PhotoImage(file="img\\icon_producto.png").subsample(4)  
    products_icon = PhotoImage(file="img\\ventas.png").subsample(4)  

    options = [
        ("Employee With More Sales", "employee", employee_icon),
        ("Analysis Sales Per Month", "sales", sales_icon),
        ("Best Selling Product", "products", products_icon),
    ]
    
    for text, analysis_type, icon in options:
    
        button = tk.Button(root, text=text, image=icon, compound="left", command=lambda at=analysis_type: show_options(at), **STYLE_BUTTON)
        button.image = icon
        
      
        button.config(width=200, height=200)

        button.pack(pady=15,fill="x")


def show_options(analysis_type):
    root_options = tk.Tk()
    root_options.title("Options")
    root_options.geometry("300x400")
    root_options.config(bg="#121212")

    actions = [
        ("View DataFrame", view_df),
        ("View Graphic", view_graphic),
        ("Export DataFrame", export_df)
    ]

   
    frame = tk.Frame(root_options, bg="#1F1F1F", padx=20, pady=20)
    frame.pack(pady=20, fill="both", expand=True)

    for text, action in actions:
        button = tk.Button(frame, text=text, command=lambda a=action, at=analysis_type: a(at), **STYLE_OPTION_BUTTON)
        button.pack(pady=10, fill="x")

    root_options.mainloop()

def create_year_window():
    year_window = tk.Toplevel()  
    year_window.title("Enter Year")
    year_window.config(bg="#121212")

    label_year = tk.Label(year_window, text="Enter the year: ", **STYLE_LABEL)
    label_year.pack(pady=20)

    entry_year = tk.Entry(year_window, **STYLE_ENTRY)
    entry_year.pack(pady=5)

    return year_window, entry_year 

def validate_year(year):
    if not year.isdigit():
        messagebox.showerror("Invalid Year", "Please enter a valid year.")
        return False
    return True

def create_df(analysis_type, year):
    if analysis_type == "employee":
        return employee_with_more_sales(connection, year)
    elif analysis_type == "sales":
        return analysis_sales_per_month(connection, year)
    elif analysis_type == "products":
        return best_selling_product(connection, year)
    else:
        messagebox.showerror("Error", "Invalid analysis type")
        return None

def create_graphic(analysis_type, df):
    if analysis_type == "employee":
        graphic_employee(df)
    elif analysis_type == "sales":
        graphics_sales(df)
    elif analysis_type == "products":
        graphic_best_product(df)
    else:
        messagebox.showerror("Error", "Invalid analysis type")
        return None


def validate_df(analysis_type, df, year):
    if not df.empty:
        
        df_window = tk.Toplevel()
        df_window.title(f"Dataframe for {analysis_type} in {year}")
        df_window.geometry("500x200")
        df_window.config(bg="#121212") 

        style = ttk.Style()
        style.configure("Treeview",
                        font=("Arial", 12),  
                        background="#1F1F1F",  
                        foreground="White",  
                        fieldbackground="#1F1F1F",  
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"),  
                        background="#FF4081",  
                        foreground="Black",  
                        borderwidth=0)

       
        table = ttk.Treeview(df_window, columns=list(df.columns), show="headings", style="Treeview")
        for col in df.columns:
            table.heading(col, text=col)
            table.column(col, width=100)
        for index, row in df.iterrows():
            table.insert("", "end", values=row.tolist())
        table.pack(expand=True, fill="both")


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
        df = create_df(analysis_type, year)
        validate_df(analysis_type, df, year)

    button_submit = tk.Button(year_window, text="Submit", command=submit_year, **STYLE_BUTTON)
    button_submit.pack(pady=20)
    year_window.mainloop()

def view_graphic(analysis_type):
    year_window, entry_year = create_year_window()

    def submit_year():
        year = entry_year.get()
        if not validate_year(year):
            return 
        year = int(year)
        year_window.destroy()
        df = create_df(analysis_type, year)
        if df.empty or df is None:
            messagebox.showerror("Error", "No data to show")
            return
        create_graphic(analysis_type, df)

    button_submit = tk.Button(year_window, text="Submit", command=submit_year, **STYLE_BUTTON)
    button_submit.pack(pady=20)
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
        
        export_window = tk.Toplevel()
        export_window.title("Choose Export Format")
        export_window.geometry("300x200")
        export_window.config(bg="#121212")
        
        var_excel = tk.BooleanVar()
        var_csv = tk.BooleanVar()
        var_latex = tk.BooleanVar()
        
        chk_excel = tk.Checkbutton(export_window, text="Excel", variable=var_excel, fg="white", bg="#121212", selectcolor="#FF4081", activebackground="#FF80AB")
        chk_excel.pack(pady=5)
        chk_csv = tk.Checkbutton(export_window, text="CSV", variable=var_csv, fg="white", bg="#121212", selectcolor="#FF4081", activebackground="#FF80AB")
        chk_csv.pack(pady=5)
        chk_latex = tk.Checkbutton(export_window, text="Latex", variable=var_latex, fg="white", bg="#121212", selectcolor="#FF4081", activebackground="#FF80AB")
        chk_latex.pack(pady=5)
        
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
            
            report_name = "report_" + str(year)
            
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

        btn_generate = tk.Button(export_window, text="Generate Report", command=generate_report, **STYLE_BUTTON)
        btn_generate.pack(pady=20)

    button_submit = tk.Button(year_window, text="Submit", command=submit_year, **STYLE_BUTTON)
    button_submit.pack(pady=20)
    year_window.mainloop()

def exit_fullscreen(event=None):
    root_database.attributes("-fullscreen", False)
    root_database.geometry("800x600")

root_database = tk.Tk()
root_database.title("Analysis Dashboard")
root_database.attributes("-fullscreen", True)
root_database.bind("<Escape>", exit_fullscreen)
root_database.config(bg="#121212")

label_message = tk.Label(root_database, text="Enter your credentials: ", **STYLE_LABEL)
label_message.pack(pady=40)

label_user = tk.Label(root_database, text="User: ", **STYLE_LABEL)
label_user.pack(pady=5)

entry_user = tk.Entry(root_database, **STYLE_ENTRY)
entry_user.pack(pady=5)

label_password = tk.Label(root_database, text="Password: ", **STYLE_LABEL)
label_password.pack(pady=5)

entry_password = tk.Entry(root_database, show="*", **STYLE_ENTRY)
entry_password.pack(pady=5)

label_host = tk.Label(root_database, text="Host: ", **STYLE_LABEL)
label_host.pack(pady=5)

entry_host = tk.Entry(root_database, **STYLE_ENTRY)
entry_host.pack(pady=5)

label_database = tk.Label(root_database, text="Database: ", **STYLE_LABEL)
label_database.pack(pady=5)

entry_database = tk.Entry(root_database, **STYLE_ENTRY)
entry_database.pack(pady=5)

button_connect = tk.Button(root_database, text="Connect", command=connect, **STYLE_BUTTON)
button_connect.pack(pady=20)

root_database.mainloop()
