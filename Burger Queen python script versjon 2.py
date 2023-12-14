import sqlite3
con = sqlite3.connect("BurgerQueen.db")
cursor = con.cursor()
cursor.execute("SELECT * FROM Burgere")
con.close()

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

# Function to register a new user
def register_user(connection, username, password, is_employee):
    query = "INSERT INTO users (name, password, is_employee) VALUES (?, ?, ?)"
    execute_query(connection, query, (username, password, is_employee))

# Function for employee login or create a new employee
def employee_login_or_create(connection, username, password):
    employee = employee_login(connection, username, password)

    if employee:
        return employee
    else:
        is_employee = input("Are you an employee? (Yes/No): ")
        if is_employee.lower() == 'yes':
            register_user(connection, username, password, 'Yes')
            print("Employee account created successfully!")
        else:
            print("Non-employee accounts cannot access employee features.")
        return employee_login(connection, username, password)

# Function to view orders for users and employees:
def view_orders(connection, user_id, is_employee):
    if is_employee.lower() == 'yes' or is_employee.lower() == 'no':
        query = "SELECT orders.id, burgers.name, orders.is_produced FROM orders JOIN burgers ON orders.burger_id = burgers.id"
        cursor = execute_query(connection, query)
    else:
        query = "SELECT orders.id, burgers.name, orders.is_produced FROM orders JOIN burgers ON orders.burger_id = burgers.id WHERE orders.user_id = ?"
        cursor = execute_query(connection, query, (user_id,))

    orders = cursor.fetchall()

    if orders:
        print("\nOrders:")
        for order in orders:
            print(f"Order ID: {order[0]}, Burger: {order[1]}, Produced: {order[2]}")
    else:
        print("No orders available.")

# Function to place an order
def place_order(connection, user_id):
    print("Place Order:")
    # Display available burgers
    burgers = view_all_burgers(connection)
    if not burgers:
        print("No burgers available to order.")
        return

    print("Available Burgers:")
    for burger in burgers:
        print(f"{burger[0]}. {burger[1]}")

    # Get user input for the chosen burger
    burger_id = input("Enter the ID of the burger you want to order: ")

    # Check if the entered ID is valid
    valid_burger_ids = [str(burger[0]) for burger in burgers]
    if burger_id not in valid_burger_ids:
        print("Invalid burger ID. Please try again.")
        return

    # Register the order in the 'orders' table
    register_order(connection, user_id, int(burger_id), 'No')
    print("Order placed successfully!")

# Function to view all available burgers
def view_all_burgers(connection):
    query = "SELECT * FROM burgers"
    cursor = execute_query(connection, query)
    return cursor.fetchall()

# Update the main function to include options for ordering and viewing orders
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

            if user:
                while True:
                    print("\nUser Menu:")
                    print("1. Place an Order")
                    print("2. View Orders")
                    print("3. Logout")

                    user_choice = input("Select an option (1/2/3): ")

                    if user_choice == "1":
                        place_order(connection, user[0])  # user[0] is the user_id
                    elif user_choice == "2":
                        view_orders(connection, user[0], user[3])  # user[3] is the is_employee field
                    elif user_choice == "3":
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif employee:
                while True:
                    print("\nEmployee Menu:")
                    print("1. View All Orders")
                    print("2. View Ingredient Inventory")
                    print("3. Mark Order as Completed")
                    print("4. Logout")

                    employee_choice = input("Select an option (1/2/3/4): ")

                    if employee_choice == "1":
                        view_all_orders(connection)  # Corrected function name
                    # ... (unchanged code)

        elif choice == "2":
            print("Exiting Burger Queen System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()