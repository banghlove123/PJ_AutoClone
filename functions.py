import subprocess
import threading
from tkinter import messagebox

def start_clone(country, progress, window):
    """ เริ่มกระบวนการ Clone พร้อม Progress Bar """
    def run_clone():
        try:
            progress.start(10)  # เริ่ม Progress Bar
            ghost_command = r'C:\path\to\ghost32.exe -clone,mode=create,src=1,dst=C:\backup.gho -sure'
            subprocess.run(ghost_command, shell=True, check=True)
            progress.stop()  # หยุด Progress Bar
            messagebox.showinfo("Success", f"Clone สำเร็จสำหรับ {country}!")
        except Exception as e:
            progress.stop()
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
        finally:
            window.destroy()  # ปิดหน้าต่างเมื่อเสร็จสิ้น

    clone_thread = threading.Thread(target=run_clone)
    clone_thread.start()
