import streamlit as st
import sqlite3
from datetime import datetime

DB_PATH = 'hotel.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def afficher_reservations():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT Reservation.id, dateDebut, dateFin, nomComplet 
        FROM Reservation JOIN Client ON Reservation.id_client = Client.id
        ORDER BY dateDebut
    ''')
    rows = c.fetchall()
    conn.close()
    
    st.write("### Liste des réservations")
    for r in rows:
        st.write(f"ID: {r[0]} | Du {r[1]} au {r[2]} | Client: {r[3]}")

def afficher_clients():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, nomComplet, email, telephone FROM Client ORDER BY nomComplet')
    rows = c.fetchall()
    conn.close()
    
    st.write("### Liste des clients")
    for cdata in rows:
        st.write(f"ID: {cdata[0]} | {cdata[1]} | Email: {cdata[2]} | Tel: {cdata[3]}")

def chambres_disponibles(date_debut, date_fin):
    conn = get_connection()
    c = conn.cursor()
    
    # On récupère les chambres qui ne sont pas réservées pendant la période
    c.execute('''
        SELECT id, numero, etage, fumeur FROM Chambre
        WHERE id NOT IN (
            SELECT id_chambre FROM ChambreReservee
            JOIN Reservation ON ChambreReservee.id_reservation = Reservation.id
            WHERE NOT (
                dateFin < ? OR dateDebut > ?
            )
        )
    ''', (date_debut, date_fin))
    rows = c.fetchall()
    conn.close()
    return rows

def afficher_chambres_disponibles():
    st.write("### Chercher chambres disponibles")
    date_debut = st.date_input("Date début")
    date_fin = st.date_input("Date fin")
    
    if date_fin < date_debut:
        st.error("La date de fin doit être après la date de début.")
        return
    
    if st.button("Rechercher"):
        dispo = chambres_disponibles(date_debut.isoformat(), date_fin.isoformat())
        if dispo:
            for ch in dispo:
                fumeur = "Oui" if ch[3] else "Non"
                st.write(f"ID: {ch[0]} | Numéro: {ch[1]} | Étage: {ch[2]} | Fumeur: {fumeur}")
        else:
            st.write("Aucune chambre disponible pour cette période.")

def ajouter_client():
    st.write("### Ajouter un nouveau client")
    with st.form("form_ajout_client"):
        nom = st.text_input("Nom complet")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.text_input("Code postal")
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        
        valider = st.form_submit_button("Ajouter client")
        
        if valider:
            if not nom or not email:
                st.error("Le nom complet et l'email sont obligatoires.")
            else:
                conn = get_connection()
                c = conn.cursor()
                c.execute('SELECT MAX(id) FROM Client')
                max_id = c.fetchone()[0] or 0
                nouveau_id = max_id + 1
                c.execute('''
                    INSERT INTO Client (id, adresse, ville, codePostal, email, telephone, nomComplet)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (nouveau_id, adresse, ville, code_postal, email, telephone, nom))
                conn.commit()
                conn.close()
                st.success(f"Client '{nom}' ajouté avec l'ID {nouveau_id}.")

def ajouter_reservation():
    st.write("### Ajouter une réservation")
    conn = get_connection()
    c = conn.cursor()
    
    # Récupérer les clients pour un selectbox
    c.execute('SELECT id, nomComplet FROM Client ORDER BY nomComplet')
    clients = c.fetchall()
    client_dict = {f"{nom} (ID {cid})": cid for cid, nom in clients}
    
    c.execute('SELECT id, numero FROM Chambre ORDER BY numero')
    chambres = c.fetchall()
    chambre_dict = {f"Chambre {numero} (ID {cid})": cid for cid, numero in chambres}
    conn.close()
    
    with st.form("form_ajout_reservation"):
        client_sel = st.selectbox("Client", options=list(client_dict.keys()))
        date_debut = st.date_input("Date début réservation")
        date_fin = st.date_input("Date fin réservation")
        chambre_sel = st.multiselect("Chambre(s)", options=list(chambre_dict.keys()))
        
        valider = st.form_submit_button("Ajouter réservation")
        
        if valider:
            if date_fin < date_debut:
                st.error("La date de fin doit être après la date de début.")
                return
            if not chambre_sel:
                st.error("Veuillez sélectionner au moins une chambre.")
                return
            
            conn = get_connection()
            c = conn.cursor()
            c.execute('SELECT MAX(id) FROM Reservation')
            max_res_id = c.fetchone()[0] or 0
            new_res_id = max_res_id + 1
            
            id_client = client_dict[client_sel]
            
            # Insérer réservation
            c.execute('''
                INSERT INTO Reservation (id, dateDebut, dateFin, id_client)
                VALUES (?, ?, ?, ?)
            ''', (new_res_id, date_debut.isoformat(), date_fin.isoformat(), id_client))
            
            # Lier chambres réservées
            for ch in chambre_sel:
                id_chambre = chambre_dict[ch]
                # On pourrait vérifier disponibilité ici mais on suppose que l'utilisateur choisit bien
                c.execute('INSERT INTO ChambreReservee (id_reservation, id_chambre) VALUES (?, ?)', (new_res_id, id_chambre))
            
            conn.commit()
            conn.close()
            st.success(f"Réservation {new_res_id} ajoutée pour le client {client_sel}.")

def main():
    st.title("Gestion Hôtelière")

    menu = ["Liste des réservations", "Liste des clients", "Chambres disponibles", "Ajouter client", "Ajouter réservation"]
    choix = st.sidebar.selectbox("Menu", menu)
    
    if choix == "Liste des réservations":
        afficher_reservations()
    elif choix == "Liste des clients":
        afficher_clients()
    elif choix == "Chambres disponibles":
        afficher_chambres_disponibles()
    elif choix == "Ajouter client":
        ajouter_client()
    elif choix == "Ajouter réservation":
        ajouter_reservation()

if __name__ == '__main__':
    main()
