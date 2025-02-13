import tkinter as tk
from tkinter import simpledialog, messagebox
from login import verify_password
from gui import open_main_window

def login():
    """ แสดงหน้าล็อกอินและตรวจสอบรหัสผ่าน """
    password = simpledialog.askstring("Login", "Enter Password:", show="*")
    
    if password and verify_password(password):
        root.destroy()  # ปิดหน้าต่างล็อกอิน
        open_main_window()  # เปิด GUI หลัก
    else:
        messagebox.showerror("Error", "Incorrect Password!")

# เรียกหน้าล็อกอิน
root = tk.Tk()
root.withdraw()  # ซ่อนหน้าต่างหลัก
login()
