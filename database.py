import sqlite3

def create_database():
    print("Connecting to database...")
    conn = sqlite3.connect("database/car_rental.db")
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    """)
    print("Created 'users' table")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            space TEXT,
            speed TEXT,
            color TEXT,
            image TEXT,
            available INTEGER DEFAULT 1,
            price REAL
        )
    """)
    print("Created 'cars' table")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            car_id INTEGER,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (car_id) REFERENCES cars(id)
        )
    """)
    print("Created 'reservations' table")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            car_id INTEGER,
            rating INTEGER,
            comment TEXT,
            admin_response TEXT
        )
    """)
    print("Created 'reviews' table")

    # Delete existing users
    cursor.execute("DELETE FROM users")
    print("Deleted existing users")

    # Insert fake cars
    cars = [
        ("Toyota", "Camry", "5 seats", "120 mph", "Silver", "car1.jpg", 1, 30.00),
        ("Honda", "Civic", "5 seats", "110 mph", "Blue", "car2.jpg", 1, 25.00),
        ("Ford", "Mustang", "4 seats", "150 mph", "Red", "car3.jpg", 0, 50.00), # rented
        ("BMW", "X5", "7 seats", "140 mph", "Black", "car4.jpg", 1, 60.00),
    ]
    cursor.executemany("INSERT INTO cars (brand, model, space, speed, color, image, available, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", cars)
    print(f"Inserted {len(cars)} fake cars")

    # Insert fake users with unique usernames
    users = [("user1", "password", 0), ("user2", "password", 0), ("admin", "password", 1)]
    cursor.executemany("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", users)
    print(f"Inserted {len(users)} fake users")

    # Insert fake reservations
    reservations = [(1, 3, "2024-01-01", "2024-01-05"), (2, 3, "2024-02-01", "2024-02-05")]
    cursor.executemany("INSERT INTO reservations (user_id, car_id, start_date, end_date) VALUES (?, ?, ?, ?)", reservations)
    print(f"Inserted {len(reservations)} fake reservations")

    conn.commit()
    print("Database committed")
    conn.close()
    print("Connection closed")

if __name__ == "__main__":
    create_database()
