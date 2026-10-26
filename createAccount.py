import bcrypt
import json 

role = input("Введите роль (admin / moder): ")
login = input("Введите логин: ")
password = input("Введите пароль: ")

file_name = 'user_data.json' if role == 'admin' else 'moder_data.json'

password_bytes = password.encode("utf-8")
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password_bytes, salt)
hashed_decoded = hashed.decode('UTF-8')

print(hashed)

user_data = {
    'name': login,
    'password': hashed_decoded
}

with open(file_name, 'w', encoding='utf-8') as jsonFile:
    json.dump(user_data, jsonFile)