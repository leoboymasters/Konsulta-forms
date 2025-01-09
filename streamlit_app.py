import streamlit as st
import datetime
import json

def calculate_section_progress(section_data):
    """Calculate the completion percentage of a form section"""
    if not section_data:
        return 0
    
    # Define all required fields for General Info section
    required_fields = [
        'last_name', 'first_name', 'middle_name', 'age', 'sex', 'birthdate',
        'purok', 'barangay', 'municipality', 'contact', 'email', 'philhealth_pin',
        'member_type', 'registration_date', 'facility_choice1', 'facility_choice2', 
        'facility_choice3', 'appointment_date'
    ]
    
    filled_required_fields = sum(1 for field in required_fields 
                               if field in section_data and section_data[field])
    
    percentage = (filled_required_fields / len(required_fields)) * 100
    return round(percentage)

def main():
    st.set_page_config(page_title="Health Assessment Tool", layout="wide")
    
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'general_info': {field: '' for field in [
                'last_name', 'first_name', 'middle_name', 'age', 'sex', 'birthdate',
                'purok', 'barangay', 'municipality', 'contact', 'email', 'philhealth_pin',
                'member_type', 'registration_date', 'facility_choice1', 'facility_choice2', 
                'facility_choice3', 'appointment_date'
            ]},
            'medical_history': {'conditions': []},
            'social_history': {},
            'immunization': {},
            'physical_exam': {},
            'ncd_assessment': {}
        }

    st.title("Konsulta Health Assessment Tool")

    sections = [
        ("General Info", 'general_info'),
        ("Medical History", 'medical_history'),
        ("Social History", 'social_history'),
        ("Immunization", 'immunization'),
        ("Physical Examination", 'physical_exam'),
        ("NCD Assessment", 'ncd_assessment')
    ]

    for title, key in sections:
        current_progress = calculate_section_progress(st.session_state.form_data[key])
        
        with st.expander(f"{title} - {current_progress}% Complete"):
            st.progress(current_progress/100)
            
            if key == 'general_info':
                st.markdown("##### GENERAL DATA AND KONSULTA REGISTRATION")
                
                # Full Name
                st.markdown("**FULL NAME**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    last_name = st.text_input("LAST", key=f"{key}_last_name")
                    st.session_state.form_data[key]['last_name'] = last_name
                with col2:
                    first_name = st.text_input("FIRST", key=f"{key}_first_name")
                    st.session_state.form_data[key]['first_name'] = first_name
                with col3:
                    middle_name = st.text_input("MIDDLE", key=f"{key}_middle_name")
                    st.session_state.form_data[key]['middle_name'] = middle_name

                # Age, Sex, Birthdate
                col1, col2, col3 = st.columns(3)
                with col1:
                    age = st.number_input("AGE", min_value=0, max_value=150, key=f"{key}_age")
                    st.session_state.form_data[key]['age'] = age
                with col2:
                    sex = st.radio("SEX", ['F', 'M'], horizontal=True, key=f"{key}_sex")
                    st.session_state.form_data[key]['sex'] = sex
                with col3:
                    birthdate = st.date_input("BIRTHDATE", key=f"{key}_birthdate")
                    st.session_state.form_data[key]['birthdate'] = birthdate.strftime('%Y-%m-%d')

                # Address
                st.markdown("**ADDRESS**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    purok = st.text_input("PUROK", key=f"{key}_purok")
                    st.session_state.form_data[key]['purok'] = purok
                with col2:
                    barangay = st.text_input("BARANGAY", key=f"{key}_barangay")
                    st.session_state.form_data[key]['barangay'] = barangay
                with col3:
                    municipality = st.text_input("MUNICIPALITY", key=f"{key}_municipality")
                    st.session_state.form_data[key]['municipality'] = municipality

                # Contact Details
                col1, col2 = st.columns(2)
                with col1:
                    contact = st.text_input("CONTACT #", key=f"{key}_contact")
                    st.session_state.form_data[key]['contact'] = contact
                with col2:
                    email = st.text_input("E-MAIL", key=f"{key}_email")
                    st.session_state.form_data[key]['email'] = email

                # PhilHealth
                philhealth_pin = st.text_input("PHILHEALTH PIN", key=f"{key}_philhealth_pin")
                st.session_state.form_data[key]['philhealth_pin'] = philhealth_pin

                # Konsulta Registration
                st.markdown("**KONSULTA REGISTRATION**")
                col1, col2 = st.columns(2)
                with col1:
                    member_type = st.radio("MEMBER TYPE", ['MEMBER', 'DEPENDENT'], key=f"{key}_member_type")
                    st.session_state.form_data[key]['member_type'] = member_type
                with col2:
                    registration_date = st.date_input("REGISTRATION DATE", key=f"{key}_registration_date")
                    st.session_state.form_data[key]['registration_date'] = registration_date.strftime('%Y-%m-%d')

                # Facility Choices
                st.markdown("**PREFERRED FACILITY AND ADDRESS**")
                facility_choice1 = st.text_input("CHOICE 1:", key=f"{key}_facility_choice1")
                facility_choice2 = st.text_input("CHOICE 2:", key=f"{key}_facility_choice2")
                facility_choice3 = st.text_input("CHOICE 3:", key=f"{key}_facility_choice3")
                st.session_state.form_data[key]['facility_choice1'] = facility_choice1
                st.session_state.form_data[key]['facility_choice2'] = facility_choice2
                st.session_state.form_data[key]['facility_choice3'] = facility_choice3

                # Authorization Transaction
                st.markdown("**AUTHORIZATION TRANSACTION**")
                col1, col2 = st.columns(2)
                with col1:
                    atc = st.checkbox("AT CODE:", key=f"{key}_atc")
                    st.session_state.form_data[key]['atc'] = atc
                with col2:
                    appointment_date = st.date_input("DATE OF APPOINTMENT", key=f"{key}_appointment_date")
                    st.session_state.form_data[key]['appointment_date'] = appointment_date.strftime('%Y-%m-%d')
                    face_capture = st.checkbox("FACE CAPTURE (If no ATC)", key=f"{key}_face_capture")
                    st.session_state.form_data[key]['face_capture'] = face_capture

                st.caption(f"Section Progress: {current_progress}%")

            # ... (previous imports and initial code remains the same)

            elif key == 'medical_history':
                st.markdown("##### PAST MEDICAL HISTORY")
                
                col1, col2 = st.columns(2)
                with col1:
                    # Past Medical History column
                    conditions = {
                        'Allergy': True,
                        'Asthma': False,
                        'Cancer': True,
                        'Cerebrovascular Disease': False,
                        'Coronary Artery Disease': False,
                        'Diabetes Mellitus': False,
                        'Emphysema': False,
                        'Epilepsy / Seizure Disorder': False,
                        'Hepatitis': True,
                        'Hyperlipidemia': False,
                        'Hypertension': True,
                        'Peptic Ulcer': False,
                        'Pneumonia': False,
                        'Thyroid Disease': False,
                        'PTB': True,
                        'Urinary Tract Infection': False,
                        'Mental Illnesses': False
                    }

                    for condition, needs_specify in conditions.items():
                        col_check, col_input = st.columns([1, 3])
                        with col_check:
                            selected = st.checkbox(condition, key=f"{key}_{condition.lower().replace(' ', '_')}")
                        with col_input:
                            if needs_specify and selected:
                                if condition == 'Hypertension':
                                    st.text_input("Highest BP (mmHg)", key=f"{key}_{condition.lower()}_bp")
                                elif condition == 'PTB':
                                    st.text_input("Specify Extra PTB", key=f"{key}_{condition.lower()}_extra")
                                else:
                                    st.text_input("Specify", key=f"{key}_{condition.lower()}_specify")

                    # Others field
                    others = st.text_input("Others", key=f"{key}_others")
                    
                    # Past Surgeries
                    st.text_input("Past Surgery/ies Done", key=f"{key}_surgeries")
                    st.text_input("Date Done", key=f"{key}_surgery_date")

                with col2:
                    # Immunization Section
                    st.markdown("##### IMMUNIZATION")
                    
                    st.markdown("**Children**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.checkbox("BCG", key="bcg")
                        st.checkbox("DPT1", key="dpt1")
                        st.checkbox("Hepa1", key="hepa1")
                    with col_b:
                        st.checkbox("OPV1", key="opv1")
                        st.checkbox("DPT2", key="dpt2")
                        st.checkbox("Hepa2", key="hepa2")
                        
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.checkbox("OPV2", key="opv2")
                        st.checkbox("DPT3", key="dpt3")
                        st.checkbox("Hepa3", key="hepa3")
                    with col_b:
                        st.checkbox("OPV3", key="opv3")
                        st.checkbox("Measles", key="measles")
                        st.checkbox("Varicella", key="varicella")
                    
                    st.markdown("**Adult**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.checkbox("HPV", key="hpv")
                    with col_b:
                        st.checkbox("MMR", key="mmr")
                        st.checkbox("None", key="none_adult")
                    
                    st.markdown("**Elderly and Immunocompromised**")
                    st.checkbox("Pneumococcal Vaccine", key="pneumococcal")
                    st.checkbox("Flu Vaccine", key="flu")
                    st.text_input("Others", key="other_immunization")

                # Family Planning
                st.markdown("##### FAMILY PLANNING")
                st.checkbox("With access to family planning counseling", key="fp_counseling")
                st.text_input("Provider", key="fp_provider")
                st.text_input("Birth Control Method used", key="birth_control")

                # Menstrual History
                st.markdown("##### MENSTRUAL HISTORY")
                col1, col2 = st.columns(2)
                with col1:
                    st.number_input("Menarche (yrs old)", key="menarche_age", min_value=0)
                    st.number_input("Onset of sexual intercourse (yrs old)", key="sexual_onset_age", min_value=0)
                    st.date_input("Last Menstrual Period", key="last_menstrual")
                with col2:
                    st.number_input("Period Duration (days)", key="period_duration", min_value=0)
                    st.number_input("No. of pads/day", key="pads_per_day", min_value=0)
                    st.number_input("Interval cycle (days)", key="interval_cycle", min_value=0)
                    st.radio("Menopause", ["Yes", "No"], key="menopause")

                # Pregnancy History
                st.markdown("##### PREGNANCY HISTORY")
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("G___ P___ (T___ A___ L___)", key="pregnancy_history")
                with col2:
                    st.text_input("Type of Delivery", key="delivery_type")
                st.radio("Pregnancy Induced Hypertension", ["Yes", "No"], key="pregnancy_hypertension")

                st.caption(f"Section Progress: {current_progress}%")

# ... (rest of the code remains the same)

    if st.button("Submit Assessment", type="primary"):
        overall_progress = sum(st.session_state.section_progress.values()) / len(sections)
        if overall_progress < 80:
            st.error(f"Please complete at least 80% of the form. Current progress: {overall_progress:.1f}%")
        else:
            st.success(f"Assessment submitted successfully! Overall completion: {overall_progress:.1f}%")

if __name__ == "__main__":
    main()