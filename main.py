import sqlite3

# Initialize Database
def init_db():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            event_name TEXT NOT NULL,
            price REAL,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

def get_price(category):
    prices = {"Student": 2000, "Regular": 5000, "VIP": 10000}
    return prices.get(category, 500)

def apply_for_event():
    name = input("Enter your name: ")
    print("Categories: Student, Regular, VIP")
    category = input("Enter category: ").capitalize()
    event = input("Enter Event Name: ")
    
    price = get_price(category)
    # Simulating a payment link generation
    pay_link = f"https://gateway.com{price}&ref={name[:3]}"

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO applications (name, category, event_name, price) VALUES (?, ?, ?, ?)",
                   (name, category, event, price))
    conn.commit()
    conn.close()

    print(f"\n✅ Application Submitted!")
    print(f"💰 Total Due: ksh{price}")
    print(f"🔗 Payment Link: {pay_link}")

def view_applications():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications")
    rows = cursor.fetchall()
    
    print("\n--- Current Applications ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Tier: {row[2]} | Event: {row[3]} | Status: {row[5]}")
    conn.close()

# Simple CLI Menu
def main():
    init_db()
    while True:
        print("\n--- Event Registration System ---")
        print("1. Apply for Event")
        print("2. View Applications")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            apply_for_event()
        elif choice == '2':
            view_applications()
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
