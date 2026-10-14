import bcrypt
import json 

login = input("Введите логин: ")
password = input("Введите пароль: ")

password_bytes = password.encode("utf-8")
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password_bytes, salt)
hashed_decoded = hashed.decode('UTF-8')

print(hashed)

user_data = {
    'name': login,
    'password': hashed_decoded
}

with open('user_data.json', 'w', encoding='utf-8') as jsonFile:
    json.dump(user_data, jsonFile)