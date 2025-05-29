import sqlite3

def create_database():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()

    # Supprimer les tables si elles existent
    c.execute('DROP TABLE IF EXISTS ChambreReservee')
    c.execute('DROP TABLE IF EXISTS Evaluation')
    c.execute('DROP TABLE IF EXISTS Reservation')
    c.execute('DROP TABLE IF EXISTS Chambre')
    c.execute('DROP TABLE IF EXISTS TypeChambre')
    c.execute('DROP TABLE IF EXISTS Prestation')
    c.execute('DROP TABLE IF EXISTS Client')
    c.execute('DROP TABLE IF EXISTS Hotel')

    # Création des tables
    c.execute('''
    CREATE TABLE Hotel (
        id INTEGER PRIMARY KEY,
        ville TEXT,
        pays TEXT,
        codePostal TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE Client (
        id INTEGER PRIMARY KEY,
        adresse TEXT,
        ville TEXT,
        codePostal TEXT,
        email TEXT,
        telephone TEXT,
        nomComplet TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE Prestation (
        id INTEGER PRIMARY KEY,
        prix REAL,
        libelle TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE TypeChambre (
        id INTEGER PRIMARY KEY,
        libelle TEXT,
        prixParNuit REAL
    )
    ''')

    c.execute('''
    CREATE TABLE Chambre (
        id INTEGER PRIMARY KEY,
        numero INTEGER,
        etage INTEGER,
        fumeur BOOLEAN,
        id_type_chambre INTEGER,
        id_hotel INTEGER,
        FOREIGN KEY (id_type_chambre) REFERENCES TypeChambre(id),
        FOREIGN KEY (id_hotel) REFERENCES Hotel(id)
    )
    ''')

    c.execute('''
    CREATE TABLE Reservation (
        id INTEGER PRIMARY KEY,
        dateDebut TEXT,
        dateFin TEXT,
        id_client INTEGER,
        FOREIGN KEY (id_client) REFERENCES Client(id)
    )
    ''')

    c.execute('''
    CREATE TABLE Evaluation (
        id INTEGER PRIMARY KEY,
        date TEXT,
        note INTEGER,
        commentaire TEXT,
        id_client INTEGER,
        FOREIGN KEY (id_client) REFERENCES Client(id)
    )
    ''')

    c.execute('''
    CREATE TABLE ChambreReservee (
        id_reservation INTEGER,
        id_chambre INTEGER,
        PRIMARY KEY (id_reservation, id_chambre),
        FOREIGN KEY (id_reservation) REFERENCES Reservation(id),
        FOREIGN KEY (id_chambre) REFERENCES Chambre(id)
    )
    ''')

    # Insertion des données

    hotels = [
        (1, 'Paris', 'France', '75001'),
        (2, 'Lyon', 'France', '69002')
    ]
    c.executemany('INSERT INTO Hotel VALUES (?, ?, ?, ?)', hotels)

    clients = [
        (1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
        (2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
        (3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
        (4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
        (5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')
    ]
    c.executemany('INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)', clients)

    prestations = [
        (1, 15, 'Petit-déjeuner'),
        (2, 30, 'Navette aéroport'),
        (3, 0, 'Wi-Fi gratuit'),
        (4, 50, 'Spa et bien-être'),
        (5, 20, 'Parking sécurisé')
    ]
    c.executemany('INSERT INTO Prestation VALUES (?, ?, ?)', prestations)

    types_chambre = [
        (1, 'Simple', 80),
        (2, 'Double', 120)
    ]
    c.executemany('INSERT INTO TypeChambre VALUES (?, ?, ?)', types_chambre)

    chambres = [
        (1, 201, 2, 0, 1, 1),
        (2, 502, 5, 1, 1, 2),
        (3, 305, 3, 0, 2, 1),
        (4, 410, 4, 0, 2, 2),
        (5, 104, 1, 1, 2, 2),
        (6, 202, 2, 0, 1, 1),
        (7, 307, 3, 1, 1, 2),
        (8, 101, 1, 0, 1, 1)
    ]
    c.executemany('INSERT INTO Chambre VALUES (?, ?, ?, ?, ?, ?)', chambres)

    reservations = [
        (1, '2025-06-15', '2025-06-18', 1),
        (2, '2025-07-01', '2025-07-05', 2),
        (3, '2025-08-10', '2025-08-14', 3),
        (4, '2025-09-05', '2025-09-07', 4),
        (5, '2025-09-20', '2025-09-25', 5),
        (7, '2025-11-12', '2025-11-14', 2),
        (9, '2026-01-15', '2026-01-18', 4),
        (10, '2026-02-01', '2026-02-05', 2)
    ]
    c.executemany('INSERT INTO Reservation VALUES (?, ?, ?, ?)', reservations)

    evaluations = [
        (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
        (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
        (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
        (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
        (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
    ]
    c.executemany('INSERT INTO Evaluation VALUES (?, ?, ?, ?, ?)', evaluations)

    chambres_reservees = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (7, 7),
        (9, 6),
        (10, 8)
    ]
    c.executemany('INSERT INTO ChambreReservee VALUES (?, ?)', chambres_reservees)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
