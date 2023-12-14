import sqlite3
def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)
    return None

# Function to execute SQL queries and fetch results
def execute_query(connection, query, data=None):
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor
    except sqlite3.Error as e:
        print(e)
    return None

# Function to create tables if they don't exist
def create_tables(connection):
    queries = [
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            is_employee TEXT
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS burgers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            ingredients TEXT
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            burger_id INTEGER,
            is_produced TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(burger_id) REFERENCES burgers(id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER
        )
        '''
    ]

    for query in queries:
        execute_query(connection, query)

# Function for user login
def user_login(connection, username, password):
    query = "SELECT * FROM users WHERE name = ? AND password = ?"
    cursor = execute_query(connection, query, (username, password))
    return cursor.fetchone()

# Function for employee login
def employee_login(connection, username, password):
    query = "SELECT * FROM users WHERE name = ? AND password = ? AND is_employee = 'Yes'"
    cursor = execute_query(connection, query, (username, password))
    return cursor.fetchone()

# Function to register a new user
def register_user(connection, username, password, is_employee):
    query = "INSERT INTO users (name, password, is_employee) VALUES (?, ?, ?)"
    execute_query(connection, query, (username, password, is_employee))

# Function to register a new order
def register_order(connection, user_id, burger_id, is_produced):
    query = "INSERT INTO orders (user_id, burger_id, is_produced) VALUES (?, ?, ?)"
    execute_query(connection, query, (user_id, burger_id, is_produced))

# Function to view user's orders
def view_user_orders(connection, user_id):
    query = "SELECT * FROM orders WHERE user_id = ?"
    cursor = execute_query(connection, query, (user_id,))
    return cursor.fetchall()

# Function to view all orders (for employees)
def view_all_orders(connection):
    query = "SELECT * FROM orders"
    cursor = execute_query(connection, query)
    return cursor.fetchall()

# Function to view ingredient inventory (for employees)
def view_inventory(connection):
    query = "SELECT * FROM ingredients"
    cursor = execute_query(connection, query)
    return cursor.fetchall()

# Function to mark an order as completed and update ingredient inventory
def mark_order_completed(connection, order_id):
    # Assuming you have a function to update inventory, update it here
    # For example, if you have an update_inventory function, you can call it like this:
    # update_inventory(connection, ingredient_id, new_quantity)
    query = "UPDATE orders SET is_produced = 'Yes' WHERE id = ?"
    execute_query(connection, query, (order_id,))

# Function for user login or create a new user
def user_login_or_create(connection, username, password):
    user = user_login(connection, username, password)

    if user:
        return user
    else:
        is_employee = input("Are you an employee? (Yes/No): ")
        register_user(connection, username, password, is_employee)
        print("User created successfully!")
        return user_login(connection, username, password)

# Function for employee login or create a new employee
def employee_login_or_create(connection, username, password):
    employee = employee_login(connection, username, password)

    if employee:
        return employee
    else:
        register_user(connection, username, password, 'Yes')
        print("Employee created successfully!")
        return employee_login(connection, username, password)



# Main function
def main():
    db_file = "burger_queen.db"
    connection = create_connection(db_file)
    create_tables(connection)

    while True:
        print("\nBurger Queen System\n")
        print("1. Log In or Create User")
        print("2. Exit")

        choice = input("Select an option (1/2): ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            user = user_login_or_create(connection, username, password)
            employee = employee_login_or_create(connection, username, password)

            

        elif choice == "2":
            print("Exiting Burger Queen System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    connection.close()

if __name__ == "__main__":
    main()
