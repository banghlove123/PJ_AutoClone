import uiautomator2 as u2
import time


class Bot:
    def __init__(self, log_callback=None):
        self.d = u2.connect()
        self.log_callback = log_callback
        self.log("📲 Connected to device")
        time.sleep(3)
        self.d.shell("settings put system accelerometer_rotation 0")   
        self.d.shell("settings put system screen_brightness_mode 0")
        self.d.shell("settings put system screen_brightness 255")
        self.d.shell("settings put system screen_off_timeout 1800000")
        
        

    
    def log(self, message):
        # ฟังก์ชันส่งข้อความไปที่ UI
        if self.log_callback:
            self.log_callback(message)
        print(message)

    def wait_for_text(self, text, timeout=5):
        start_time = time.time()
        while not self.d(text=text).exists:
            if time.time() - start_time > timeout:
                self.log(f"⏳ หมดเวลา: ไม่พบ '{text}'")
                return False
            time.sleep(2)
        self.log(f"✅ พบข้อความ: {text}")
        return True

    def click(self, text):
        self.d.shell("settings put system accelerometer_rotation 0")   
        self.d.shell("settings put system screen_brightness_mode 0")
        time.sleep(1)
        element = self.d(text=text)
        if element.exists:
            bounds = element.info["bounds"]
            self.log(f"👉 คลิก: {text} | พิกัด: {bounds}")
            element.click()
            time.sleep(1)
            return True
        else:
            self.log(f"❌ ไม่พบข้อความ: {text}")
            return False

    def open_settings_and_search(self, query):
        
        self.d.shell("pm clear com.android.settings")
        self.d.app_start("com.android.settings")
        self.d.press("search")
        self.d.send_keys(query)
        time.sleep(1)
        self.log(f"🔍 ค้นหา: {query}")

    def optimize_gotsync(self):
        # """ตั้งค่า GOTSync ให้ใช้พลังงานแบบ 'ไม่จำกัด'"""
        self.open_settings_and_search("GOTSync1")
        steps = ["GOTSync", "แบตเตอรี่", "ไม่จำกัด"]
        for step in steps:
            if not self.wait_for_text(step):
                return False
            self.click(step)
        self.log("✅ ตั้งค่า GOTSync เป็น 'ไม่จำกัด' สำเร็จ")
        return True

    def configure_code(self,text):
        self.d.app_start("th.co.gosoft.scmobile.got.gotsync")
        if self.wait_for_text("ตกลง"):
            self.click("ตกลง")
        time.sleep(5)
        self.d.send_keys(text, clear=True)

    def enable_unknown_sources(self):
        # """เปิดให้สามารถติดตั้งแอปจากแหล่งที่ไม่รู้จัก"""
        self.open_settings_and_search("ติดตั้งแอปที่ไม่รู้จัก")
        if self.wait_for_text("การเข้าถึงพิเศษ"):
            self.click("การเข้าถึงพิเศษ")
            if self.wait_for_text("ติดตั้งแอปที่ไม่รู้จัก"):
                self.click("ติดตั้งแอปที่ไม่รู้จัก")
                time.sleep(5)
                if self.wait_for_text("SOTI MobiControl"):
                    self.click("SOTI MobiControl")
        self.log("✅ เปิดการติดตั้งจากแหล่งที่ไม่รู้จักสำเร็จ")

    def add_language(self):
        # """เพิ่มภาษา English (United States)"""
        self.open_settings_and_search("ภาษา")
        steps = [
            "การจัดการทั่วไป",
            "ภาษา",
            "เพิ่มภาษา",
            "English",
            "United States",
            "ใช้ค่าปัจจุบัน",
        ]
        for step in steps:
            if not self.wait_for_text(step):
                return False
            self.click(step)
        self.log("✅ เพิ่มภาษา English (United States) สำเร็จ")
        return True

    def configure_side_button(self):
        # """ตั้งค่าปุ่มด้านข้างให้เปิดเมนูปิดเครื่อง"""
        self.open_settings_and_search("ปุ่มด้านข้าง")

        steps = ["คุณสมบัติขั้นสูง", "เมนูปิดเครื่อง"]

        for step in steps:
            if not self.wait_for_text(step):
                print(f"❌ ไม่พบ: {step}")
                return False  # หยุดการทำงานถ้าข้อความไม่พบ
            self.click(step)

        print("✅ ตั้งค่าปุ่มด้านข้างสำเร็จ")
        return True  # สำเร็จทุกขั้นตอน

    def configure_keyboard(self):
        # """ตั้งค่าแป้นพิมพ์ Gboard"""
        self.open_settings_and_search("รายการแป้นพิมพ์และแป้นพิมพ์พื้นฐาน")

        steps = [
            "การจัดการทั่วไป",
            "รายการแป้นพิมพ์และแป้นพิมพ์พื้นฐาน",
            "Gboard",
            "ค่ากำหนด",
            "ความสูงของแป้นพิมพ์",
            "สูงมาก",
        ]

        for step in steps:
            if not self.wait_for_text(step):
                print(f"❌ ไม่พบ: {step}")
                return False  # จบการทำงานถ้าข้อความไม่พบ
            self.click(step)

        # กด Back หลังจากตั้งค่าความสูงแป้นพิมพ์
        self.d.press("back")

        # ดำเนินการตั้งค่าการพิมพ์แบบเลื่อนผ่าน
        extra_steps = ["การพิมพ์แบบเลื่อนผ่าน", "เปิดใช้การเลื่อนนิ้วเพื่อพิมพ์"]

        for step in extra_steps:
            if not self.wait_for_text(step):
                print(f"❌ ไม่พบ: {step}")
                return False
            self.click(step)

        print("✅ ตั้งค่าแป้นพิมพ์ Gboard สำเร็จ")
        return True  # สำเร็จทุกขั้นตอน

    def security(self):
        self.d.shell("adb shell")
        self.d.shell("locksettings set-pin 123456")  # ล็อค
        self.d.shell("am start -a android.settings.WIFI_SETTINGS")  # หน้า wifi
        self.d.shell("settings put system accelerometer_rotation 1")
        self.d.shell("pm uninstall com.github.uiautomator")  # ลบแอป
        print(f"✅ จบการทำงาน")
