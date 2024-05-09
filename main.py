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

engine = create_engine('sqlite:///currency_converter.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def convert(from_, to, amount):
    URL = f"https://api.frankfurter.app/latest?amount={amount}&from={from_}&to={to}"
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            result = data['rates'][to]
            single_value = result / amount
            session = Session()
            conversion = session.query(CurrencyConversion).filter(
                CurrencyConversion.source_currency == from_,
                CurrencyConversion.target_currency == to
            ).all()
            if conversion:
                session.delete(conversion[0])
            conversion = CurrencyConversion(
                source_currency=from_,
                target_currency=to,
                amount=single_value,
            )
            session.add(conversion)
            session.commit()
            session.close()
            return result
    except requests.exceptions.RequestException as e:
        session = Session()
        conversion = session.query(CurrencyConversion).filter(
            CurrencyConversion.source_currency == from_,
            CurrencyConversion.target_currency == to
        ).all()
        if conversion:
            result = conversion[0].amount * amount
        else:
            result = 'Ошибка'
        session.close()
        return result


def convert_currency(*args, **kwargs):
    source_currency = choice1.get().upper().strip()
    target_currency = choice2.get().upper().strip()
    amount = int(amount_entry.get())
    
    result = convert(source_currency, target_currency, amount)
    if result == 'Ошибка':
        result_text = 'Ошибка'
    else:
        result_text = f"{amount} {source_currency} это {result} {target_currency}"
    result_label.configure(text=result_text)
  

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
