import cv2
from PIL import Image
import streamlit as st
from ultralytics import YOLO
from streamlit_option_menu import option_menu
import sqlite3


def get_profile_data(user_id):
    # Se connecter à la base de données SQLite
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Exécuter la requête SQL pour récupérer les informations du profil de l'utilisateur
    cursor.execute("SELECT name, email, profile_image FROM users WHERE id=?", (user_id,))
    profile_data = cursor.fetchone()

    # Fermer la connexion à la base de données
    conn.close()

    return profile_data


st.set_page_config(page_title="Object Detect App", layout="wide")
st.markdown(
    """
        <style>
            .{
                margin:0;
                
            }
            .css-uf99v8 {
            display: flex;
            flex-direction: column;
            width: 80%;
            overflow: auto;
            margin: 0 auto;
            -webkit-box-align: center;
            align-items: center;
            text-align: justify;
        }
        
        </style>
        """,
        unsafe_allow_html=True
)

def acceuil():

    selected = option_menu(
        menu_title=None,
        options=["Home","Profil", "Traduction From Image", "Traduction From Video", "Traduction Using WebCam"],
        icons=['house','person', 'image', "file-play", 'camera-video'],
        menu_icon="cast", default_index=0, orientation="horizontal",
        
    )
    if selected == "Home":
        st.title("Sign Language Translator")
        
        st.write('##### Welcome to our Sign Language Translation app powered by AI, where communication barriers dissolve as gestures are seamlessly translated into spoken language.!')
        st.image('image1.jpg')
    elif selected == "Traduction From Image":
        image_object_detect()
    elif selected == "Traduction From Video":
        video_object_detect()
    elif selected == "Traduction Using WebCam":
        webcam_object_detect()
    elif selected == "Profil":
        profil_page()

#Image 
def detect_image(path_model,path_img):
    # Run batched inference on a list of images
    model = YOLO(path_model) 
    results = model(path_img)  

    # Process results list
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        result.save(filename='result.jpg')  # save to disk

def image_object_detect():
    st.title('Traduction From Image')
    st.write("##### Welcome to our Traduction From Image Interface! Upload your image and Let our advanced algorithms translate your signs.ur app utilizes AI-powered computer vision algorithms to translate sign language from an image, accurately detecting and interpreting hand gestures, converting them into text for comprehension.!")
    
    
    model_path = "best.pt"
    
   
    model_path = "best.pt"
    col1, col2 = st.columns(2)
    with col1:
        uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption='Uploaded Image', width=500)

            if st.button('Traduction'):
                detect_image(model_path,image)
                with col2:
                    co1, col2,col3 = st.columns([1,3,1])
                    with col2:
                        st.header("Result")
                        st.image('result.jpg', caption='Detected Image',  width=500)

            
#video_object_detect()
def detect_video(path_model,video_bytes):
    
    model = YOLO(path_model)
    st_frame = st.empty()
    
    
    # Convert video bytes to file path and open the video
    with open("temp_video.mp4", "wb") as temp_file:
        temp_file.write(video_bytes)

    # Open the video file
    vid_cap = cv2.VideoCapture("temp_video.mp4")

    # Read video frames
    while vid_cap.isOpened():
        ret, frame = vid_cap.read()
        if ret:
            res = model.predict(frame, conf=0.25)
            res_plotted = res[0].plot()
            st_frame.image(res_plotted,
                        caption='Detected Video',
                        channels="BGR",
                        use_column_width=True
                        )

        else:
            vid_cap.release()
            break   
        
def video_object_detect():
    st.title("Traduction from video")
    st.write("##### Welcome to our Video Sign Language Translation Interface! Simply upload your video, and our advanced algorithms will swiftly translate your signs within it. Say goodbye to communication barriers and hello to seamless understanding!")
    model_path = "best.pt"
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload video", type=["mp4", "avi"])
    
        if uploaded_file is not None:
            
            st.video(uploaded_file)
            st.write('Uploded video')
            
            video_bytes = uploaded_file.read()
            
            
            if st.button('traduction'):
                with col2:
                    st.header("Result: \n")
                    detect_video(model_path,video_bytes)

#webcam_object_detect()



def webcam_object_detect():
    st.title("Traduction using WebCam")
    st.write("##### Welcome to our Video Sign Language Translation Interface! With just your webcam, you can effortlessly capture your signs in real-time, allowing our advanced algorithms to swiftly translate them. Bid farewell to communication obstacles and embrace smooth comprehension.")

    # Initialisation de la session_state
    if 'webcam_active' not in st.session_state:
        st.session_state['webcam_active'] = False

    model = YOLO("best.pt")
    source_webcam = 0
    webcam = st.button('Open WebCam')
    stop_button = None  # Initialisation du bouton "Stop WebCam"
    co1, col2,col3 = st.columns([1,3,1])

    if webcam:
        with col2:
            try:
                vid_cap = cv2.VideoCapture(source_webcam)
                st_frame = st.empty()

                # Créer le bouton "Stop WebCam" une seule fois en dehors de la boucle while
                if not st.session_state['webcam_active']:
                    stop_button = st.button('Stop WebCam')

                while (vid_cap.isOpened()):
                    success, image = vid_cap.read()
                    res = model.predict(image, conf=0.35)
                    res_plotted = res[0].plot()
                    if success:
                        st_frame.image(res_plotted,
                                caption='Detected Video',
                                channels="BGR",
                                use_column_width=True
                                )
                    else:
                        vid_cap.release()
                        break
                    
                    # Listen for 'q' key press to stop webcam feed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                    # Traiter l'événement lorsque le bouton "Stop WebCam" est cliqué
                    if stop_button:
                        st.session_state['webcam_active'] = False  # Arrêter la webcam
                        break

            except Exception as e:
                st.sidebar.error("Error loading video: " + str(e))

def profil_page():
    st.title("Profil Page")
    st.write("Welcome to your profile page. Here, you can view and edit your profile information.")

    # Récupérer l'ID de l'utilisateur à partir de la session
    user_id = st.session_state.get('user_id')

    if user_id:
        # Récupérer les données du profil de l'utilisateur
        profile_data = get_profile_data(user_id)

        if profile_data:
            # Afficher les données du profil
            st.write(f"Name: {profile_data[0]}")
            st.write(f"Email: {profile_data[1]}")
            # Afficher l'image de profil
            st.image(profile_data[5], caption='Profile Image', use_column_width=True)
        else:
            st.write("User not found.")
    else:
        st.error("You are not logged in.")

acceuil()