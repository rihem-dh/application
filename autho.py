import streamlit as st
import streamlit_authenticator


import sqlite3
import hashlib
import os
from streamlit_option_menu import option_menu
from PIL import Image





# Fonction pour hacher le mot de passe

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



# Fonction pour vérifier les informations d'identification dans la base de données
def check_credentials(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password =hash_password(password)
    c.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, hashed_password))
    user_id = c.fetchone()
    conn.close()
    return user_id

def main():
    # Barre de navigation horizontale
    st.markdown(
        """
        <style>
            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
                background-color: #f0f0f0;
            }
            .nav-item {
                margin: 0 10px;
                cursor: pointer;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    selected_option = option_menu(
        menu_title=None,
        options=["Connection", "À propos"],
        icons=['lock', 'house'],
        menu_icon="cast", default_index=0, orientation="horizontal",
    )

    if selected_option == "Connection":
        st.title("Page d'authentification")
        # Créer des zones de saisie pour le nom d'utilisateur et le mot de passe
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):
            # Authentifier l'utilisateur
            user_id = check_credentials(username, password)
            if user_id:
                st.session_state['user_id'] = user_id
                st.success("Connexion réussie ! Redirection vers la page principale...")
                # Redirection vers la page app.py
                os.system("streamlit run app.py --server.enableXsrfProtection=false")
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")

        # Bouton de création d'un compte
        if st.button("Créer un compte"):
            # Redirection vers la page creation.py
            os.system("streamlit run creation.py --server.enableXsrfProtection=false")


    

    elif selected_option == "À propos":
        with st.container():
            
            st.title("À propos de notre application :")
            # Définir le style CSS pour le titre
            title_style = """
                color: #1f77b4;
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                margin-top: 20px;
            """

            # Afficher le titre avec le style personnalisé
            st.markdown(
                f'<p style="{title_style}">"Traducteur de la langue des signes"</p>',
                unsafe_allow_html=True
            )

            # Définir un style pour le texte de la description
            description_style = "font-size: 18px; line-height: 1.6; color: #333;"

            # Afficher la description avec un style personnalisé
            st.markdown(
                """
                <div style="{style}">
                Notre application de traduction de la langue des signes vise à faciliter la communication entre les personnes sourdes ou malentendantes et les personnes entendantes. En utilisant notre application, les utilisateurs peuvent simplement effectuer des gestes de la langue des signes devant leur caméra, importer une image ou une vidéo, et notre système intelligent traduit ces gestes en temps réel en texte ou en discours audible. Cette technologie révolutionnaire permet de surmonter les barrières linguistiques et favorise une communication fluide et efficace dans divers contextes, que ce soit à l'école, au travail ou dans la vie quotidienne.
                </div>
                """.format(style=description_style),
                unsafe_allow_html=True
            )

        # Ajouter une phrase d'introduction avant la vidéo
        st.markdown(
            """
            <br>
            <div style="{style}">
            Pour mieux apprendre la langue des signes, visionnez la vidéo ci-dessous :
            </div>
            """.format(style=description_style),
            unsafe_allow_html=True
        )

        # Ajouter la vidéo avec des contrôles
        video_url = "https://www.youtube.com/watch?v=G6hVRVG74lc"  
        st.video(video_url)

if __name__ == "__main__":
    main()
