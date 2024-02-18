import customtkinter as ctk
from tkinter import messagebox
import time

attempt_counter = 0
lock_time = None
password = "1234"

def decrypt_text(input_text):
    decrypted_paragraphs = [paragraph[::-1] for paragraph in input_text.split('\n')]
    return '\n'.join(decrypted_paragraphs)

def show_decryptor():
    decryptor_window = ctk.CTkToplevel()
    decryptor_window.title("Шифратор")
    decryptor_window.geometry("600x400")

    label = ctk.CTkLabel(decryptor_window, text="Шифратор", font=("Helvetica", 25))
    label.pack(padx=10, pady=10)

    input_text = ctk.CTkTextbox(decryptor_window, font=("Helvetica", 18), width=400, height=100)
    input_text.pack(pady=10)

    output_label = ctk.CTkLabel(decryptor_window, text="", font=("Helvetica", 18), wraplength=400)
    output_label.pack(pady=10)

    def handle_decrypt():
        text_to_decrypt = input_text.get("1.0", "end-1c")  # Получаем весь текст из Textbox
        decrypted_text = decrypt_text(text_to_decrypt)
        output_label.configure(text=decrypted_text)

    decrypt_button = ctk.CTkButton(decryptor_window, text='Зашифровать', command=handle_decrypt,
                                   font=("Helvetica", 16), fg_color="#0078D7", text_color="white",
                                   width=200, height=40, corner_radius=15, border_width=2, border_color="#0053BA",
                                   hover_color="#0053BA")
    decrypt_button.pack(pady=10)

    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(output_label.cget("text"))
        messagebox.showinfo("Копирование", "Текст скопирован в буфер обмена")

    copy_button = ctk.CTkButton(decryptor_window, text='Копировать', command=copy_to_clipboard,
                                font=("Helvetica", 16), fg_color="#0078D7", text_color="white",
                                width=200, height=40, corner_radius=15, border_width=2, border_color="#0053BA",
                                hover_color="#0053BA")
    copy_button.pack(pady=10)

def show():
    global attempt_counter, lock_time, password
    if check_lock_status():
        return

    p = password_entry.get()
    if p == password:
        attempt_counter = 0
        root.withdraw()
        show_decryptor()
    else:
        attempt_counter += 1
        label.configure(text="Пароль неверный", bg_color="red")
        if attempt_counter >= 5:
            lock_time = time.time()
            messagebox.showerror("Заблокировано", "Слишком много неверных попыток. Попробуйте через 30 секунд.")

def check_lock_status():
    global lock_time
    if lock_time and time.time() - lock_time < 30:
        remaining_time = 30 - (time.time() - lock_time)
        messagebox.showerror("Заблокировано", f"Попробуйте через {int(remaining_time)} секунд")
        return True
    lock_time = None
    return False

root = ctk.CTk()
root.geometry("600x400")
root.title("Система входа")

label = ctk.CTkLabel(root, text="Введите пароль для входа", font=("Helvetica", 18))
label.pack(pady=20)

password_entry = ctk.CTkEntry(root, width=200, height=40, font=("Helvetica", 18), show="*")
password_entry.pack(pady=10)

submit_button = ctk.CTkButton(root, text="Войти", command=show, width=200, height=40, font=("Helvetica", 16))
submit_button.pack(pady=20)

root.mainloop()
