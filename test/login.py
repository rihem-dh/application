import hashlib
import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import LoginError
from streamlit_option_menu import option_menu

# Loading config file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Function to hash the password
def hash_password(password):
    h = hashlib.sha256()
    h.update(password.encode('utf-8'))
    return h.hexdigest()

# Function to save user information to YAML file
def save_user_info_to_yaml(username, email, password):
    hashed_password = hash_password(password)
    user_info = {'username': username, 'email': email, 'password': hashed_password}
    with open('users.yaml', 'a') as file:
        yaml.dump(user_info, file)
        
        
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
        st.title("authentifier")

        try:
            authenticator.login()
        except LoginError as e:
            st.error(e)

        if st.session_state.get("authentication_status"):
            
            st.write(f'Welcome *{st.session_state["name"]}*')
            st.title('Some content')
            # Rediriger l'utilisateur vers une autre page après l'authentification
            st.write("Redirecting...")
            st.experimental_set_query_params(logged_in=True)
            st.experimental_rerun()
        elif st.session_state.get("authentication_status") is False:
            st.error('Username/password is incorrect')
        elif st.session_state.get("authentication_status") is None:
            st.warning('Please enter your username and password')


    

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

# Appel de la fonction main
main()
