from datetime import datetime
import random

def generate_id():
    today = datetime.today().strftime('%Y%m%d')  # YYYYMMDD 형식
    random_digits = f"{random.randint(0, 9999):04d}"  # 4자리 랜덤 숫자 (0000~9999)
    return today + random_digits

