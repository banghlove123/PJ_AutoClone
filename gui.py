import tkinter as tk
from tkinter import ttk, messagebox
from functions import start_clone

def open_main_window():
    """ เปิดหน้าต่างหลักของโปรแกรม """
    root = tk.Tk()
    root.title("AutoClone Tool")
    root.geometry("400x300")

    label = tk.Label(root, text="เลือกประเทศที่ต้องการ Clone", font=("Arial", 14))
    label.pack(pady=10)

    countries = ["Thailand", "Japan", "USA", "Germany"]

    for country in countries:
        btn = tk.Button(root, text=country, command=lambda c=country: open_country_window(c), width=20)
        btn.pack(pady=5)

    root.mainloop()

def open_country_window(country):
    """ เปิดหน้าต่างใหม่สำหรับ Clone ประเทศที่เลือก """
    new_window = tk.Toplevel()
    new_window.title(f"AutoClone - {country}")
    new_window.geometry("300x200")

    label = tk.Label(new_window, text=f"เริ่ม Clone สำหรับ {country}", font=("Arial", 14))
    label.pack(pady=10)

    progress = ttk.Progressbar(new_window, orient="horizontal", length=200, mode="indeterminate")
    progress.pack(pady=10)

    clone_button = tk.Button(new_window, text="Start Clone", command=lambda: start_clone(country, progress, new_window), bg="green", fg="white")
    clone_button.pack(pady=10)
