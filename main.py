from tkinter import *
import hashlib
import json
import bcrypt

width = 500
height = 450
root = Tk()
root.title("City Info")
root.geometry(f"{width}x{height}")

def adminWindow():

    def auth():
        entered_login = entryName.get()
        entered_password = entryPassword.get()
        password_bytes = entered_password.encode("utf-8")
            
        with open('user_data.json', 'r') as file:
            json_obj = json.load(file)
            print(json_obj)
            
        if entered_login == json_obj['name'] and bcrypt.checkpw(password_bytes, json_obj['password'].encode('utf-8')):
            print('Ok')
            print(json_obj['name'])
            print(f'{password_bytes}')
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
    

entryMain = Entry(text="Введите название города")
entryBtn = Button(text="Нажать", width=17)
adminBtn = Button(text="Админ аккаунт", width=50, command=adminWindow)

entryMain.pack()
entryBtn.pack()
adminBtn.pack(side=BOTTOM)

name = "город"
population = "0"

cityTitleLabel = Label(text=f"Название: {name}")
cityPopulationLabel = Label(text=f"Название: {population}")

cityTitleLabel.pack()
cityPopulationLabel.pack()


root.mainloop()