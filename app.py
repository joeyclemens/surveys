# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Main Streamlit application
def main():
    # Configure page layout
    st.set_page_config(layout="wide")

    st.title("Survey Analysis App")

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
            selected_columns = st.multiselect("Select numerical columns", staff_data.select_dtypes(include=['int', 'float']).columns)

        if not any(selected_columns):
            st.warning("Please select at least one numerical column.")
            return

        # Calculate average for selected columns
        averages = staff_data[selected_columns].mean()

        # Plot the averages
        st.bar_chart(averages)

        # Questions related analysis
        st.header("Questions Analysis for Staff Survey")

        # List of questions for Staff survey
        staff_questions = [
            "How would you rate the internal temperature?",
            "How would you rate the internal lighting? ",
            "How would you rate the internal acoustic privacy?"
        ]

        # Display average number of times each answer is selected for each question
        for question in staff_questions:
            st.subheader(f"Average Ratings for: {question}")
            answers_count = staff_data[question].value_counts().sort_index()
            st.bar_chart(answers_count)

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
            selected_columns = st.multiselect("Select numerical columns", numerical_columns_except_age)

        if not any(selected_columns):
            st.warning("Please select at least one numerical column.")
            return

        # Calculate average for selected columns
        averages = patient_data[selected_columns].mean()

        # Plot the averages
        st.bar_chart(averages)

        # Questions related analysis
        st.header("Questions Analysis for Patient Survey")

        # List of questions for Patient survey
        patient_questions = [
            "How would you rate the rate the internal temperature?",
            "How would you rate the internal lighting?",
            "How would you rate the internal sound-proofing?"
        ]

        # Display average number of times each answer is selected for each question
        for question in patient_questions:
            st.subheader(f"Average Ratings for: {question}")
            answers_count = patient_data[question].value_counts().sort_index()
            st.bar_chart(answers_count)

# Run the app
if __name__ == "__main__":
    main()
