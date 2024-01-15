import customtkinter as ctk
from tkinter import messagebox
import time
import threading

# Глобальные переменные для отслеживания попыток и времени блокировки
attempt_counter = 0
lock_time = None
password = "1234"

def decrypt_text(input_text):
    # Разделяем входной текст на абзацы и инвертируем каждый абзац
    decrypted_paragraphs = [paragraph[::-1] for paragraph in input_text.split('\n')]
    # Объединяем абзацы обратно, сохраняя переносы строк
    return '\n'.join(decrypted_paragraphs)

def show_decryptor():
    decryptor_window = ctk.CTkToplevel()
    decryptor_window.title("Дешифратор")
    decryptor_window.geometry("600x400")

    label = ctk.CTkLabel(decryptor_window, text="Дешифратор", font=("Helvetica", 25))
    label.pack(padx=10, pady=10)

    # Используем CTkTextbox для многострочного ввода
    input_text = ctk.CTkTextbox(decryptor_window, font=("Helvetica", 18), width=400, height=100)
    input_text.pack(pady=10)

    output_label = ctk.CTkLabel(decryptor_window, text="", font=("Helvetica", 18), wraplength=400)
    output_label.pack(pady=10)

    def handle_decrypt():
        # Получаем текст из поля ввода, обрабатываем его и выводим результат
        text_to_decrypt = input_text.get("1.0", "end-1c")  # Получаем весь текст из Textbox
        decrypted_text = decrypt_text(text_to_decrypt)
        output_label.configure(text=decrypted_text)

    decrypt_button = ctk.CTkButton(decryptor_window, text='Дешифровать', command=handle_decrypt,
                                   font=("Helvetica", 16), fg_color="#0078D7", text_color="white",
                                   width=200, height=40, corner_radius=15, border_width=2, border_color="#0053BA",
                                   hover_color="#0053BA")
    decrypt_button.pack(pady=10)

    # Исправляем функцию копирования для правильной работы
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

    p = password_entry.get()  # Получение пароля из поля ввода
    if p == password:
        attempt_counter = 0  # Сброс счётчика попыток при успешном вводе
        root.withdraw()  # Скрытие основного окна
        show_decryptor()  # Показ окна дешифратора
    else:
        attempt_counter += 1
        label.configure(text="Пароль неверный", bg_color="red")
        if attempt_counter >= 5:
            lock_time = time.time()
            messagebox.showerror("Заблокировано", "Слишком много неверных попыток. Попробуйте через 30 секунд.")

def check_lock_status():
    global lock_time
    if lock_time and time.time() - lock_time < 30:
        # Если система заблокирована, сообщаем пользователю
        remaining_time = 30 - (time.time() - lock_time)
        messagebox.showerror("Заблокировано", f"Попробуйте через {int(remaining_time)} секунд")
        return True
    lock_time = None  # Сброс времени блокировки
    return False

root = ctk.CTk()
root.geometry("600x400")  # Задаем размер окна
root.title("Система входа")  # Задаем заголовок окна

# Создание и настройка текстовой метки для приветствия или сообщения о статусе
label = ctk.CTkLabel(root, text="Введите пароль для входа", font=("Helvetica", 18))
label.pack(pady=20)

# Создание поля для ввода пароля
password_entry = ctk.CTkEntry(root, width=200, height=40, font=("Helvetica", 18), show="*")
password_entry.pack(pady=10)

# Создание кнопки для подтверждения введенного пароля
submit_button = ctk.CTkButton(root, text="Войти", command=show, width=200, height=40, font=("Helvetica", 16))
submit_button.pack(pady=20)

# Запуск главного цикла приложения
root.mainloop()
