import streamlit as st
import datetime
import json
from typing import Dict, List, Any

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
            'general_info': {},
            'medical_history': {},
            'social_history': {},
            'immunization': {},
            'physical_exam': {},
            'ncd_assessment': {}
        }

    st.title("Konsulta Health Assessment Tool")

    sections = [
        ("General Data and Konsulta Registration", 'general_info'),
        ("Health Assessment Tool", 'medical_history'),
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
                # Header with peach/salmon background
                st.markdown("""
                    <div style='background-color: #FFCDB2; padding: 10px; text-align: center;'>
                        <h3>GENERAL DATA AND KONSULTA REGISTRATION</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                # Full Name
                st.markdown("**FULL NAME**")
                cols = st.columns([1, 1, 1])
                with cols[0]:
                    last_name = st.text_input("LAST", key=f"{key}_last_name", 
                        value=st.session_state.form_data[key].get('last_name', ''))
                    st.session_state.form_data[key]['last_name'] = last_name
                with cols[1]:
                    first_name = st.text_input("FIRST", key=f"{key}_first_name",
                        value=st.session_state.form_data[key].get('first_name', ''))
                    st.session_state.form_data[key]['first_name'] = first_name
                with cols[2]:
                    middle_name = st.text_input("MIDDLE", key=f"{key}_middle_name",
                        value=st.session_state.form_data[key].get('middle_name', ''))
                    st.session_state.form_data[key]['middle_name'] = middle_name

                # Age and Sex and Birthdate in one line
                cols = st.columns([1, 2, 2])
                with cols[0]:
                    st.markdown("**AGE**")
                    age = st.number_input("", min_value=0, max_value=150, key=f"{key}_age",
                        value=int(st.session_state.form_data[key].get('age', 0)))
                    st.session_state.form_data[key]['age'] = age
                with cols[1]:
                    st.markdown("**SEX**")
                    sex = st.radio("", ['F', 'M'], horizontal=True, key=f"{key}_sex",
                        index=0 if st.session_state.form_data[key].get('sex', 'F') == 'F' else 1)
                    st.session_state.form_data[key]['sex'] = sex
                with cols[2]:
                    st.markdown("**BIRTHDATE** (MM/DD/YYYY)")
                    birthdate = st.date_input("", key=f"{key}_birthdate")
                    st.session_state.form_data[key]['birthdate'] = birthdate.strftime('%Y-%m-%d')

                # Address
                st.markdown("**ADDRESS**")
                cols = st.columns([1, 1, 1])
                with cols[0]:
                    purok = st.text_input("PUROK", key=f"{key}_purok",
                        value=st.session_state.form_data[key].get('purok', ''))
                    st.session_state.form_data[key]['purok'] = purok
                with cols[1]:
                    barangay = st.text_input("BARANGAY", key=f"{key}_barangay",
                        value=st.session_state.form_data[key].get('barangay', ''))
                    st.session_state.form_data[key]['barangay'] = barangay
                with cols[2]:
                    municipality = st.text_input("MUNICIPALITY", key=f"{key}_municipality",
                        value=st.session_state.form_data[key].get('municipality', ''))
                    st.session_state.form_data[key]['municipality'] = municipality

                # Contact and Email
                cols = st.columns([1, 1])
                with cols[0]:
                    contact = st.text_input("CONTACT #", key=f"{key}_contact",
                        value=st.session_state.form_data[key].get('contact', ''))
                    st.session_state.form_data[key]['contact'] = contact
                with cols[1]:
                    email = st.text_input("E-MAIL", key=f"{key}_email",
                        value=st.session_state.form_data[key].get('email', ''))
                    st.session_state.form_data[key]['email'] = email

                # PhilHealth PIN
                philhealth_pin = st.text_input("PHILHEALTH PIN", key=f"{key}_philhealth_pin",
                    value=st.session_state.form_data[key].get('philhealth_pin', ''))
                st.session_state.form_data[key]['philhealth_pin'] = philhealth_pin

                # Member Type and Registration Date with KPP Sign
                cols = st.columns([2, 2, 1])
                with cols[0]:
                    st.markdown("**MEMBER TYPE**")
                    member_type = st.radio("", ['MEMBER', 'DEPENDENT'], key=f"{key}_member_type", horizontal=True,
                        index=0 if st.session_state.form_data[key].get('member_type', 'MEMBER') == 'MEMBER' else 1)
                    st.session_state.form_data[key]['member_type'] = member_type
                    specify = st.text_input("Specify:", key=f"{key}_member_specify",
                        value=st.session_state.form_data[key].get('member_specify', ''))
                    st.session_state.form_data[key]['member_specify'] = specify
                with cols[1]:
                    st.markdown("**REGISTRATION DATE** (MM/DD/YYYY)")
                    registration_date = st.date_input("", key=f"{key}_registration_date")
                    st.session_state.form_data[key]['registration_date'] = registration_date.strftime('%Y-%m-%d')
                with cols[2]:
                    st.markdown("**KPP SIGN**")
                    st.markdown("________")

                # KONSULTA REGISTRATION header
                st.markdown("""
                    <div style='background-color: white; padding: 5px;'>
                        <h4>KONSULTA REGISTRATION</h4>
                    </div>
                """, unsafe_allow_html=True)

                # Preferred Facility
                st.markdown("**PREFERRED FACILITY AND ADDRESS**")
                
                # Facility choices with checkboxes
                cols = st.columns([4, 1])
                with cols[0]:
                    facility_choice1 = st.text_input("CHOICE 1:", key=f"{key}_facility_choice1",
                        value=st.session_state.form_data[key].get('facility_choice1', ''))
                with cols[1]:
                    choice1_check = st.checkbox("", key=f"{key}_choice1_check")
                st.session_state.form_data[key]['facility_choice1'] = facility_choice1
                st.session_state.form_data[key]['choice1_check'] = choice1_check

                cols = st.columns([4, 1])
                with cols[0]:
                    facility_choice2 = st.text_input("CHOICE 2:", key=f"{key}_facility_choice2",
                        value=st.session_state.form_data[key].get('facility_choice2', ''))
                with cols[1]:
                    choice2_check = st.checkbox("", key=f"{key}_choice2_check")
                st.session_state.form_data[key]['facility_choice2'] = facility_choice2
                st.session_state.form_data[key]['choice2_check'] = choice2_check

                cols = st.columns([4, 1])
                with cols[0]:
                    facility_choice3 = st.text_input("CHOICE 3:", key=f"{key}_facility_choice3",
                        value=st.session_state.form_data[key].get('facility_choice3', ''))
                with cols[1]:
                    choice3_check = st.checkbox("", key=f"{key}_choice3_check")
                st.session_state.form_data[key]['facility_choice3'] = facility_choice3
                st.session_state.form_data[key]['choice3_check'] = choice3_check

                # Authorization Transaction
                st.markdown("**AUTHORIZATION TRANSACTION**")
                cols = st.columns([1, 2, 2])
                with cols[0]:
                    atc = st.checkbox("AT CODE:", key=f"{key}_atc",
                        value=st.session_state.form_data[key].get('atc', False))
                    st.session_state.form_data[key]['atc'] = atc
                with cols[1]:
                    st.markdown("**DATE OF APPOINTMENT**")
                    appointment_date = st.date_input("", key=f"{key}_appointment_date")
                    st.session_state.form_data[key]['appointment_date'] = appointment_date.strftime('%Y-%m-%d')
                with cols[2]:
                    face_capture = st.checkbox("If no ATC, ☐ FACE CAPTURE", key=f"{key}_face_capture",
                        value=st.session_state.form_data[key].get('face_capture', False))
                    st.session_state.form_data[key]['face_capture'] = face_capture

            elif key == 'medical_history':
                # Header with peach/salmon background
                st.markdown("""
                    <div style='background-color: #FFCDB2; padding: 10px; text-align: center;'>
                        <h3>HEALTH ASSESSMENT TOOL</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # PAST MEDICAL HISTORY
                    st.markdown("##### PAST MEDICAL HISTORY")
                    
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
                        'Mental Illnesses': False,
                        'Others': True
                    }

                    for condition, needs_specify in conditions.items():
                        col_check, col_input = st.columns([1, 3])
                        condition_key = condition.lower().replace(' ', '_').replace('/', '_')
                        
                        with col_check:
                            selected = st.checkbox(condition, key=f"{key}_{condition_key}")
                            st.session_state.form_data[key][condition_key] = selected
                        
                        with col_input:
                            if needs_specify and selected:
                                if condition == 'Hypertension':
                                    bp_value = st.text_input("Highest BP (mmHg):", key=f"{key}_{condition_key}_bp")
                                    st.session_state.form_data[key][f"{condition_key}_bp"] = bp_value
                                elif condition == 'PTB':
                                    extra_value = st.text_input("Specify Extra PTB:", key=f"{key}_{condition_key}_extra")
                                    st.session_state.form_data[key][f"{condition_key}_extra"] = extra_value
                                else:
                                    spec_value = st.text_input("Specify:", key=f"{key}_{condition_key}_specify")
                                    st.session_state.form_data[key][f"{condition_key}_specify"] = spec_value
                    
                    # Past Surgery
                    surgery = st.text_input("Past Surgery/ies Done:", key=f"{key}_surgeries")
                    st.session_state.form_data[key]['surgeries'] = surgery
                    
                    date = st.text_input("Date Done:", key=f"{key}_surgery_date")
                    st.session_state.form_data[key]['surgery_date'] = date

                    # FAMILY HISTORY
                    st.markdown("##### FAMILY HISTORY")
                    family_conditions = {
                        'Allergy': True,
                        'Asthma': False,
                        'Cancer': True,
                        'Cerebrovascular Disease': False,
                        'Coronary Artery Disease': False,
                        'Diabetes Mellitus': True,
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
                        'Mental Illnesses': False,
                        'Other': True
                    }

                    for condition, needs_specify in family_conditions.items():
                        col_check, col_input = st.columns([1, 3])
                        condition_key = f"family_{condition.lower().replace(' ', '_').replace('/', '_')}"
                        
                        with col_check:
                            selected = st.checkbox(condition, key=f"{key}_{condition_key}")
                            st.session_state.form_data[key][condition_key] = selected
                        
                        with col_input:
                            if needs_specify and selected:
                                if condition == 'Diabetes Mellitus':
                                    st.text_input("If yes, perform FBS:", key=f"{key}_{condition_key}_fbs")
                                elif condition == 'Hypertension':
                                    st.text_input("Highest BP (mmHg):", key=f"{key}_{condition_key}_bp")
                                elif condition == 'PTB':
                                    st.text_input("Specify Extra PTB:", key=f"{key}_{condition_key}_extra")
                                else:
                                    st.text_input("Specify:", key=f"{key}_{condition_key}_specify")

                    # PERSONAL/SOCIAL HISTORY
                    st.markdown("##### PERSONAL/SOCIAL HISTORY")
                    
                    # Smoking
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown("Smoking")
                    with col2:
                        smoking = st.radio("Smoking Status", ['Yes', 'No', 'Quit'], key=f"{key}_smoking", horizontal=True)
                        st.session_state.form_data[key]['smoking'] = smoking
                    if smoking == 'Yes':
                        pack_years = st.text_input("No. of pack-years:", key=f"{key}_pack_years")
                        st.session_state.form_data[key]['pack_years'] = pack_years

                    # Alcohol
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown("Alcohol")
                    with col2:
                        alcohol = st.radio("Alcohol Status", ['Yes', 'No', 'Quit'], key=f"{key}_alcohol", horizontal=True)
                        st.session_state.form_data[key]['alcohol'] = alcohol
                    if alcohol == 'Yes':
                        servings = st.text_input("No. of servings/day:", key=f"{key}_alcohol_servings")
                        st.session_state.form_data[key]['alcohol_servings'] = servings

                    # Illicit Drugs
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown("Illicit Drugs")
                    with col2:
                        drugs = st.radio("Drug Use Status", ['Yes', 'No', 'Quit'], key=f"{key}_drugs", horizontal=True)
                        st.session_state.form_data[key]['drugs'] = drugs

                    # Sexually Active
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown("Sexually Active")
                    with col2:
                        active = st.radio("Sexually Active Status", ['Yes', 'No', 'Quit'], key=f"{key}_sexually_active", horizontal=True)
                        st.session_state.form_data[key]['sexually_active'] = active

                with col2:
                    # IMMUNIZATION
                    st.markdown("##### IMMUNIZATION")
                    
                    st.markdown("**Children**")
                    col_a, col_b, col_c, col_d = st.columns(4)
                    
                    with col_a:
                        bcg = st.checkbox("BCG", key=f"{key}_bcg")
                        dpt1 = st.checkbox("DPT1", key=f"{key}_dpt1")
                        hepa1 = st.checkbox("Hepa1", key=f"{key}_hepa1")
                        st.session_state.form_data[key].update({'bcg': bcg, 'dpt1': dpt1, 'hepa1': hepa1})
                    
                    with col_b:
                        opv1 = st.checkbox("OPV1", key=f"{key}_opv1")
                        dpt2 = st.checkbox("DPT2", key=f"{key}_dpt2")
                        hepa2 = st.checkbox("Hepa2", key=f"{key}_hepa2")
                        st.session_state.form_data[key].update({'opv1': opv1, 'dpt2': dpt2, 'hepa2': hepa2})

                    with col_c:
                        opv2 = st.checkbox("OPV2", key=f"{key}_opv2")
                        dpt3 = st.checkbox("DPT3", key=f"{key}_dpt3")
                        hepa3 = st.checkbox("Hepa3", key=f"{key}_hepa3")
                        st.session_state.form_data[key].update({'opv2': opv2, 'dpt3': dpt3, 'hepa3': hepa3})

                    with col_d:
                        opv3 = st.checkbox("OPV3", key=f"{key}_opv3")
                        measles = st.checkbox("Measles", key=f"{key}_measles")
                        varicella = st.checkbox("Varicella", key=f"{key}_varicella")
                        st.session_state.form_data[key].update({'opv3': opv3, 'measles': measles, 'varicella': varicella})

                    st.markdown("**Adult**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        hpv = st.checkbox("HPV", key=f"{key}_hpv")
                        st.session_state.form_data[key]['hpv'] = hpv
                    with col2:
                        mmr = st.checkbox("MMR", key=f"{key}_mmr")
                        st.session_state.form_data[key]['mmr'] = mmr
                    with col3:
                        none = st.checkbox("None", key=f"{key}_none")
                        st.session_state.form_data[key]['none'] = none

                    st.markdown("**Elderly and Immunocompromised**")
                    col1, col2 = st.columns(2)
                    with col1:
                        pneumo = st.checkbox("Pneumococcal Vaccine", key=f"{key}_pneumococcal")
                        st.session_state.form_data[key]['pneumococcal'] = pneumo
                    with col2:
                        flu = st.checkbox("Flu Vaccine", key=f"{key}_flu")
                        st.session_state.form_data[key]['flu'] = flu

                    others = st.text_input("Others:", key=f"{key}_immunization_others")
                    st.session_state.form_data[key]['immunization_others'] = others

                    # FAMILY PLANNING
                    st.markdown("##### FAMILY PLANNING")
                    counseling = st.checkbox("With access to family planning counseling", key=f"{key}_fp_counseling")
                    st.session_state.form_data[key]['fp_counseling'] = counseling
                    
                    provider = st.text_input("Provider:", key=f"{key}_fp_provider")
                    st.session_state.form_data[key]['fp_provider'] = provider
                    
                    birth_control = st.text_input("Birth Control Method used:", key=f"{key}_birth_control")
                    st.session_state.form_data[key]['birth_control'] = birth_control

                    # MENSTRUAL HISTORY
                

            st.caption(f"Section Progress: {current_progress}%")

    if st.button("Submit Assessment", type="primary"):
        overall_progress = sum(calculate_section_progress(st.session_state.form_data[key]) for key in ['general_info', 'medical_history', 'immunization', 'family_planning', 'menstrual_history', 'pregnancy_history']) / 6
        if overall_progress < 80:
            st.error(f"Please complete at least 80% of the form. Current progress: {overall_progress:.1f}%")
        else:
            st.success(f"Assessment submitted successfully! Overall completion: {overall_progress:.1f}%")

if __name__ == "__main__":
    main()