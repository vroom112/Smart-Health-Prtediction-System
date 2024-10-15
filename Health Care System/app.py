import streamlit as st
import joblib
import pandas as pd
import time
from fpdf import FPDF

# Set up Streamlit page configuration
st.set_page_config(page_title="Smart Health Prediction System", layout="centered")

# loading model and list of symptoms
model = joblib.load("saved_model/random_f.joblib")
symptoms_list = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

# Custom CSS styling to enhance colors and layout
st.markdown("""
<style>
    body {
        background-color: #f9f9f9;
        font-family: Arial, sans-serif;
    }
    .big-title {
        font-size: 48px;
        color: #007BFF; 
        text-align: center;
        animation: fadeIn 1.5s;
    }
    .header {
        color: #28A745;
        text-align: center;
        animation: fadeIn 1.5s;
    }
    .stTextInput input, .stTextArea textarea {
        border: 2px solid #007BFF;
        border-radius: 6px;
        padding: 10px;
    }
    .stButton button {
        background-color: #007BFF; 
        color: white;
        padding: 10px 20px;
        border: None;
        border-radius: 5px;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #0056b3; 
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .warning {
        background-color: #ffd5d5;
        color: #856404;
        border: 1px solid #ffeeba;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Start of Streamlit UI
st.title("The Smart Health Prediction System", anchor="home")
st.markdown("<h3 class='header'>Welcome to our health prediction system.</h3>", unsafe_allow_html=True)

# Add an image
st.image("C:/Users/Tadiwanashe/Documents/Health Care System/images/hologram-feminine-silhouette-man-hand.jpg", caption="Health Awareness", use_column_width=True)
st.header("Let's Talk About Your Symptoms 🩺")

# Initialize session state
if 'symptoms' not in st.session_state:
    st.session_state.symptoms = []
    st.session_state.prediction = None
    st.session_state.age = None
    st.session_state.gender = None
    st.session_state.medical_history = []
    st.session_state.name = None  # Initialize name in session state

# Input for demographic information
st.sidebar.header("Demographic Information")
name = st.sidebar.text_input("Enter your name:")
age = st.sidebar.number_input("Enter your age:", min_value=0, max_value=120, value=30)
gender = st.sidebar.selectbox("Select your gender:", options=["Select...", "Male", "Female", "Other"])
medical_history_input = st.sidebar.text_area("Any pre-existing medical conditions (comma-separated):", "")

if st.sidebar.button("Submit Demographic Information"):
    if name and age is not None and gender != "Select...":
        st.session_state.name = name
        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.medical_history = [condition.strip() for condition in medical_history_input.split(",")] if medical_history_input else []
        st.sidebar.success("Demographic information submitted!")
    else:
        st.sidebar.warning("Please fill in all fields.")

# Symptom selection
st.sidebar.title("Symptom Selection")
st.sidebar.subheader("Choose your symptoms:")
symptom_input = st.sidebar.selectbox('Select a symptom from the list:', options=symptoms_list)

# Adding/removing symptoms
if st.sidebar.button("Add Symptom"):
    if symptom_input:
        st.session_state.symptoms.append(symptom_input)
        st.sidebar.success(f"{symptom_input} added!")
        
if st.session_state.symptoms:
    symptom_to_remove = st.sidebar.selectbox('Select a symptom to remove:', options=["Select..."] + st.session_state.symptoms)
    if st.sidebar.button("Remove Symptom"):
        if symptom_to_remove != "Select..." and symptom_to_remove in st.session_state.symptoms:
            st.session_state.symptoms.remove(symptom_to_remove)
            st.sidebar.success(f"{symptom_to_remove} removed!")

# Display selected symptoms and demographic info
if st.session_state.symptoms:
    st.subheader("Your Selected Symptoms:")
    st.write(", ".join(st.session_state.symptoms))

if st.session_state.name and st.session_state.age is not None and st.session_state.gender:
    st.subheader("Your Demographic Information:")
    st.write(f"**Name:** {st.session_state.name}")
    st.write(f"**Age:** {st.session_state.age}")
    st.write(f"**Gender:** {st.session_state.gender}")
    if st.session_state.medical_history:
        st.write(f"**Medical History:** {', '.join(st.session_state.medical_history)}")

# Evaluate symptoms when button clicked
if st.sidebar.button("Evaluate Symptoms"):
    with st.spinner('Predicting output...'):
        time.sleep(1)
        if st.session_state.symptoms:
            # Prepare model input
            prediction_value = [1 if sym in st.session_state.symptoms else 0 for sym in symptoms_list]
            query = pd.DataFrame(prediction_value).T

            # Add demographic information to the prediction input
            query.loc['age'] = st.session_state.age
            gender_encoded = 0 if st.session_state.gender == 'Male' else (1 if st.session_state.gender == 'Female' else 2)
            query.loc['gender'] = gender_encoded
            query.index = query.index.astype(str)

            # Convert medical history to features
            for condition in st.session_state.medical_history:
                if condition in symptoms_list:
                    query.loc[condition] = 1

            query = query.T  

            # Handle missing values
            query.fillna(0, inplace=True)

            # Make prediction
            st.session_state.prediction = model.predict(query)[0]
            st.success("Prediction complete!")

# Summary Output Section
if st.session_state.prediction is not None:
    st.subheader("Summary of Your Health Information:")
    st.write("### Selected Symptoms:")
    st.write(", ".join(st.session_state.symptoms))
    st.write("### Diagnosis Result:")
    st.warning(f"**Diagnosis:** {st.session_state.prediction}")

    # Recommendations based on prediction
    st.write("### Recommendations for Further Action:")
    if st.session_state.prediction == "Diabetes":
        st.info("Consult a healthcare provider for fasting blood glucose tests and lifestyle modifications.")
    elif st.session_state.prediction == "Hypertension":
        st.info("Monitor your blood pressure and discuss dietary changes with a healthcare provider.")

    # Option to copy summary to clipboard
    summary_text = (
        f"Name: {st.session_state.name}\n"
        f"Selected Symptoms: {', '.join(st.session_state.symptoms)}\n"
        f"Diagnosis: {st.session_state.prediction}\n"
        f"Age: {st.session_state.age}\n"
        f"Gender: {st.session_state.gender}\n"
        f"Medical History: {', '.join(st.session_state.medical_history)}"
    )
    if st.button("Copy Summary to Clipboard"):
        st.session_state.showing_summary = True
        st.success("Summary copied to clipboard!")

    # Option to download summary as PDF
    if st.button("Download Summary as PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, summary_text)
        pdf_file_path = "symptom_summary.pdf"
        pdf.output(pdf_file_path)
        with open(pdf_file_path, "rb") as f:
            st.download_button("Click here to download the summary", f, file_name=pdf_file_path)

# Footer
st.sidebar.info("Developed by Tadiwanashe Vurumu | © 2024 Smart Health App")