import sqlite3
import os

def create_database():
    # Supprime la base si elle existe pour repartir à zéro
    if os.path.exists("hotel.db"):
        os.remove("hotel.db")

    conn = sqlite3.connect("hotel.db")
    c = conn.cursor()

    # Création des tables
    c.execute('''
    CREATE TABLE Hotel (
        id INTEGER PRIMARY KEY,
        ville TEXT,
        pays TEXT,
        code_postal INTEGER
    )''')

    c.execute('''
    CREATE TABLE Client (
        id INTEGER PRIMARY KEY,
        adresse TEXT,
        ville TEXT,
        code_postal INTEGER,
        email TEXT,
        telephone TEXT,
        nom TEXT
    )''')

    c.execute('''
    CREATE TABLE Prestation (
        id INTEGER PRIMARY KEY,
        prix REAL,
        description TEXT
    )''')

    c.execute('''
    CREATE TABLE TypeChambre (
        id INTEGER PRIMARY KEY,
        type TEXT,
        prix_par_nuit REAL
    )''')

    c.execute('''
    CREATE TABLE Chambre (
        id INTEGER PRIMARY KEY,
        numero INTEGER,
        etage INTEGER,
        fumeur INTEGER,
        hotel_id INTEGER,
        type_chambre_id INTEGER,
        FOREIGN KEY (hotel_id) REFERENCES Hotel(id),
        FOREIGN KEY (type_chambre_id) REFERENCES TypeChambre(id)
    )''')

    c.execute('''
    CREATE TABLE Reservation (
        id INTEGER PRIMARY KEY,
        date_debut TEXT,
        date_fin TEXT,
        client_id INTEGER,
        chambre_id INTEGER,
        FOREIGN KEY (client_id) REFERENCES Client(id),
        FOREIGN KEY (chambre_id) REFERENCES Chambre(id)
    )''')

    c.execute('''
    CREATE TABLE Evaluation (
        id INTEGER PRIMARY KEY,
        date TEXT,
        note INTEGER,
        commentaire TEXT,
        client_id INTEGER,
        FOREIGN KEY (client_id) REFERENCES Client(id)
    )''')

    # Insertion des données

    c.executemany("INSERT INTO Hotel VALUES (?, ?, ?, ?)", [
        (1, 'Paris', 'France', 75001),
        (2, 'Lyon', 'France', 69002)
    ])

    c.executemany("INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)", [
        (1, '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
        (2, '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
        (3, '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
        (4, '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
        (5, '3 Rue des Fleurs', 'Nice', 6000, 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')
    ])

    c.executemany("INSERT INTO Prestation VALUES (?, ?, ?)", [
        (1, 15, 'Petit-déjeuner'),
        (2, 30, 'Navette aéroport'),
        (3, 0, 'Wi-Fi gratuit'),
        (4, 50, 'Spa et bien-être'),
        (5, 20, 'Parking sécurisé')
    ])

    c.executemany("INSERT INTO TypeChambre VALUES (?, ?, ?)", [
        (1, 'Simple', 80),
        (2, 'Double', 120)
    ])

    c.executemany("INSERT INTO Chambre VALUES (?, ?, ?, ?, ?, ?)", [
        (1, 201, 2, 0, 1, 1),
        (2, 502, 5, 1, 1, 2),
        (3, 305, 3, 0, 2, 1),
        (4, 410, 4, 0, 2, 2),
        (5, 104, 1, 1, 2, 2),
        (6, 202, 2, 0, 1, 1),
        (7, 307, 3, 1, 1, 2),
        (8, 101, 1, 0, 1, 1)
    ])

    c.executemany("INSERT INTO Reservation VALUES (?, ?, ?, ?, ?)", [
        (1, '2025-06-15', '2025-06-18', 1, 1),
        (2, '2025-07-01', '2025-07-05', 2, 2),
        (3, '2025-11-12', '2025-11-14', 2, 7),
        (4, '2026-02-01', '2026-02-05', 2, 10),  # Attention, chambre 10 n'existe pas, je corrige ci-dessous
        (5, '2025-08-10', '2025-08-14', 3, 3),
        (6, '2025-09-05', '2025-09-07', 4, 4),
        (7, '2026-01-15', '2026-01-18', 4, 9),  # chambre 9 n'existe pas non plus
        (8, '2025-09-20', '2025-09-25', 5, 5)
    ])

    # Corrige pour chambres valides : Remplace chambres 9 et 10 par chambres valides, ex 6 et 8
    c.execute("UPDATE Reservation SET chambre_id = 6 WHERE chambre_id = 10")
    c.execute("UPDATE Reservation SET chambre_id = 8 WHERE chambre_id = 9")

    c.executemany("INSERT INTO Evaluation VALUES (?, ?, ?, ?, ?)", [
        (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
        (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
        (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
        (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
        (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
    ])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Base de données créée avec succès.")
