import sqlite3 as sl

# Функция для загрузки данных из файла в телефонную книгу
conn = sl.connect("contacts.db")

# создаем курсор - основной объект выполнения SQL кода
cur = conn.cursor()

# создаем таблицу контактов, если она не создана
cur.execute(""" 
            CREATE TABLE IF NOT EXISTS contacts
            (
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            number TEXT
            );
            """)
conn.commit()

# Функция для сохранения телефонной книги в БД
def save_phone_book():
    conn.commit()

# Функция для просмотра всех контактов в телефонной книге
def view_contacts():
    print("Телефонная книга:")
    cur.execute("SELECT * FROM contacts;")
    contact = cur.fetchall()
    if contact:
        for i in range(len(contact)):
            print(f"{contact[i][0]}. {contact[i][1]} {contact[i][2]}: {contact[i][3]}")
    else:
        print("Телефонная книга пуста.")
    
# Функция для добавления нового контакта
def add_contact(name, surname, number):
    cur.execute("SELECT id FROM contacts ORDER BY id DESC LIMIT 1")
    contact = cur.fetchall()
    if contact:
        cur.execute("INSERT INTO contacts VALUES (?,?,?,?)", (contact[0][0]+1, name, surname, number))
    else:
        cur.execute("INSERT INTO contacts VALUES (?,?,?,?);", (1, name, surname, number))
    print(f"Контакт {name} {surname} добавлен.")

# # Функция для удаления контакта
def delete_contact(id):
    cur.execute("""SELECT name FROM contacts WHERE id = ?""", [id])
    contact = cur.fetchall()
    if contact:
        cur.execute("""DELETE FROM contacts WHERE id = ?""", [id])
        print(f"Контакт c id={id} удален.")
    else:
        print(f"Контакт c id={id} не найден.")

# # Функция для поиска контакта
def find_contact(name):
    cur.execute("SELECT * FROM contacts WHERE name = ?", [name])
    contact = cur.fetchall()
    if contact:
        for i in range(len(contact)):
            print(f"{contact[i][0]}. {contact[i][1]} {contact[i][2]}: {contact[i][3]}")
    else:
        print(f"Контакт {name} не найден.")

# Функция для изменения контакта
def change_contact(id, name, surname, number):
    cur.execute("UPDATE contacts SET name = ?, surname = ?, number = ? WHERE id = ?", (name, surname, number, id))
    print(f"Контакт {name} изменен.")

while True:
    print("\nМеню:")
    print("1. Просмотреть контакты")
    print("2. Добавить контакт")
    print("3. Удалить контакт")
    print("4. Найти контакт")
    print("5. Изменить контакт")
    print("6. Сохранить контакты в файл")
    print("7. Выход")

    choice = input("Выберите действие: ")

    if choice == '1':
        view_contacts()
    elif choice == '2':
        name = input("Введите имя: ")
        surname = input("Введите фамилию: ")
        number = input("Введите номер телефона: ")
        add_contact(name, surname, number)
    elif choice == '3':
        id = input("Введите id контакта, который нужно удалить: ")
        delete_contact(id)
    elif choice == '4':
        name = input("Введите имя контакта, который нужно найти: ")
        find_contact(name)
    elif choice == '5':
        id = input("Введите id контакта, который нужно изменить: ")
        name = input("Введите имя для изменения: ")
        surname = input("Введите фамилию для изменения: ")
        number = input("Введите номер для изменения: ")
        change_contact(id, name, surname, number)
    elif choice == '6':
        save_phone_book()
        print("Контакты сохранены в файл.")
    elif choice == '7':
        break
    else:
        print("Не правильный выбор! Выберите вариант из пречня.")
