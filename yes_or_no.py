import psutil
import time
import tkinter as tk
import os
import threading
import pygetwindow as gw  # pip install pygetwindow

blocked_apps = ['telegram.exe']
already_asked = set()


def show_popup(app_name, exe_path):
    def on_yes():
        already_asked.add(exe_path)
        if exe_path and os.path.exists(exe_path):
            try:
                os.startfile(exe_path)
                print(f"{app_name} qayta ishga tushirildi.")
            except Exception as e:
                print(f"{app_name} ni qayta ochishda xatolik: {e}")
        root.destroy()

    def on_no():
        print(f"{app_name} bloklandi.")
        root.destroy()

    root = tk.Tk()
    root.title("Diqqat!")
    root.geometry("350x150")
    root.attributes("-topmost", True)

    tk.Label(root, text=f"'{app_name}' ilovasiga kirishni rostan ham xohlaysizmi?",
             wraplength=300).pack(pady=20)
    tk.Button(root, text="Ha", width=10, command=on_yes).pack(side="left", padx=50, pady=10)
    tk.Button(root, text="Yo‘q", width=10, command=on_no).pack(side="right", padx=50, pady=10)

    root.mainloop()


def monitor_apps():
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                pname = proc.info['name']
                exe_path = proc.info['exe']

                if not pname or not exe_path:
                    continue

                if pname.lower() in blocked_apps:
                    # ❗ faqat oyna ochilganda tekshirish
                    windows = gw.getWindowsWithTitle("Telegram")
                    if windows and exe_path not in already_asked:
                        print(f"{pname} oynasi ochildi, ruxsat so‘ralmoqda.")

                        try:
                            proc.terminate()
                            proc.wait(timeout=3)
                        except Exception as e:
                            print(f"O‘chirishda xatolik: {e}")

                        threading.Thread(target=show_popup,
                                         args=(pname, exe_path),
                                         daemon=True).start()

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        time.sleep(1)


if __name__ == "__main__":
    monitor_apps()
