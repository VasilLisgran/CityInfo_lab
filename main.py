from tkinter import *
from tkinter.messagebox import showerror, showwarning, showinfo
import json
import bcrypt

width = 500
height = 450
root = Tk()
root.title("City Info")
root.geometry(f"{width}x{height}")

cities = []

def adminPanel():
    window = Tk()
    window.title("Админ панель")
    window.geometry(f"{width}x{height}")
    label = Label(window, text="Админ панель")

    def addCity():
        city = entryTitle.get()
        population = entryPopulatuon.get()

        if isinstance(int(population), int):
            cities_dict = {}
            cities_dict['city'] = city
            cities_dict['population'] = population
            cities.append(cities_dict)

            print(cities)

            with open('cities.json', 'w') as file:
                json.dump(cities, file)
        else:
            showerror(window, title='Ошибка!', message='Неправильно введено население!')

    entryTitle = Entry(window, width=17, text="Введите название города")
    entryPopulatuon = Entry(window, width=17, text="Введите население города")
    addButton = Button(window, width=17, text="Добавить город", command=addCity)

    label.grid(row=0, column=1)
    entryTitle.grid(row=1, column=0)
    entryPopulatuon.grid(row=2, column=0)
    addButton.grid(row=3, column=0)

def adminWindow():
    def auth():
        entered_login = entryName.get()
        entered_password = entryPassword.get()
        password_bytes = entered_password.encode("utf-8")
            
        with open('user_data.json', 'r') as file:
            json_obj = json.load(file)
            print(json_obj)
            
        if entered_login == json_obj['name'] and bcrypt.checkpw(password_bytes, json_obj['password'].encode('utf-8')):
            window.destroy()
            print('Ok')
            print(json_obj['name'])
            print(f'{password_bytes}')
            adminPanel()
            return
        print('no')
        print(json_obj)
        print(f'{password_bytes}')

    window = Tk()
    window.title("Авторизация")
    window.geometry(f"{width}x{height}")
    label = Label(window, text="Авторизация")
    entryName = Entry(window, text="Введите логин")
    entryPassword = Entry(window, text="Введите пароль")
    entryBtn = Button(window, text="Нажать", width=17, command=auth)
    
    label.pack()
    entryName.pack()
    entryPassword.pack()
    entryBtn.pack()

def search():
    city_title = entryMain.get()
    with open('cities.json') as file:
        json_file = json.load(file)

    for el in json_file:
        if el['city'] == city_title:
            name = city_title
            population = el['population']

            cityTitleLabel = Label(text=f"Название: {name}")
            cityPopulationLabel = Label(text=f"Название: {population}")

            cityTitleLabel.pack()
            cityPopulationLabel.pack()
            return   
    showwarning(title='Предупреждение', message='Не найдено!')   
     
entryMain = Entry(text="Введите название города")
entryBtn = Button(text="Нажать", width=17, command=search)
adminBtn = Button(text="Админ аккаунт", width=50, command=adminWindow)

entryMain.pack()
entryBtn.pack()
adminBtn.pack(side=BOTTOM)

name = "город"
population = "0"
 
root.mainloop()