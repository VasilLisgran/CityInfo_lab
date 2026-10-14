from tkinter import *

width = 500
height = 450
root = Tk()
root.title("City Info")
root.geometry(f"{width}x{height}")

def adminWindow():
    window = Tk()
    window.title("Авторизация")
    window.geometry(f"{width}x{height}")
    label = Label(window, text="Авторизация")
    entryName = Entry(window, text="Введите логин")
    entryPassword = Entry(window, text="Введите пароль")
    entryBtn = Button(window, text="Нажать", width=17)

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