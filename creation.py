import streamlit as st
import sqlite3
import os
import hashlib

# Fonction pour créer la table dans la base de données si elle n'existe pas déjà
def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT UNIQUE, 
                 password TEXT, 
                 email TEXT,
                 profile_image BLOB)''')
    conn.commit()
    conn.close()




def hash_password(password):
    # Convertir la variable password en chaîne de caractères si elle est de type bytes
    password_str = password.decode('utf-8') if isinstance(password, bytes) else password
    # Créer un objet de hachage SHA256
    h = hashlib.sha256()
    # Mettre à jour le hachage avec la chaîne de caractères encodée
    h.update(password_str.encode('utf-8'))
    # Récupérer le hachage sous forme de chaîne hexadécimale
    password_hash = h.hexdigest()
    return password_hash

 
    
# Fonction pour insérer un nouvel utilisateur dans la base de données
def insert_user(username, password, email, profile_image):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = hash_password(password)  # Correction du nom de variable
    try:
        c.execute('''INSERT INTO users (username, password, email, profile_image)
                     VALUES (?, ?, ?, ?)''', (username, hashed_password, email, profile_image))
        user_id = c.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        user_id = None  # Utilisateur déjà existant
    conn.close()
    return user_id

def main():
    st.title("Création de compte")

    # Création de la table dans la base de données
    create_table()

    # Formulaire de création de compte
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    email = st.text_input("E-mail")
    profile_image = st.file_uploader("Image de profil", type=["jpg", "jpeg", "png"])

    if st.button("Créer un compte"):
        if username and password and email:
            if profile_image is not None:
                # Convertir l'image en format binaire
                profile_image_binary = profile_image.read()
                hashed_password=hash_password(password)
                user_id = insert_user(username, hashed_password, email, profile_image_binary)
                if user_id is not None:
                    st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                    os.system("streamlit run autho.py --server.enableXsrfProtection=false")
                else:
                    st.error("Nom d'utilisateur ou adresse e-mail déjà utilisé.")
            else:
                st.error("Veuillez télécharger une image de profil.")
        else:
            st.error("Veuillez remplir tous les champs obligatoires.")

if __name__ == "__main__":
    main()
