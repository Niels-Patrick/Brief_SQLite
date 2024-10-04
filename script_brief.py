import sqlite3
import csv

# Connecting to the database
con = sqlite3.connect("brief.db")
# Creating the cursor
cur = con.cursor()

# Creating the table Clients in the database
cur.execute(
    """CREATE TABLE Clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nom VARCHAR(100) NOT NULL,
        prenom VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL,
        date_inscription TEXT NOT NULL);"""
)

# Creating the table Commandes in the database
cur.execute(
    """CREATE TABLE Commandes(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        client_id INTEGER NOT NULL,
        produit VARCHAR(255) NOT NULL,
        date_commande TEXT NOT NULL,
        CONSTRAINT fk_client_id FOREIGN KEY(client_id) REFERENCES Clients(client_id));"""
)

# Inserting new entries in the Clients table
cur.execute(
    """INSERT INTO Clients (nom, prenom, email, date_inscription)
        VALUES ('Jack', 'Daniels', 'jackd@gmail.com', '2024-05-23 12:34:54.123'),
               ('Adam', 'Jensen', 'adamj@gmail.com', '2024-07-05 09:54:12.123'),
               ('Alice', 'Lidell', 'aliceiw@gmail.com', '2024-02-12 14:45:02.123');"""
)
con.commit()

# Inserting new entries in the Commandes table
cur.execute(
    """INSERT INTO Commandes(client_id, produit, date_commande)
        VALUES (1, 'Whisky', '2024-05-23 12:34:54.123'),
               (2, 'Puce neurale', '2024-07-05 09:54:12.123'),
               (3, 'Gigancake', '2024-02-12 14:45:02.123');"""
)
con.commit()

# Selecting all clients
res = cur.execute("SELECT * FROM Clients;")
print(res.fetchall())

# Selecting all orders for a client
res = cur.execute("SELECT * FROM Commandes WHERE client_id = 2")
print(res.fetchall())

# Updating the email of a client
res = cur.execute(
    """UPDATE Clients
        SET email = 'aLidell@gmail.com'
        WHERE nom = 'Alice'"""
)
con.commit()

# Delete an order
res = cur.execute(
    """DELETE FROM Commandes
        WHERE id = 1"""
)
con.commit()

# Export database to a CSV file
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

with open('brief.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    for table_name in tables:
        table_name = table_name[0]

        writer.writerow([f"Table: {table_name}"])

        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()

        column_names = [description[0] for description in cur.description]

        writer.writerow(column_names)

        writer.writerows(rows)

        writer.writerow([])

con.close()
