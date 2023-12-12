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

# Main function
def main():
    db_file = "burger_queen.db"
    connection = create_connection(db_file)
    create_tables(connection)

    while True:
        print("\nBurger Queen System\n")
        print("1. Log In")
        print("2. Exit")

        choice = input("Select an option (1/2): ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            user = user_login(connection, username, password)
            employee = employee_login(connection, username, password)

            if user:
                user_id = user[0]
                while True:
                    print("\nUser Menu\n")
                    print("1. Order Burger")
                    print("2. View Orders")
                    print("3. Log Out")

                    user_choice = input("Select an option (1/2/3): ")

                    if user_choice == "1":
                        burger_id = int(input("Enter the ID of the burger you want to order: "))
                        is_produced = "No"
                        register_order(connection, user_id, burger_id, is_produced)
                        print("Order placed successfully!")

                    elif user_choice == "2":
                        orders = view_user_orders(connection, user_id)
                        print("\nYour Orders:\n")
                        for order in orders:
                            print(order)

                    elif user_choice == "3":
                        break

                    else:
                        print("Invalid choice. Please try again.")

            elif employee:
                while True:
                    print("\nEmployee Menu\n")
                    print("1. View All Orders")
                    print("2. View Inventory")
                    print("3. Mark Order as Completed")
                    print("4. Log Out")

                    employee_choice = input("Select an option (1/2/3/4): ")

                    if employee_choice == "1":
                        orders = view_all_orders(connection)
                        print("\nAll Orders:\n")
                        for order in orders:
                            print(order)

                    elif employee_choice == "2":
                        inventory = view_inventory(connection)
                        print("\nIngredient Inventory:\n")
                        for item in inventory:
                            print(item)

                    elif employee_choice == "3":
                        order_id = int(input("Enter the ID of the order to mark as completed: "))
                        mark_order_completed(connection, order_id)
                        print("Order marked as completed!")

                    elif employee_choice == "4":
                        break

                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("Invalid username or password. Please try again.")

        elif choice == "2":
            print("Exiting Burger Queen System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    connection.close()

if __name__ == "__main__":
    main()
