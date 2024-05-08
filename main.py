import json
import requests
from tkinter import *

import customtkinter as ctk
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class CurrencyConversion(Base):
    __tablename__ = 'currency_conversions'

    id = Column(Integer, primary_key=True)
    source_currency = Column(String)
    target_currency = Column(String)
    amount = Column(Integer)
    result = Column(String)

engine = create_engine('sqlite:///currency_converter.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def convert_currency(*args, **kwargs):
    source_currency = choice1.get().upper().strip()
    target_currency = choice2.get().upper().strip()
    amount = int(amount_entry.get())
    URL = f"https://api.frankfurter.app/latest?amount={amount}&from={source_currency}&to={target_currency}"

    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            result_text = f"{amount} {source_currency} это {data['rates'][target_currency]} {target_currency}"
            result_label.configure(text=result_text)

            session = Session()
            conversion = CurrencyConversion(
                source_currency=source_currency,
                target_currency=target_currency,
                amount=amount,
                result=result_text
            )
            session.add(conversion)
            session.commit()
            session.close()

        else:
            result_label.configure(text=f'Не получилось получить данные, ошибка: {response.status_code}')
    except requests.exceptions.RequestException as e:

        result_label.configure(text=f'Произошла ошибка')

root = ctk.CTk()
root.title('Currency Converter')
root.geometry = ('500x400')

source_label = ctk.CTkLabel(root, text='Что перевести')
source_label.pack()
choice1 = ctk.CTkComboBox(master=root, values=['AUD', 'BGN', 'BRL', 'CAD', 'CNY', 'MXN', 'EUR', 'USD', 'INR', 'JPY', 'TRY'])
choice1.pack()

target_label = ctk.CTkLabel(root, text='Во что перевести')
target_label.pack()
choice2 = ctk.CTkComboBox(master=root, values=['AUD', 'BGN', 'BRL', 'CAD', 'CNY', 'MXN', 'EUR', 'USD', 'INR', 'JPY', 'TRY'])
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
