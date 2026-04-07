import sqlite3

# Initialize Database
def init_db():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
             event_name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,                                       
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            event_id INTEGER,
            price REAL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (event_id) REFERENCES events(id)       
        )
    """)
    conn.commit()
    conn.close()

def get_price(category):
    prices = { 
        "Student": 2000, #Ksh 2,000
        "Regular": 5000, #Ksh 5,000
        "VIP": 10000.    #Ksh 10,000
        }
    return prices.get(category, 5000)

categories = ["Student", "Regular", "VIP"]

def add_event():
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    event_name = input("Enter event name: ")

    try:
        cursor.execute(
            "INSERT INTO events (event_name) VALUES (?)", 
            (event_name,)
        )
        conn.commit()
        print(f"✅ Event '{event_name}' added successfully!")
    except sqlite3.IntegrityError:
        print("❌ Event already exists!")
    finally:
        conn.close()

def apply_for_event():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall

    if len(events) == 0:
        print("No events available.Add an event first")
        conn.close()
        return
    
    print("\nAvailable Events:")
    for event in events:
        print(f"{event[0]}. {event[1]}")

    name = input("Enter your name: ")

    print("Categories: Student, Regular, VIP")
    category = input("Enter category: ").capitalize()

    event_id = int(input("Enter event ID"))
    price = get_price(category)
    
    cursor.execute("""
    INSERT INTO applications (name, category, event_id, price)
    VALUES (?, ?, ?, ?)
    """, (name, category, event_id, price))

    conn.commit()

    print("✅ Application submitted successfully.")
    print(f"Total Due: Ksh {price}")

    conn.close()


# ---------------- CRUD 2: READ ALL ----------------
def view_applications():
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT applications.id, applications.name, applications.category,
           events.event_name, applications.price, applications.status
    FROM applications
    JOIN events ON applications.event_id = events.id
    """)

    print(f"Total Due: Ksh {get_price:,}")

    applications = cursor.fetchall()

    if not applications:
        print("No applications found.")
    else:
        for app in applications:
            print(app)

    conn.close()


# ---------------- CRUD 3: READ ONE ----------------
def view_application_by_id():
    app_id = input("Enter application ID: ")

    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT applications.id, applications.name, applications.category,
           events.event_name, applications.price, applications.status
    FROM applications
    JOIN events ON applications.event_id = events.id
    WHERE applications.id = ?
    """, (app_id,))

    app = cursor.fetchone()

    if app:
        print(app)
    else:
        print("Application not found.")

    conn.close()


# ---------------- CRUD 4: UPDATE NAME ----------------
def update_name():
    app_id = input("Enter application ID: ")
    new_name = input("Enter new name: ")

    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE applications SET name = ? WHERE id = ?",
        (new_name, app_id)
    )

    conn.commit()
    print("✅ Name updated.")

    conn.close()


# ---------------- CRUD 5: UPDATE CATEGORY ----------------
def update_category():
    app_id = input("Enter application ID: ")

    print("Categories:", categories)
    new_category = input("Enter new category: ").capitalize()

    new_price = get_price(new_category)

    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET category = ?, price = ?
    WHERE id = ?
    """, (new_category, new_price, app_id))

    conn.commit()
    print("✅ Category and price updated.")

    conn.close()


# ---------------- CRUD 6: UPDATE STATUS ----------------
def update_status():
    app_id = input("Enter application ID: ")
    new_status = input("Enter new status (Pending/Paid/Approved): ")

    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET status = ?
    WHERE id = ?
    """, (new_status, app_id))

    conn.commit()
    print("✅ Status updated.")

    conn.close()


# ---------------- CRUD 7: DELETE ----------------
def delete_application():
    app_id = input("Enter application ID to delete: ")

    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (app_id,)
    )

    conn.commit()
    print("✅ Application deleted.")

    conn.close()


# ---------------- CRUD 8: SEARCH ----------------
def search_by_event():
    search = input("Enter event name to search: ")

    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT applications.name, events.event_name, applications.status
    FROM applications
    JOIN events ON applications.event_id = events.id
    WHERE events.event_name LIKE ?
    """, ('%' + search + '%',))

    results = cursor.fetchall()

    if results:
        for result in results:
            print(result)
    else:
        print("No matching applications found.")

    conn.close()


# ---------------- MENU ----------------
def main():
    init_db()

    while True:
        print("\n===== EVENT APPLICATION SYSTEM =====")
        print("1. Add Event")
        print("2. Apply for Event")
        print("3. View All Applications")
        print("4. View Application by ID")
        print("5. Update Applicant Name")
        print("6. Update Category")
        print("7. Update Status")
        print("8. Delete Application")
        print("9. Search by Event Name")
        print("10. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_event()

        elif choice == "2":
            apply_for_event()

        elif choice == "3":
            view_applications()

        elif choice == "4":
            view_application_by_id()

        elif choice == "5":
            update_name()

        elif choice == "6":
            update_category()

        elif choice == "7":
            update_status()

        elif choice == "8":
            delete_application()

        elif choice == "9":
            search_by_event()

        elif choice == "10":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
