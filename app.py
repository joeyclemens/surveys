# app.py
import streamlit as st
import pandas as pd

# Main Streamlit application
def main():
    # Configure page layout
    st.set_page_config(layout="wide")
    # Display the image at the top left
    image_path = "MJMEDICAL.png"
    st.image(image_path, use_column_width=False, width=300)
    
    st.title("Survey Analysis")

    # Select between survey options
    survey_option = st.selectbox("Select a survey option", ["Select Option", "Staff survey", "Patient survey"])

    if survey_option == "Select Option":
        st.info("Please select a survey option from the dropdown.")
    elif survey_option == "Staff survey":
        # Load Staff survey data
        staff_data = pd.read_csv("survey/staff.csv")
        
        # Display options to select numerical columns
        select_all = st.checkbox("Select All", key="staff_select_all")
        if select_all:
            selected_columns = staff_data.select_dtypes(include=['int', 'float']).columns
        else:
            selected_columns = st.multiselect("Please select at least one header", staff_data.select_dtypes(include=['int', 'float']).columns)

        if not any(selected_columns):
            st.warning("Please select at least one header.")
            return

        # Calculate average for selected columns
        averages = staff_data[selected_columns].mean()

        # Plot the averages with a custom color scheme
        st.bar_chart(averages, color='#1f77b4', height=500)  # blue color
        # Add horizontal line
        st.markdown("---")
        # Questions related analysis
        # st.header("Questions Analysis for Staff Survey")

        # List of questions for Staff survey
        staff_questions = [
            "How would you rate the internal temperature?",
            "How would you rate the internal lighting? ",
            "How would you rate the internal acoustic privacy?"
        ]

        # Display average number of times each answer is selected for each question with a custom color scheme
        for i, question in enumerate(staff_questions):
            st.subheader(f"{question}")
            answers_count = staff_data[question].value_counts().sort_index()
            st.bar_chart(answers_count, color='#d62728')  # red color

        # Add download button for Staff data
        st.download_button(
            label="Download Staff Data as CSV",
            data=staff_data.to_csv(index=False).encode(),
            file_name="staff_survey_data.csv",
            key="staff_download_button",
            help="Click to download the Staff survey data"
        )

    elif survey_option == "Patient survey":
        # Load Patient survey data
        patient_data = pd.read_csv("survey/patient.csv")

        # Display options to select numerical columns (including "Select All" and "Select All (except 'How old are you?')")
        all_numerical_columns = patient_data.select_dtypes(include=['int', 'float']).columns
        exclude_column = "How old are you?"
        numerical_columns_except_age = [col for col in all_numerical_columns if col != exclude_column]

        select_all = st.checkbox("Select All", key="patient_select_all")
        select_all_except_age = st.checkbox("Select All (except 'How old are you?')", key="patient_select_all_except_age")
        
        if select_all:
            selected_columns = all_numerical_columns
        elif select_all_except_age:
            selected_columns = numerical_columns_except_age
        else:
            selected_columns = st.multiselect("Please select at least one header", all_numerical_columns)

        if not any(selected_columns):
            st.warning("Please select at least one header.")
            return

        # Calculate average for selected columns
        averages = patient_data[selected_columns].mean()

        # Plot the averages with a custom color scheme
        st.bar_chart(averages, color='#ff7f0e')  # orange color
        # Add horizontal line
        st.markdown("---")
        # Questions related analysis
        # st.header("Questions Analysis for Patient Survey")

        # List of questions for Patient survey
        patient_questions = [
            "How would you rate the rate the internal temperature?",
            "How would you rate the internal lighting?",
            "How would you rate the internal sound-proofing?"
        ]

        # Display average number of times each answer is selected for each question with a custom color scheme
        for i, question in enumerate(patient_questions):
            st.subheader(f"{question}")
            answers_count = patient_data[question].value_counts().sort_index()
            st.bar_chart(answers_count, color='#2ca02c')  # green color

        # Add download button for Patient data
        st.download_button(
            label="Download Patient Data as CSV",
            data=patient_data.to_csv(index=False).encode(),
            file_name="patient_survey_data.csv",
            key="patient_download_button",
            help="Click to download the Patient survey data"
        )




# Run the app
if __name__ == "__main__":
    main()
