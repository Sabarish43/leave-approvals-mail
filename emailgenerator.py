import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# ========== SETUP GEMINI ==========
GENAI_API_KEY = "AIzaSyC3Cbb1kPNDDgI_OW1XKRnEA6vZUis1Xoo"  
genai.configure(api_key=GENAI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-2.0-flash")
# ========== FUNCTIONS ==========

def generate_email(prompt, format_type, tone):
    full_prompt = (
        f"Write an email with the following characteristics:\n"
        f"Format: {format_type}\nTone: {tone}\n\n"
        f"Content: {prompt}"
    )
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(full_prompt)
    return response.text.strip()

def create_pdf(content, filename="generated_email.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename

# ========== STREAMLIT APP ==========

st.set_page_config(page_title="AI Email Generator", layout="centered")
st.title("📧 AI Email Generator using Gemini")

st.markdown("Enter the content of the email you want to generate:")

# User Input
user_text = st.text_area("Email Content Input", height=200, placeholder="Describe what your email should include...")

# Format and Tone Selection
col1, col2 = st.columns(2)

with col1:
    format_type = st.selectbox("Email Format", ["Formal", "Informal", "Business", "Casual", "Apology", "Follow-up"])

with col2:
    tone = st.selectbox("Email Tone", ["Professional", "Friendly", "Polite", "Persuasive", "Empathetic", "Direct"])

# Buttons
generate_clicked = st.button("Generate Email")
regenerate_clicked = st.button("Regenerate Email")

# Session State to Store Output
if "email_output" not in st.session_state:
    st.session_state.email_output = ""

if (generate_clicked or regenerate_clicked) and user_text:
    with st.spinner("Generating email..."):
        st.session_state.email_output = generate_email(user_text, format_type, tone)

# Display Output
if st.session_state.email_output:
    st.subheader("✉️ Generated Email")
    st.text_area("Generated Email", value=st.session_state.email_output, height=300)

    # Download PDF
    if st.button("Download as PDF"):
        filename = create_pdf(st.session_state.email_output)
        with open(filename, "rb") as file:
            st.download_button("Click to Download PDF", data=file, file_name="generated_email.pdf", mime="application/pdf")

# Instructions
st.markdown("---")
st.markdown("✅ Enter your email idea, select the format & tone, then generate. Click **Regenerate** to refresh the style.")
