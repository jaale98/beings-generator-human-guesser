import re
import random
import sqlite3

class Being:
    """
    A class to represent a Being with specific attributes.
    Attributes:
        beingid (str): A unique identifier for the being.
        ishuman (bool): Whether the being is human or not.
        sex (str): The sex of the being.
        age (int): The age of the being.
        weight (int): The weight of the being in kg.
    """
    def __init__(self, beingid, ishuman, sex, age, weight):
        if not isinstance(beingid, str) or not re.match(r"^[A-Za-z]\d{5}$", beingid):
            raise ValueError("beingid must be a string")
        if not isinstance(ishuman, bool):
            raise ValueError("ishuman must be a boolean (True or False)")
        if sex not in ['M','F','N/A']:
            raise ValueError("sex must be one of 'M','F', or 'N/A'")
        if not isinstance(age, int) or not (0 <= age <= 10000):
            raise ValueError("age must be a non-negative integer up to 10000")
        if not isinstance(weight, int) or not (0 <= weight <= 10000):
            raise ValueError("weight must be a non-negative integer up to 10000")

        self.beingid = beingid
        self.ishuman = ishuman
        self.sex = sex
        self.age = age
        self.weight = weight
    
    def __str__(self):
        return (f"Being(beingid='{self.beingid}', ishuman={self.ishuman}, "
            f"sex='{self.sex}', age={self.age}, weight={self.weight})")

def generate_random_being():
   
    # Generate a random beingid (1 letter + 5 digits)
    letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    digits = f"{random.randint(0, 99999):05}" # ensure 5 digits, allowing leading zeroes
    beingid = letter + digits

    # decide if the being is human
    ishuman = random.choice([True, False])

    # assign a sex
    if ishuman:
        sex = 'N/A' if random.random() < 0.05 else random.choice(['M','F'])
    else:
        sex = 'N/A' if random.random() <0.95 else random.choice(['M','F'])

    # assign an age (0 to 10000)
    if ishuman:
        age = random.randint(0,100)
    else:
        age = random.randint(101,10000)

    # assign a weight (0 to 10000 kg)
    if ishuman:
        max_weight = min(100, int(10 * (age**.5))) 
        max_weight = max(max_weight, 3)
        weight = random.randint(3, max_weight)
    else:
        weight = random.randint(0, 10000)

    # Create and return the random Being object
    return Being(beingid, ishuman, sex, age, weight)

def initialize_database():
    #init database and create beings table
    conn = sqlite3.connect("beings.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS beings (
            beingid TEXT PRIMARY KEY,
            ishuman BOOLEAN,
            sex TEXT,
            age INTEGER,
            weight INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_being_to_database(being):
    #save a being to the database
    conn = sqlite3.connect("beings.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO beings (beingid, ishuman, sex, age, weight)
            VALUES (?, ?, ?, ?, ?)
        """, (being.beingid, being.ishuman, being.sex, being.age, being.weight))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Duplicate beingid '{being.beingid}' detected. Generating a new being...")
    finally:
        conn.close()

def main():
    initialize_database()

    while True:
        user_input = input("Generate a new being? (y/n): ").strip().lower()
        if user_input == 'y':
            being = generate_random_being()
            print(being)
            save_being_to_database(being)
            print("Being saved to database.")
        elif user_input == 'n':
            print("Exiting program.")
            break
        else:
            print("Invalid input. Please enter 'y' to generate or 'n' to quit.")

if __name__ == "__main__":
    main()   