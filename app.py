import streamlit as st
import sqlite3
from datetime import datetime

conn = sqlite3.connect('hotel.db', check_same_thread=False)
c = conn.cursor()

st.title("Gestion Hôtelière")

menu = ["Réservations", "Clients", "Chambres Disponibles", "Ajouter Client", "Ajouter Réservation"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Réservations":
    st.header("Liste des Réservations")
    c.execute('''
    SELECT Reservation.id, Client.nom, Chambre.numero, Reservation.date_debut, Reservation.date_fin 
    FROM Reservation
    JOIN Client ON Reservation.client_id = Client.id
    JOIN Chambre ON Reservation.chambre_id = Chambre.id
    ORDER BY Reservation.date_debut
    ''')
    rows = c.fetchall()
    for r in rows:
        st.write(f"Réservation {r[0]} : Client {r[1]}, Chambre {r[2]}, du {r[3]} au {r[4]}")

elif choice == "Clients":
    st.header("Liste des Clients")
    c.execute("SELECT id, nom, email, ville FROM Client")
    rows = c.fetchall()
    for r in rows:
        st.write(f"ID {r[0]} - {r[1]} - {r[2]} - {r[3]}")

elif choice == "Chambres Disponibles":
    st.header("Rechercher chambres disponibles")
    date_debut = st.date_input("Date début")
    date_fin = st.date_input("Date fin")

    if date_debut > date_fin:
        st.error("La date de début doit être avant la date de fin.")
    else:
        # Convertir dates en string au format ISO
        dd_str = date_debut.strftime('%Y-%m-%d')
        df_str = date_fin.strftime('%Y-%m-%d')

        query = '''
        SELECT Chambre.id, Chambre.numero, Chambre.etage, TypeChambre.type
        FROM Chambre
        JOIN TypeChambre ON Chambre.type_chambre_id = TypeChambre.id
        WHERE Chambre.id NOT IN (
            SELECT chambre_id FROM Reservation
            WHERE NOT(date_fin < ? OR date_debut > ?)
        )
        ORDER BY Chambre.numero
        '''
        c.execute(query, (dd_str, df_str))
        chambres = c.fetchall()
        if chambres:
            for ch in chambres:
                st.write(f"Chambre {ch[1]} (Étage {ch[2]}) - Type: {ch[3]}")
        else:
            st.write("Aucune chambre disponible sur cette période.")

elif choice == "Ajouter Client":
    st.header("Ajouter un nouveau client")
    nom = st.text_input("Nom complet")
    email = st.text_input("Email")
    ville = st.text_input("Ville")
    adresse = st.text_input("Adresse")
    code_postal = st.text_input("Code postal")
    telephone = st.text_input("Téléphone")

    if st.button("Ajouter Client"):
        if nom and email and ville and adresse and code_postal and telephone:
            c.execute("INSERT INTO Client (nom, email, ville, adresse, code_postal, telephone) VALUES (?, ?, ?, ?, ?, ?)",
                      (nom, email, ville, adresse, int(code_postal), telephone))
            conn.commit()
            st.success("Client ajouté avec succès.")
        else:
            st.error("Veuillez remplir tous les champs.")

elif choice == "Ajouter Réservation":
    st.header("Ajouter une réservation")
    c.execute("SELECT id, nom FROM Client")
    clients = c.fetchall()
    client_dict = {f"{c[1]} (ID:{c[0]})": c[0] for c in clients}
    client_selection = st.selectbox("Client", list(client_dict.keys()))

    c.execute('''
    SELECT Chambre.id, Chambre.numero, TypeChambre.type FROM Chambre
    JOIN TypeChambre ON Chambre.type_chambre_id = TypeChambre.id
    ''')
    chambres = c.fetchall()
    chambre_dict = {f"N°{ch[1]} - {ch[2]} (ID:{ch[0]})": ch[0] for ch in chambres}
    chambre_selection = st.selectbox("Chambre", list(chambre_dict.keys()))

    date_debut = st.date_input("Date début réservation")
    date_fin = st.date_input("Date fin réservation")

    if st.button("Ajouter Réservation"):
        if date_debut > date_fin:
            st.error("La date de début doit être avant la date de fin.")
        else:
            # Vérifier si la chambre est disponible
            dd_str = date_debut.strftime('%Y-%m-%d')
            df_str = date_fin.strftime('%Y-%m-%d')
            chambre_id = chambre_dict[chambre_selection]

            c.execute('''
            SELECT COUNT(*) FROM Reservation
            WHERE chambre_id = ? AND NOT(date_fin < ? OR date_debut > ?)
            ''', (chambre_id, dd_str, df_str))
            (count,) = c.fetchone()

            if count == 0:
                c.execute('''
                INSERT INTO Reservation (date_debut, date_fin, client_id, chambre_id)
                VALUES (?, ?, ?, ?)
                ''', (dd_str, df_str, client_dict[client_selection], chambre_id))
                conn.commit()
                st.success("Réservation ajoutée avec succès.")
            else:
                st.error("Cette chambre est déjà réservée pendant cette période.")
