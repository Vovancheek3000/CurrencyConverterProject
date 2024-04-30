import os

import json
import requests
import customtkinter as ctk


def convert_currency(*args, **kwargs):
    source_currency = choice1.get().upper().strip()
    target_currency = choice2.get().upper().strip()
    amount = int(amount_entry.get())
    URL = f"https://api.frankfurter.app/latest?amount={amount}&from={source_currency}&to={target_currency}"

    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            result = result_label.configure(text=f"{amount} {source_currency} это {data['rates'][target_currency]} {target_currency}")
        else:
            result = result_label.configure(text=f'Не получилось получит данные, ошибка: {response.status_code}')
    except requests.exceptions.RequestException as e:
        result_label.configure(text=f'Произошла ошибка: {e}')
    return result


root = ctk.CTk()
root.title('Currency Converter')
root.geometry = ('500x400')

source_label = ctk.CTkLabel(root, text='Что перевести')
source_label.pack()
choice1 = ctk.CTkComboBox(master=root, values=['EUR', 'USD', 'MXN'])
choice1.pack()

target_label = ctk.CTkLabel(root, text='Во что перевести')
target_label.pack()
choice2 = ctk.CTkComboBox(master=root, values=['EUR', 'USD', 'MXN'])
choice2.pack()

amount_label = ctk.CTkLabel(root, text='Сколько перевести')
amount_label.pack()
amount_entry = ctk.CTkEntry(master=root)
amount_entry.pack()

convert_button = ctk.CTkButton(root, text='Конвертировать', command=convert_currency)
convert_button.pack()

result_label = ctk.CTkLabel(root, text='')
result_label.pack()

root.mainloop()




