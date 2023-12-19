import sqlite3
import hashlib

# Function to create the initial database structure and insert dummy data
def create_database():
    connection = sqlite3.connect("BurgerQueenSql.db")
    cursor = connection.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Brukere (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Navn TEXT NOT NULL,
            Passord TEXT NOT NULL,
            Ansatt TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Burgere (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Navn TEXT NOT NULL,
            Ingredienser TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ordre (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Hvem TEXT NOT NULL,
            Hva TEXT NOT NULL,
            Produsert TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingredienser (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Ingrediens TEXT NOT NULL,
            "Hvor mye" INTEGER NOT NULL
        );
    ''')

    # Insert dummy data
    with open("dummydatasqlscript.sql", "r") as dummy_data_file:
        dummy_data_script = dummy_data_file.read()
        cursor.executescript(dummy_data_script)

    # Commit and close
    connection.commit()
    connection.close()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if the user is an employee
def is_employee(username):
    connection = sqlite3.connect("BurgerQueenSql.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT Ansatt FROM Brukere
        WHERE Navn = ?
    ''', (username,))

    result = cursor.fetchone()

    connection.close()

    return result[0] == 'Ja' if result else False

# Function to create a new user account
def create_account(username, password, is_employee):
    connection = sqlite3.connect("BurgerQueenSql.db")
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute('''
        INSERT INTO Brukere (Navn, Passord, Ansatt)
        VALUES (?, ?, ?)
    ''', (username, hashed_password, 'Ja' if is_employee else 'Nei'))

    connection.commit()
    connection.close()

# Function to authenticate a user
def authenticate_user(username, password):
    connection = sqlite3.connect("BurgerQueenSql.db")
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute('''
        SELECT Navn FROM Brukere
        WHERE Navn = ? AND Passord = ?
    ''', (username, hashed_password))

    result = cursor.fetchone()

    connection.close()

    return result is not None

# Function to make an order
def make_order(username):
    connection = sqlite3.connect("BurgerQueenSql.db")
    cursor = connection.cursor()

    # Display available burgers
    print("\n--- Available Burgers ---")
    cursor.execute("SELECT Navn FROM Burgere")
    burgers = cursor.fetchall()
    for i, burger in enumerate(burgers, start=1):
        print(f"{i}. {burger[0]}")

    # Select a burger to order
    try:
        burger_index = int(input("Select a burger to order (enter the corresponding number): ")) - 1
        selected_burger = burgers[burger_index][0]

        # Insert the order into the database
        cursor.execute('''
            INSERT INTO Ordre (Hvem, Hva, Produsert)
            VALUES (?, ?, 'Nei')
        ''', (username, selected_burger))

        print(f"Order for '{selected_burger}' placed successfully!")

    except (ValueError, IndexError):
        print("Invalid input. Order canceled.")

    connection.commit()
    connection.close()

# Main function to run the Burger Queen application
def main():
    create_database()

    while True:
        print("\n--- Burger Queen Application ---")
        print("1. Log In")
        print("2. Create Account")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            handle_login()
        elif choice == "2":
            # Add account creation code here
            pass
        elif choice == "3":
            print("Exiting Burger Queen Application. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

def handle_login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if authenticate_user(username, password):
        if is_employee(username):
            handle_employee_menu()
        else:
            handle_customer_menu(username)
    else:
        print("Authentication failed. Please try again.")

def handle_employee_menu():
    while True:
        print("\n--- Employee Menu ---")
        print("1. View Orders")
        print("2. Make an Order")
        print("3. Log Out")

        employee_choice = input("Select an option: ")

        if employee_choice == "1":
            # Implement View Orders for employees
            pass
        elif employee_choice == "2":
            # Implement Make an Order for employees
            pass
        elif employee_choice == "3":
            break
        else:
            print("Invalid option. Try again.")

def handle_customer_menu(username):
    while True:
        print("\n--- Customer Menu ---")
        print("1. Make an Order")
        print("2. Log Out")

        customer_choice = input("Select an option: ")

        if customer_choice == "1":
            make_order(username)
        elif customer_choice == "2":
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()



