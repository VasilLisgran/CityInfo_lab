from tkinter import *
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
from tkinter.simpledialog import askstring
import json
import os
import bcrypt

width = 500
height = 450
root = Tk()
root.title("City Info")
root.geometry(f"{width}x{height}")

CITIES_FILE = 'cities.json'
ADMIN_FILE = 'user_data.json'
MODER_FILE = 'moder_data.json'

cities = []

def loadCities():
    if os.path.exists(CITIES_FILE):
        with open(CITIES_FILE, 'r', encoding='utf-8') as file:
            cities.extend(json.load(file))
    for el in cities:
        el['population'] = int(el['population'])
        el['special'] = el.get('special', False)

def saveCities():
    with open(CITIES_FILE, 'w', encoding='utf-8') as file:
        json.dump(cities, file, ensure_ascii=False)

def findCity(title):
    for el in cities:
        if el['city'].lower() == title.strip().lower():
            return el
    return None

def userFile(role):
    return ADMIN_FILE if role == 'admin' else MODER_FILE

def loadUser(role):
    if not os.path.exists(userFile(role)):
        return None
    with open(userFile(role), 'r', encoding='utf-8') as file:
        return json.load(file)

def saveUser(role, name, password):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    user_data = {
        'name': name,
        'password': hashed.decode('UTF-8')
    }
    with open(userFile(role), 'w', encoding='utf-8') as jsonFile:
        json.dump(user_data, jsonFile)

def showStats():
    total = len(cities)
    millionaires = 0
    small = 0

    for el in cities:
        if el['population'] >= 1000000:
            millionaires += 1
        elif el['population'] < 20000:
            small += 1

    other = total - millionaires - small

    showinfo(title='Статистика', message=
             f"Всего записей в базе: {total}\n"
             f"Городов-миллионников: {millionaires}\n"
             f"Городов менее 20 тыс.: {small}\n"
             f"Иных городов: {other}")

def changePassword(role, parent):
    user = loadUser(role)
    old = askstring("Смена пароля", "Введите старый пароль:", show='*', parent=parent)
    if old is None:
        return
    if not bcrypt.checkpw(old.encode("utf-8"), user['password'].encode('utf-8')):
        showerror(title='Ошибка!', message='Старый пароль неверный!')
        return
    new = askstring("Смена пароля", "Введите новый пароль:", show='*', parent=parent)
    if not new:
        return
    saveUser(role, user['name'], new)
    showinfo(title='Готово', message='Пароль изменён!')

def resetModerPassword(parent):
    new = askstring("Сброс пароля", "Новый пароль модератора:", show='*', parent=parent)
    if not new:
        return
    user = loadUser('moder')
    name = user['name'] if user else 'moder'
    saveUser('moder', name, new)
    showinfo(title='Готово', message=f'Пароль модератора сброшен. Логин: {name}')

def panel(role):
    window = Toplevel(root)
    title = "Админ панель" if role == 'admin' else "Панель модератора"
    window.title(title)
    window.geometry(f"{width}x{height}")
    label = Label(window, text=title)
    specialVar = BooleanVar(master=window)

    def readPopulation():
        try:
            population = int(entryPopulation.get())
            if population < 0:
                raise ValueError
            return population
        except ValueError:
            showerror(title='Ошибка!', message='Неправильно введено население!')
            return None

    def addCity():
        city = entryTitle.get().strip()
        if city == '':
            showerror(title='Ошибка!', message='Введите название города!')
            return
        population = readPopulation()
        if population is None:
            return
        if findCity(city) is not None:
            showerror(title='Ошибка!', message='Такой город уже есть!')
            return

        cities.append({'city': city, 'population': population, 'special': specialVar.get()})
        saveCities()
        showinfo(title='Готово', message='Город добавлен!')

    def editCity():
        el = findCity(entryTitle.get())
        if el is None:
            showwarning(title='Предупреждение', message='Не найдено!')
            return
        population = readPopulation()
        if population is None:
            return

        if role == 'moder' and abs(population - el['population']) * 100 > el['population'] * 5:
            showerror(title='Ошибка!', message='Модератор может менять население не более чем на 5%!')
            return

        el['population'] = population
        saveCities()
        showinfo(title='Готово', message='Население изменено!')

    entryTitle = Entry(window, width=17)
    entryPopulation = Entry(window, width=17)
    labelTitle = Label(window, text="Город")
    labelPopulation = Label(window, text="Население")
    addButton = Button(window, width=25, text="Добавить город", command=addCity)
    editButton = Button(window, width=25, text="Изменить население", command=editCity)
    statsButton = Button(window, width=25, text="Статистика", command=showStats)
    passButton = Button(window, width=25, text="Сменить пароль",
                        command=lambda: changePassword(role, window))

    label.grid(row=0, column=1)
    labelTitle.grid(row=1, column=0)
    entryTitle.grid(row=1, column=1)
    labelPopulation.grid(row=2, column=0)
    entryPopulation.grid(row=2, column=1)
    addButton.grid(row=3, column=1)
    editButton.grid(row=4, column=1)
    statsButton.grid(row=5, column=1)
    passButton.grid(row=6, column=1)

    if role == 'admin':
        def deleteCity():
            el = findCity(entryTitle.get())
            if el is None:
                showwarning(title='Предупреждение', message='Не найдено!')
                return
            if askyesno(title='Удаление', message=f"Удалить город {el['city']}?"):
                cities.remove(el)
                saveCities()
                showinfo(title='Готово', message='Город удалён!')

        def setSpecial():
            el = findCity(entryTitle.get())
            if el is None:
                showwarning(title='Предупреждение', message='Не найдено!')
                return
            el['special'] = specialVar.get()
            saveCities()
            showinfo(title='Готово', message='Особый статус сохранён!')

        specialCheck = Checkbutton(window, text="Особый статус", variable=specialVar)
        specialButton = Button(window, width=25, text="Применить статус", command=setSpecial)
        deleteButton = Button(window, width=25, text="Удалить город", command=deleteCity)
        resetButton = Button(window, width=25, text="Сбросить пароль модератора",
                             command=lambda: resetModerPassword(window))

        specialCheck.grid(row=7, column=1)
        specialButton.grid(row=8, column=1)
        deleteButton.grid(row=9, column=1)
        resetButton.grid(row=10, column=1)

def authWindow(role):
    def auth():
        user = loadUser(role)
        if user is None:
            if role == 'admin':
                showerror(title='Ошибка!', message='Аккаунт админа не создан. Запустите createAccount.py')
            else:
                showerror(title='Ошибка!', message='Пароль модератора ещё не задан. Его задаёт админ.')
            return

        entered_login = entryName.get()
        entered_password = entryPassword.get()
        password_bytes = entered_password.encode("utf-8")

        if entered_login == user['name'] and bcrypt.checkpw(password_bytes, user['password'].encode('utf-8')):
            window.destroy()
            panel(role)
            return
        showerror(title='Ошибка!', message='Неверный логин или пароль!')

    window = Toplevel(root)
    window.title("Авторизация")
    window.geometry(f"{width}x{height}")
    label = Label(window, text="Авторизация")
    labelName = Label(window, text="Логин")
    labelPassword = Label(window, text="Пароль")
    entryName = Entry(window)
    entryPassword = Entry(window, show="*")
    entryBtn = Button(window, text="Нажать", width=17, command=auth)

    label.pack()
    labelName.pack()
    entryName.pack()
    labelPassword.pack()
    entryPassword.pack()
    entryBtn.pack()

def search():
    city = findCity(entryMain.get())

    if city is None:
        cityTitleLabel.config(text="")
        cityPopulationLabel.config(text="")
        citySpecialLabel.config(text="")
        showwarning(title='Предупреждение', message='Не найдено!')
        return

    cityTitleLabel.config(text=f"Название: {city['city']}")
    cityPopulationLabel.config(text=f"Население: {city['population']}")
    citySpecialLabel.config(text=f"Особый статус: {'✔' if city['special'] else '—'}")

labelMain = Label(text="Введите название города")
entryMain = Entry()
entryBtn = Button(text="Найти", width=17, command=search)
cityTitleLabel = Label()
cityPopulationLabel = Label()
citySpecialLabel = Label()
adminBtn = Button(text="Админ аккаунт", width=50, command=lambda: authWindow('admin'))
moderBtn = Button(text="Модер аккаунт", width=50, command=lambda: authWindow('moder'))

labelMain.pack()
entryMain.pack()
entryBtn.pack()
cityTitleLabel.pack()
cityPopulationLabel.pack()
citySpecialLabel.pack()
adminBtn.pack(side=BOTTOM)
moderBtn.pack(side=BOTTOM)

loadCities()
root.mainloop()