# import requests
# from time import perf_counter

# v = input("Валюта: ").upper()
# def count():
#     i=0
#     start = perf_counter()
#     for i in range(28):
#         start1 = perf_counter()
#         if v == requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]["currency"]:
#             end1=perf_counter()
#             if "saleRate" in requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]:
#                 print(f'Валюта\n{requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]["currency"]}')
#                 print(f'Продажа по курсу Приватбанка\n{requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]["saleRate"]}')
#                 print(f'Покупка по курсу Приватбанка\n{requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]["purchaseRate"]}')
#                 print(f'Продажа по курсу НБУ\n{requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]["saleRateNB"]}')
#                 print(f'Покупка по курсу НБУ\n{requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]["purchaseRateNB"]}')
#             else:
#                 print(f'Валюта\n{requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]["currency"]}')
#                 print(f'Продажа по курсу НБУ\n{requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]["saleRateNB"]}')
#                 print(f'Покупка по курсу НБУ\n{requests.get("https://api.privatbank.ua/p24api/exchange_rates?date=12.07.2023").json()["exchangeRate"][i]["purchaseRateNB"]}')
#             end = perf_counter()
#             print(end1-start1)
#             print(end-start1)
#             print(end-start)
#             break
#         # else:
#         #     print("no")
#         i+=1

# count()


# import sqlite3

# connect = sqlite3.connect("gamdb.db")
# cursor = connect.cursor()


# games_table = "videogames"
# create_table_query = f"""CREATE TABLE IF NOT EXISTS {games_table} (id INTEGER PRIMARY KEY AUTOINCREMENT, videogames TEXT, genre TEXT);"""
# cursor.execute(create_table_query)

# reviews_table = "reviews"
# create_table_query = f"""CREATE TABLE IF NOT EXISTS {reviews_table} (id INTEGER PRIMARY KEY AUTOINCREMENT,rev_user TEXT, rev_text TEXT, videogames_id INTEGER, FOREIGN KEY (videogames_id) REFERENCES videogames (id));"""
# cursor.execute(create_table_query)

# list_of_games = [
#     ("Cyberpunk 2077", "RPG"),
#     ("Dead Space", "Horror")
# ]

# rev_list = [
#     ('Bob', 'best game ever 10/10'),
#     ('JOHN2323', '8/10' )
# ]


# # cursor.executemany('''INSERT INTO videogames (games, genre) VALUES(?,?)''', [(i[0], i[1]) for i in list_of_games])
# # connect.commit()

# cursor.executemany(f'''INSERT INTO {games_table} (videogames, genre) VALUES (?,?)''', [(i[0], i[1]) for i in list_of_games])
# cursor.executemany(f'''INSERT INTO {reviews_table} (rev_user, rev_text, videogames_id) VALUES (?,?,?)''', [(i[0], i[1], idx+1) for idx, i in enumerate(rev_list)])

# def get_question_answers():
#     cursor.execute(f'''SELECT {games_table}.id, videogames, genre, rev_user, rev_text FROM {games_table} 
#                       JOIN {reviews_table} ON {games_table}.id = {reviews_table}.videogames_id''')
#     result = cursor.fetchall()
#     for row in result:
#         print(f"Game: {row[1]}")
#         print(f"Genre: {row[2]}")
#         print(f"User: {row[3]}")
#         print(f'Review: {row[4]}')
#         print("\n")

# get_question_answers()

# import sqlite3

# connect = sqlite3.connect("userss.db")
# cursor = connect.cursor()

# user_table = "users"
# create_table_query = f"""CREATE TABLE IF NOT EXISTS {user_table} (nickname TEXT, password TEXT);"""
# cursor.execute(create_table_query)


# nickname = input('Nickname: ')
# password = input('Password: ')

# info = cursor.execute('SELECT * FROM users')
# if info.fetchone() is None: 
#         cursor.execute("INSERT INTO users (nickname, password) VALUES (?, ?)", (nickname, password))
#         connect.commit()
# else:
#         print('cxcz')


from keyboard import press_and_release
from time import sleep
import pyautogui, pyperclip

def paste(text: str):    
    pyperclip.copy(text)
    press_and_release('ctrl + v')

def type(text: str, interval=0.0):    
    buffer = pyperclip.paste()
    if not interval:
        paste(text)
    else:
        for char in text:
            paste(char)
            sleep(interval)
    pyperclip.copy(buffer)

type('Hello World!', 0.1)# ExampleHello World!