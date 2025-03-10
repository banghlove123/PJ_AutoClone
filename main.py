import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import functions as SumTest
import sys
from io import StringIO
import threading

class GOTControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Setup Tablet ")
        self.root.geometry("400x600")
        root.resizable(False, False)

        # พื้นที่แสดงผล
        self.output_text = scrolledtext.ScrolledText(root, width=45, height=25, wrap=tk.WORD)
        self.output_text.pack(pady=5)

        # Label แสดงสถานะ
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(root, textvariable=self.status_var)
        self.status_label.pack(pady=5)
        self.status_var.set("สถานะ: พร้อมใช้งาน") # ตั้งค่าสถานะเริ่มต้น

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=500, mode='indeterminate')
        self.progress.pack(pady=5)

        # Input Box
        self.input_var = tk.StringVar()
        tk.Label(root, text="กรอกรหัสร้าน").pack()
        self.input_entry = tk.Entry(root, textvariable=self.input_var, validate="key", validatecommand=(root.register(self.validate_input), "%P"))
        self.input_entry.pack(pady=5)

        # ปุ่มล็อคและปลดล็อค
        self.lock_button = tk.Button(root, text=" ล็อค", command=self.lock_input)
        self.lock_button.pack(pady=5)

        self.unlock_button = tk.Button(root, text=" ปลดล็อค", command=self.unlock_input)
        self.unlock_button.pack(pady=5)
        self.unlock_button.pack_forget()

        # ปุ่มควบคุม
        self.start_button = tk.Button(root, text="Start Robot Setup GOT", command=self.start_setup, state=tk.DISABLED) # ปิดปุ่มในตอนแรก
        self.start_button.pack(pady=5)

        # เก็บ stdout เดิม
        self.original_stdout = sys.stdout
        self.string_io = StringIO()
        sys.stdout = self.string_io

        self.bot = None  # ยังไม่ initialize bot จนกดปุ่ม
        self.log_output("✅ พร้อมใช้งาน กดปุ่ม 'Start Robot Setup GOT' เพื่อเริ่มตั้งค่า")
        self.stop_event = threading.Event()

    def validate_input(self, value):
        return value.isdigit() and len(value) <= 6

    def lock_input(self):
        self.input_entry.config(state='disabled')
        self.lock_button.pack_forget()
        self.unlock_button.pack()
        self.start_button.config(state=tk.NORMAL) # เปิดใช้งานปุ่ม
        self.status_var.set("สถานะ: ล็อคการแก้ไขรหัสร้าน") # เปลี่ยนสถานะ

    def unlock_input(self):
        self.input_entry.config(state='normal', validate="key", validatecommand=(self.root.register(self.validate_input), "%P"))
        self.unlock_button.pack_forget()
        self.lock_button.pack()
        self.start_button.config(state=tk.DISABLED) # ปิดใช้งานปุ่ม
        self.input_var.set("")
        self.status_var.set("สถานะ: พร้อมใช้งาน") # เปลี่ยนสถานะ

    def start_setup(self):
        if not self.initialize_bot():
            return
        self.stop_event.clear()
        self.run_task(self.run_configuration)
        self.status_var.set("สถานะ: กำลังตั้งค่า") # เปลี่ยนสถานะ

    def initialize_bot(self):
        try:
            self.bot = SumTest.Bot(log_callback=self.log_output)
            self.log_output("✅ อุปกรณ์เชื่อมต่อเรียบร้อย")
            self.status_var.set("สถานะ: เชื่อมต่ออุปกรณ์สำเร็จ") # เปลี่ยนสถานะ
            return True
        except Exception as e:
            self.log_output(f"❌ ไม่สามารถเชื่อมต่ออุปกรณ์: {str(e)}")
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถเชื่อมต่ออุปกรณ์: {str(e)}")
            self.status_var.set("สถานะ: ไม่สามารถเชื่อมต่ออุปกรณ์") # เปลี่ยนสถานะ
            return False

    def log_output(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.string_io.seek(0)
        self.string_io.truncate(0)

    def run_task(self, task):
        threading.Thread(target=self.run_with_progress, args=(task,), daemon=True).start()

    def run_with_progress(self, task):
        try:
            self.progress.start()
            task()
            if not self.stop_event.is_set():
                self.log_output("✅ การตั้งค่าเสร็จสมบูรณ์")
                messagebox.showinfo("สำเร็จ", "การตั้งค่าเสร็จสมบูรณ์")
                self.status_var.set("สถานะ: ตั้งค่าสำเร็จ") # เปลี่ยนสถานะ
        except Exception as e:
            error_message = f"❌ เกิดข้อผิดพลาด: {str(e)}"
            self.log_output(error_message)
            messagebox.showerror("ข้อผิดพลาด", error_message)
            self.status_var.set("สถานะ: เกิดข้อผิดพลาด") # เปลี่ยนสถานะ
        finally:
            self.progress.stop()

    def run_configuration(self):
        text = self.input_var.get()
        if not text:
                self.log_output("❌ กรุณากรอกรหัสร้านก่อน")
                return
        try:
            self.unlock_button.config(state='disabled')
            self.start_button.config(state=tk.DISABLED) # ปิดใช้งานปุ่ม
            self.log_output("🔧 กำลังตั้งค่าอุปกรณ์")
            self.bot.configure_side_button()
            self.bot.enable_unknown_sources()
            self.bot.add_language()
            self.bot.configure_keyboard()
            self.bot.optimize_gotsync()
            self.bot.configure_code(text=text)
            self.bot.security()
            self.unlock_button.config(state='normal')
            self.start_button.config(state=tk.NORMAL)
        except Exception as e:
            self.stop_event.set()
            raise e

    def __del__(self):
        sys.stdout = self.original_stdout

if __name__ == "__main__":
    root = tk.Tk()
    app = GOTControlApp(root)
    root.mainloop()
