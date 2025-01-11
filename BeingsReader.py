import sqlite3

def add_guessed_column():
    # adds the "guessed_ishuman" column to beings.db
    conn = sqlite3.connect("beings.db")
    cursor = conn.cursor()

    cursor.execute("""
        ALTER TABLE beings ADD COLUMN guessed_ishuman BOOLEAN
    """)

    conn.commit()
    conn.close()
    print("Added 'guessed_ishuman' column to the db")

def update_guessed_ishuman():
    # iterates through each row and guesses if human, adds true or false to new col
    conn = sqlite3.connect("beings.db")
    cursor = conn.cursor()

    cursor.execute("SELECT beingid, sex, age, weight FROM beings")
    beings_data = cursor.fetchall()

    for being in beings_data:
        beingid, sex, age, weight = being

        guessed_ishuman = (age <= 130 and weight <= 130) or sex in ['M','F']

        cursor.execute("""
            UPDATE beings
            SET guessed_ishuman = ?
            WHERE beingid = ?
        """, (guessed_ishuman, beingid))

    conn.commit()
    conn.close()
    print("Updated 'guessed_ishuman' column with guessed values")

def compare_guesses():
    conn = sqlite3.connect('beings.db')
    cursor = conn.cursor()

    cursor.execute("SELECT guessed_ishuman, ishuman FROM beings")
    rows = cursor.fetchall()

    correct_guesses = 0
    total_rows = len(rows)

    for row in rows:
        guessed_ishuman, ishuman = row
        if guessed_ishuman == ishuman:
            correct_guesses += 1
    
    if total_rows > 0:
        correct_percentage = (correct_guesses / total_rows) * 100
        print(f"Correct gueses: {correct_percentage:.2f}%")
    else:
        print("No rows to compare.")
    
    conn.close()

try:
    add_guessed_column()
except sqlite3.OperationalError:
    print("'guessed_ishuman' column already exists")
update_guessed_ishuman()
compare_guesses()
 