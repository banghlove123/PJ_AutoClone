import hashlib

# 🔐 เก็บรหัสผ่านที่ถูกเข้ารหัส SHA256
STORED_PASSWORD_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbddfbdbe45f24c7b2c21"  # "password"

def verify_password(input_password):
    """ ตรวจสอบรหัสผ่านโดยใช้ SHA256 """
    hashed_input = hashlib.sha256(input_password.encode()).hexdigest()
    return hashed_input == STORED_PASSWORD_HASH
