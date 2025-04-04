import streamlit as st
import numpy as np
import pandas as pd
from utils import validate_marks, convert_marks, calculate_percentage
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generate_pdf(results, total_marks, total_max, percentage):
    """Generate PDF report of marks."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Convert results to table data
    data = [['Subject', 'Marks', 'Maximum Marks', 'Percentage']]
    for subject, marks, max_marks in results:
        subject_percentage = calculate_percentage(marks, max_marks)
        if subject in ["Hindi", "Computer"] and st.session_state.get('converted_marks', {}).get(subject.lower()):
            original = st.session_state.converted_marks[subject.lower()]['original']
            data.append([subject, f"{original} → {marks:.2f}", str(max_marks), f"{subject_percentage:.2f}%"])
        else:
            data.append([subject, str(marks), str(max_marks), f"{subject_percentage:.2f}%"])

    # Add total and percentage
    data.append(['Total', f"{total_marks:.2f}", f"{total_max:.2f}", f"{percentage:.2f}%"])

    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)
    return buffer

def conversion_page():
    st.title("Marks Conversion")

    # Initialize conversion state
    if 'converted_marks' not in st.session_state:
        st.session_state.converted_marks = {}

    with st.form("conversion_form"):
        # Hindi marks conversion
        st.subheader("Convert Hindi Marks")
        hindi_marks = st.number_input(" ", min_value=0.0, key="conv_hindi_marks", value=None, placeholder="Enter marks")
        hindi_max = st.number_input(" ", min_value=1.0, key="conv_hindi_max", value=None, placeholder="Enter maximum marks")
        hindi_new_max = st.number_input(" ", min_value=1.0, key="conv_hindi_new_max", value=None, placeholder="Enter new maximum marks")

        # Computer marks conversion
        st.subheader("Convert Computer Marks")
        comp_marks = st.number_input(" ", min_value=0.0, key="conv_comp_marks", value=None, placeholder="Enter marks")
        comp_max = st.number_input(" ", min_value=1.0, key="conv_comp_max", value=None, placeholder="Enter maximum marks")
        comp_new_max = st.number_input(" ", min_value=1.0, key="conv_comp_new_max", value=None, placeholder="Enter new maximum marks")

        submit = st.form_submit_button("Convert Marks")

        if submit:
            if validate_marks(comp_marks, comp_max) and validate_marks(hindi_marks, hindi_max):
                st.session_state.converted_marks = {
                    "computer": {
                        "original": comp_marks,
                        "converted": convert_marks(comp_marks, comp_max, comp_new_max),
                        "max": comp_new_max
                    },
                    "hindi": {
                        "original": hindi_marks,
                        "converted": convert_marks(hindi_marks, hindi_max, hindi_new_max),
                        "max": hindi_new_max
                    }
                }
                st.success("Marks converted successfully!")
            else:
                st.error("Please enter valid marks (between 0 and maximum marks)")

    # Reset button for conversion page
    if st.button("Reset Conversion Form"):
        if 'converted_marks' in st.session_state:
            del st.session_state.converted_marks
        st.rerun()

    if st.button("Return to Marks Calculator"):
        st.session_state.show_conversion = False
        st.rerun()

def main():
    # Initialize session states
    if 'show_conversion' not in st.session_state:
        st.session_state.show_conversion = False

    # Show conversion page if conversion mode is active
    if st.session_state.show_conversion:
        conversion_page()
        return

    st.title("Marks Calculator")

    # Custom CSS for convert marks button
    st.markdown("""
        <style>
        .convert-button {
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            margin-bottom: 20px;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)

    # Convert Marks button
    if st.button("Convert Marks", key="convert_button", use_container_width=False):
        st.session_state.show_conversion = True
        st.rerun()

    with st.form("marks_form"):
        # Get converted marks if available
        converted_hindi = st.session_state.get('converted_marks', {}).get('hindi', {})
        converted_comp = st.session_state.get('converted_marks', {}).get('computer', {})

        # Subjects in specified order
        st.subheader("Maths")
        math_marks = st.number_input(" ", min_value=0.0, key="math_marks", value=None, placeholder="Enter marks")

        st.subheader("English")
        eng_marks = st.number_input(" ", min_value=0.0, key="eng_marks", value=None, placeholder="Enter marks")

        st.subheader("Science")
        sci_marks = st.number_input(" ", min_value=0.0, key="sci_marks", value=None, placeholder="Enter marks")

        st.subheader("Social")
        social_marks = st.number_input(" ", min_value=0.0, key="social_marks", value=None, placeholder="Enter marks")

        st.subheader("Kannada")
        kan_marks = st.number_input(" ", min_value=0.0, key="kan_marks", value=None, placeholder="Enter marks")

        st.subheader("Hindi")
        hindi_marks = st.number_input(
            " ",
            min_value=0.0,
            value=converted_hindi.get('converted', None),
            key="hindi_marks",
            placeholder="Enter marks"
        )

        st.subheader("Computer")
        comp_marks = st.number_input(
            " ",
            min_value=0.0,
            value=converted_comp.get('converted', None),
            key="comp_marks",
            placeholder="Enter marks"
        )

        st.subheader("Maximum Marks")
        max_marks = st.number_input(" ", min_value=1.0, value=None, key="max_marks", placeholder="Enter maximum marks")

        submit = st.form_submit_button("Calculate Results")

        if submit:
            # Get the appropriate maximum marks for converted subjects
            hindi_max = converted_hindi.get('max', max_marks) if converted_hindi else max_marks
            comp_max = converted_comp.get('max', max_marks) if converted_comp else max_marks

            # Calculate total marks and validate
            subjects_data = [
                ("Maths", math_marks, max_marks),
                ("English", eng_marks, max_marks),
                ("Science", sci_marks, max_marks),
                ("Social", social_marks, max_marks),
                ("Kannada", kan_marks, max_marks),
                ("Hindi", hindi_marks, hindi_max),
                ("Computer", comp_marks, comp_max)
            ]

            valid_data = True
            total_marks = 0
            total_max = 0

            # Process marks
            results = []
            for subject, marks, subject_max in subjects_data:
                if not validate_marks(marks, subject_max):
                    st.error(f"Invalid marks for {subject}")
                    valid_data = False
                    break

                results.append((subject, marks, subject_max))
                total_marks += marks
                total_max += subject_max

            if valid_data:
                st.success("Marks calculated successfully!")

                # Create DataFrame for table display
                table_data = []
                for subject, marks, subject_max in results:
                    subject_percentage = calculate_percentage(marks, subject_max)
                    if subject in ["Hindi", "Computer"] and st.session_state.get('converted_marks', {}).get(subject.lower()):
                        original = st.session_state.converted_marks[subject.lower()]['original']
                        table_data.append({
                            "Subject": subject,
                            "Marks": f"{original} → {marks:.2f}",
                            "Maximum Marks": subject_max,
                            "Percentage": f"{subject_percentage:.2f}%"
                        })
                    else:
                        table_data.append({
                            "Subject": subject,
                            "Marks": marks,
                            "Maximum Marks": subject_max,
                            "Percentage": f"{subject_percentage:.2f}%"
                        })

                # Calculate total percentage
                percentage = calculate_percentage(total_marks, total_max)

                # Add total row
                table_data.append({
                    "Subject": "Total",
                    "Marks": f"{total_marks:.2f}",
                    "Maximum Marks": f"{total_max:.2f}",
                    "Percentage": f"{percentage:.2f}%"
                })

                # Display results in table format
                st.subheader("Results")
                df = pd.DataFrame(table_data)
                st.table(df)

                # Store PDF buffer in session state
                pdf_buffer = generate_pdf(results, total_marks, total_max, percentage)
                st.session_state.pdf_buffer = pdf_buffer

    # Generate PDF button outside form
    if 'pdf_buffer' in st.session_state:
        st.download_button(
            label="Download Results as PDF",
            data=st.session_state.pdf_buffer.getvalue(),
            file_name="marks_report.pdf",
            mime="application/pdf"
        )

    # Reset button
    if st.button("Reset Form"):
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()