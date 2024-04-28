import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import RegisterError
import hashlib

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

def register_user():
    st.title("Création de compte")

    try:
        (email_of_registered_user,
        username_of_registered_user,
        name_of_registered_user) = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            save_user_info_to_yaml(username_of_registered_user, email_of_registered_user, name_of_registered_user)
            st.success('User registered successfully')
    except RegisterError as e:
        st.error(e)

if __name__ == "__main__":
    register_user()
