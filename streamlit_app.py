import streamlit as st
import datetime
import json
from typing import Dict, List, Any

def calculate_section_progress(section_data, section_key='general_info'):
    """Calculate the completion percentage of a form section"""
    if not section_data:
        return 0
    
    if section_key == 'general_info':
        required_fields = [
            'last_name', 'first_name', 'middle_name', 'age', 'sex', 'birthdate',
            'purok', 'barangay', 'municipality', 'contact', 'email', 'philhealth_pin',
            'member_type', 'registration_date', 'facility_choice1', 'facility_choice2', 
            'facility_choice3', 'appointment_date'
        ]
    elif section_key == 'medical_history':
        # Track all medical conditions and their specifications
        base_fields = [
            'past_allergy', 'past_asthma', 'past_cancer', 'past_cerebrovascular_disease',
            'past_coronary_artery_disease', 'past_diabetes_mellitus', 'past_emphysema',
            'past_epilepsy_seizure_disorder', 'past_hepatitis', 'past_hyperlipidemia',
            'past_hypertension', 'past_peptic_ulcer', 'past_pneumonia', 'past_thyroid_disease',
            'past_ptb', 'past_urinary_tract_infection', 'past_mental_illnesses', 'past_others',
            # Family history fields
            'fam_allergy', 'fam_asthma', 'fam_cancer', 'fam_cerebrovascular_disease',
            'fam_coronary_artery_disease', 'fam_diabetes_mellitus', 'fam_emphysema',
            'fam_epilepsy_seizure_disorder', 'fam_hepatitis', 'fam_hyperlipidemia',
            'fam_hypertension', 'fam_peptic_ulcer', 'fam_pneumonia', 'fam_thyroid_disease',
            'fam_ptb', 'fam_urinary_tract_infection', 'fam_mental_illnesses', 'fam_other',
            # Social history fields
            'smoking_status', 'alcohol_status', 'drugs_status', 'sexually_active_status',
            # Physical exam fields
            'height', 'weight', 'bp', 'temp', 'rr', 'blood_type'
        ]
        required_fields = base_fields
    else:
        return 0

    filled_fields = 0
    total_fields = len(required_fields)

    # Count filled fields
    for field in required_fields:
        if field in section_data and section_data[field]:
            # For boolean fields (checkboxes), count them if they're explicitly set
            if isinstance(section_data[field], bool):
                filled_fields += 1
            # For other fields, count them if they have a value
            elif section_data[field]:
                filled_fields += 1
        
        # Check for specification fields if main field is checked
        if field.startswith(('past_', 'fam_')) and field in section_data and section_data[field]:
            spec_field = f"{field}_specify"
            bp_field = f"{field}_bp"
            fbs_field = f"{field}_fbs"
            
            if spec_field in section_data and section_data[spec_field]:
                filled_fields += 1
                total_fields += 1
            elif bp_field in section_data and section_data[bp_field]:
                filled_fields += 1
                total_fields += 1
            elif fbs_field in section_data and section_data[fbs_field]:
                filled_fields += 1
                total_fields += 1

    percentage = (filled_fields / total_fields) * 100 if total_fields > 0 else 0
    return round(percentage)

def render_immunization_section(key):
    """Render immunization section without nested columns"""
    st.markdown("##### IMMUNIZATION")
    
    st.markdown("**Children**")
    # Instead of nesting columns, create a single row of columns
    cols = st.columns(4)
    
    with cols[0]:
        bcg = st.checkbox("BCG", key=f"{key}_bcg")
        dpt1 = st.checkbox("DPT1", key=f"{key}_dpt1")
        hepa1 = st.checkbox("Hepa1", key=f"{key}_hepa1")
        st.session_state.form_data[key].update({'bcg': bcg, 'dpt1': dpt1, 'hepa1': hepa1})
    
    with cols[1]:
        opv1 = st.checkbox("OPV1", key=f"{key}_opv1")
        dpt2 = st.checkbox("DPT2", key=f"{key}_dpt2")
        hepa2 = st.checkbox("Hepa2", key=f"{key}_hepa2")
        st.session_state.form_data[key].update({'opv1': opv1, 'dpt2': dpt2, 'hepa2': hepa2})

    with cols[2]:
        opv2 = st.checkbox("OPV2", key=f"{key}_opv2")
        dpt3 = st.checkbox("DPT3", key=f"{key}_dpt3")
        hepa3 = st.checkbox("Hepa3", key=f"{key}_hepa3")
        st.session_state.form_data[key].update({'opv2': opv2, 'dpt3': dpt3, 'hepa3': hepa3})

    with cols[3]:
        opv3 = st.checkbox("OPV3", key=f"{key}_opv3")
        measles = st.checkbox("Measles", key=f"{key}_measles")
        varicella = st.checkbox("Varicella", key=f"{key}_varicella")
        st.session_state.form_data[key].update({'opv3': opv3, 'measles': measles, 'varicella': varicella})

    st.markdown("**Adult**")
    adult_cols = st.columns(3)
    with adult_cols[0]:
        hpv = st.checkbox("HPV", key=f"{key}_hpv")
        st.session_state.form_data[key]['hpv'] = hpv
    with adult_cols[1]:
        mmr = st.checkbox("MMR", key=f"{key}_mmr")
        st.session_state.form_data[key]['mmr'] = mmr
    with adult_cols[2]:
        none = st.checkbox("None", key=f"{key}_none")
        st.session_state.form_data[key]['none'] = none

    st.markdown("**Elderly and Immunocompromised**")
    elderly_cols = st.columns(2)
    with elderly_cols[0]:
        pneumo = st.checkbox("Pneumococcal Vaccine", key=f"{key}_pneumococcal")
        st.session_state.form_data[key]['pneumococcal'] = pneumo
    with elderly_cols[1]:
        flu = st.checkbox("Flu Vaccine", key=f"{key}_flu")
        st.session_state.form_data[key]['flu'] = flu

    others = st.text_input("Others:", key=f"{key}_immunization_others")
    st.session_state.form_data[key]['immunization_others'] = others

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
        ("Health Assessment Tool", 'medical_history')
    ]

    for title, key in sections:
        current_progress = calculate_section_progress(st.session_state.form_data[key], key)
        
        with st.expander(f"{title} - {current_progress}% Complete"):
            st.progress(current_progress/100)
            
            if key == 'general_info':
                st.markdown("<h3 style='text-align: center;'>GENERAL DATA AND KONSULTA REGISTRATION</h3>", unsafe_allow_html=True)
                
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
                for i in range(1, 4):
                    cols = st.columns([4, 1])
                    with cols[0]:
                        facility = st.text_input(f"CHOICE {i}:", key=f"{key}_facility_choice{i}",
                            value=st.session_state.form_data[key].get(f'facility_choice{i}', ''))
                        st.session_state.form_data[key][f'facility_choice{i}'] = facility
                    with cols[1]:
                        choice_check = st.checkbox("", key=f"{key}_choice{i}_check",
                            value=st.session_state.form_data[key].get(f'choice{i}_check', False))
                        st.session_state.form_data[key][f'choice{i}_check'] = choice_check

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
                st.markdown("<h3 style='text-align: center;'>HEALTH ASSESSMENT TOOL</h3>", unsafe_allow_html=True)
                
                tabs = st.tabs([
                    "Medical History", "Family History", "Social History", 
                    "Family Planning", "Menstrual History", "Pregnancy History",
                    "Physical Examination", "Pediatric Assessment"
                ])
                
                with tabs[0]:
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
                        cols = st.columns([1, 3])
                        # Ensure unique keys by adding 'past_' prefix
                        key_base = f"past_{condition.lower().replace(' ', '_').replace('/', '_')}"
                        
                        with cols[0]:
                            selected = st.checkbox(condition, key=f"past_med_{key_base}")
                            st.session_state.form_data[key][key_base] = selected
                        
                        with cols[1]:
                            if needs_specify and selected:
                                if condition == 'Hypertension':
                                    bp_value = st.text_input("Highest BP (mmHg):", key=f"past_med_{key_base}_bp")
                                    st.session_state.form_data[key][f"{key_base}_bp"] = bp_value
                                elif condition == 'PTB':
                                    extra_value = st.text_input("Specify Extra PTB:", key=f"past_med_{key_base}_extra")
                                    st.session_state.form_data[key][f"{key_base}_extra"] = extra_value
                                else:
                                    spec_value = st.text_input("Specify:", key=f"past_med_{key_base}_specify")
                                    st.session_state.form_data[key][f"{key_base}_specify"] = spec_value
                    
                    # Past Surgery
                    st.markdown("**Past Surgery/ies Done:**")
                    cols = st.columns([1, 1])
                    with cols[0]:
                        surgery = st.text_input("Surgery:", key=f"{key}_surgeries")
                        st.session_state.form_data[key]['surgeries'] = surgery
                    with cols[1]:
                        date = st.text_input("Date Done:", key=f"{key}_surgery_date")
                        st.session_state.form_data[key]['surgery_date'] = date

                with tabs[1]:
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
                        cols = st.columns([1, 3])
                        # Ensure unique keys by adding 'fam_' prefix and avoiding conflict with past medical history
                        key_base = f"fam_{condition.lower().replace(' ', '_').replace('/', '_')}"
                        
                        with cols[0]:
                            selected = st.checkbox(condition, key=f"family_hist_{key_base}")
                            st.session_state.form_data[key][key_base] = selected
                        
                        with cols[1]:
                            if needs_specify and selected:
                                if condition == 'Diabetes Mellitus':
                                    fbs = st.text_input("If yes, perform FBS:", key=f"family_hist_{key_base}_fbs")
                                    st.session_state.form_data[key][f"{key_base}_fbs"] = fbs
                                elif condition == 'Hypertension':
                                    bp = st.text_input("Highest BP (mmHg):", key=f"family_hist_{key_base}_bp")
                                    st.session_state.form_data[key][f"{key_base}_bp"] = bp
                                else:
                                    spec = st.text_input("Specify:", key=f"family_hist_{key_base}_specify")
                                    st.session_state.form_data[key][f"{key_base}_specify"] = spec

                with tabs[2]:
                    st.markdown("##### PERSONAL/SOCIAL HISTORY")
                    social_items = ['Smoking', 'Alcohol', 'Illicit Drugs', 'Sexually Active']
                    
                    for item in social_items:
                        cols = st.columns([2, 2, 1])
                        item_key = item.lower().replace(' ', '_')
                        
                        with cols[0]:
                            st.markdown(f"**{item}**")
                        with cols[1]:
                            status = st.radio(
                                f"{item} Status",
                                ['Yes', 'No', 'Quit'],
                                key=f"{key}_{item_key}_status",
                                horizontal=True
                            )
                            st.session_state.form_data[key][f"{item_key}_status"] = status
                        
                        if status == 'Yes':
                            if item == 'Smoking':
                                pack_years = st.text_input("No. of pack-years:", key=f"{key}_pack_years")
                                st.session_state.form_data[key]['pack_years'] = pack_years
                            elif item == 'Alcohol':
                                servings = st.text_input("No. of servings/day:", key=f"{key}_alcohol_servings")
                                st.session_state.form_data[key]['alcohol_servings'] = servings

                with tabs[3]:
                    st.markdown("##### FAMILY PLANNING")
                    counseling = st.checkbox("With access to family planning counseling", key=f"{key}_fp_counseling")
                    st.session_state.form_data[key]['fp_counseling'] = counseling
                    
                    cols = st.columns(2)
                    with cols[0]:
                        provider = st.text_input("Provider:", key=f"{key}_fp_provider")
                        st.session_state.form_data[key]['fp_provider'] = provider
                    with cols[1]:
                        method = st.text_input("Birth Control Method used:", key=f"{key}_birth_control")
                        st.session_state.form_data[key]['birth_control'] = method

                with tabs[4]:
                    st.markdown("##### MENSTRUAL HISTORY")
                    cols1 = st.columns(2)
                    with cols1[0]:
                        menarche = st.number_input("Menarche (years old):", min_value=0, max_value=100, key=f"{key}_menarche")
                        st.session_state.form_data[key]['menarche'] = menarche
                    with cols1[1]:
                        onset = st.number_input("Onset of sexual intercourse (years old):", min_value=0, max_value=100, key=f"{key}_sexual_onset")
                        st.session_state.form_data[key]['sexual_onset'] = onset

                    cols2 = st.columns(2)
                    with cols2[0]:
                        last_period = st.date_input("Last Menstrual Period:", key=f"{key}_last_period")
                        st.session_state.form_data[key]['last_period'] = last_period.strftime('%Y-%m-%d')
                    with cols2[1]:
                        duration = st.number_input("Period Duration (days):", min_value=0, max_value=30, key=f"{key}_period_duration")
                        st.session_state.form_data[key]['period_duration'] = duration

                    cols3 = st.columns(2)
                    with cols3[0]:
                        interval = st.number_input("Interval cycle (days):", min_value=0, max_value=100, key=f"{key}_interval_cycle")
                        st.session_state.form_data[key]['interval_cycle'] = interval
                    with cols3[1]:
                        menopause = st.radio("Menopause:", ["Yes", "No"], horizontal=True, key=f"{key}_menopause")
                        st.session_state.form_data[key]['menopause'] = menopause

                with tabs[5]:
                    st.markdown("##### PREGNANCY HISTORY")
                    st.text_input("G___ P___ A___ L___", key=f"{key}_pregnancy_history",
                        help="G=Gravida, P=Para, A=Abortion, L=Living children")
                    
                    cols = st.columns(2)
                    with cols[0]:
                        delivery_type = st.text_input("Type of Delivery:", key=f"{key}_delivery_type")
                        st.session_state.form_data[key]['delivery_type'] = delivery_type
                    with cols[1]:
                        induced_htn = st.radio("Pregnancy Induced Hypertension:", ["Yes", "No"], 
                            horizontal=True, key=f"{key}_induced_htn")
                        st.session_state.form_data[key]['induced_htn'] = induced_htn

                with tabs[6]:
                    st.markdown("##### PERTINENT PHYSICAL EXAMINATION FINDINGS")
                    
                    # Vital Signs
                    st.markdown("**Vital Signs**")
                    cols1 = st.columns(4)
                    with cols1[0]:
                        height = st.number_input("Height (cm):", min_value=0.0, key=f"{key}_height")
                        st.session_state.form_data[key]['height'] = height
                    with cols1[1]:
                        weight = st.number_input("Weight (kg):", min_value=0.0, key=f"{key}_weight")
                        st.session_state.form_data[key]['weight'] = weight
                    with cols1[2]:
                        bp = st.text_input("BP (mmHg):", key=f"{key}_bp")
                        st.session_state.form_data[key]['bp'] = bp
                    with cols1[3]:
                        temp = st.number_input("Temp (°C):", min_value=35.0, max_value=42.0, key=f"{key}_temp")
                        st.session_state.form_data[key]['temp'] = temp

                    cols2 = st.columns(2)
                    with cols2[0]:
                        rr = st.number_input("RR (cpm):", min_value=0, key=f"{key}_rr")
                        st.session_state.form_data[key]['rr'] = rr
                    with cols2[1]:
                        st.markdown("**Blood Type**")
                        blood_options = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
                        blood_type = st.selectbox("", blood_options, key=f"{key}_blood_type")
                        st.session_state.form_data[key]['blood_type'] = blood_type

                    # Visual Acuity
                    st.markdown("**Visual Acuity**")
                    cols3 = st.columns(2)
                    with cols3[0]:
                        right_eye = st.text_input("Right Eye:", key=f"{key}_right_eye")
                        st.session_state.form_data[key]['right_eye'] = right_eye
                    with cols3[1]:
                        left_eye = st.text_input("Left Eye:", key=f"{key}_left_eye")
                        st.session_state.form_data[key]['left_eye'] = left_eye

                with tabs[7]:
                    st.markdown("##### PEDIA CLIENT AGED 0-24 MOS")
                    measurements = [
                        "Body Length", "Head Circumference", "Chest Circumference",
                        "Abdominal Circumference", "Hip Circumference",
                        "Mid-Upper Arm Circumference", "Limbs Circumference"
                    ]
                    
                    for measurement in measurements:
                        cols = st.columns([3, 1])
                        field_key = measurement.lower().replace(' ', '_').replace('-', '_')
                        
                        with cols[0]:
                            value = st.number_input(f"{measurement} (cm):", 
                                min_value=0.0, key=f"{key}_{field_key}")
                            st.session_state.form_data[key][field_key] = value
                    
                    for condition, needs_specify in conditions.items():
                        cols = st.columns([1, 3])
                        condition_key = condition.lower().replace(' ', '_').replace('/', '_')
                        
                        with cols[0]:
                            selected = st.checkbox(condition, key=f"{key}_{condition_key}")
                            st.session_state.form_data[key][condition_key] = selected
                        
                        with cols[1]:
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

                with tabs[3]:
                    render_immunization_section(key)

            st.caption(f"Section Progress: {current_progress}%")

    if st.button("Submit Assessment", type="primary"):
        overall_progress = sum(calculate_section_progress(st.session_state.form_data[key]) 
                             for key in st.session_state.form_data.keys()) / len(st.session_state.form_data)
        if overall_progress < 80:
            st.error(f"Please complete at least 80% of the form. Current progress: {overall_progress:.1f}%")
        else:
            st.success(f"Assessment submitted successfully! Overall completion: {overall_progress:.1f}%")

if __name__ == "__main__":
    main()
