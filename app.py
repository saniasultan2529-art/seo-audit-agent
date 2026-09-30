import re
import requests
import streamlit as st
from bs4 import BeautifulSoup
from groq import Groq

# ------------------------------------------------------------------------------
# 1. Page Configuration & UI Setup
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Medical Local SEO & Schema Agent",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 AI Local SEO & Medical Schema Audit Agent")
st.write(
    "Automated audit tool built specifically for Clinics, Dentists, and Healthcare Practices. "
    "Scrapes local business signals and generates valid JSON-LD `MedicalClinic` / `Dentist` Schema."
)

# Sidebar setup for user configuration
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
st.sidebar.markdown("[Get a free Groq API key](https://console.groq.com)")

st.sidebar.markdown("---")
st.sidebar.subheader("About This Agent")
st.sidebar.info(
    "This agent analyzes local ranking signals (Google Maps embeds, phone availability, "
    "JSON-LD markup) and uses Llama 3.3 to auto-generate valid Schema.org structured data."
)

# ------------------------------------------------------------------------------
# 2. Medical Web Scraper Function
# ------------------------------------------------------------------------------
def scrape_medical_site(url):
    """
    Fetches web content and extracts specific local healthcare SEO signals.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()

        # Extract primary HTML tags
        title = soup.title.string.strip() if soup.title and soup.title.string else "Missing Title Tag"
        h1 = soup.find('h1').text.strip() if soup.find('h1') else "Missing H1 Tag"
        
        # Regex search for telephone patterns
        phone_matches = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text_content)
        phone = phone_matches[0] if phone_matches else "No Phone Number Detected"

        # Check for Google Maps embeds or map links
        has_maps = ("google.com/maps" in response.text) or ("maps.google.com" in response.text)
        
        # Check for pre-existing JSON-LD Schema
        existing_schema = soup.find_all('script', type='application/ld+json')
        has_schema = len(existing_schema) > 0
        
        return {
            "title": title,
            "h1": h1,
            "phone": phone,
            "has_maps": has_maps,
            "has_schema": has_schema,
            "raw_text_snippet": text_content[:1500].replace('\n', ' ')
        }
    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------------------
# 3. Groq AI Schema Generator Function
# ------------------------------------------------------------------------------
def generate_medical_schema(data, user_key):
    """
    Sends scraped local SEO signals to Groq Llama 3 to generate an audit & Schema markup.
    """
    client = Groq(api_key=user_key)
    
    prompt = f"""
    You are an expert Local SEO Specialist for Healthcare Practices and Clinics.
    
    Analyze the following scraped website data:
    - Target Webpage Title: {data['title']}
    - Primary Heading (H1): {data['h1']}
    - Detected Phone Number: {data['phone']}
    - Embedded Google Maps Found: {data['has_maps']}
    - Existing JSON-LD Schema Found: {data['has_schema']}
    - Website Content Snippet: {data['raw_text_snippet']}

    Deliverables required:
    1. **Executive Local SEO Diagnosis (3 Bullet Points)**:
       - Highlight missing or improperly configured local signals (e.g., telephone formatting, missing address, map integration, or structured data).
    2. **Valid JSON-LD Schema Code Block**:
       - Generate a clean, error-free `@context`: "https://schema.org" block.
       - Use `@type`: `MedicalClinic` or `Dentist`.
       - Include structured fields with placeholders for: `name`, `image`, `telephone`, `address` (PostalAddress), `geo` (GeoCoordinates), `openingHoursSpecification`, `medicalSpecialty`, and `priceRange`.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ------------------------------------------------------------------------------
# 4. User Interface Execution Flow
# ------------------------------------------------------------------------------
target_url = st.text_input("Enter Healthcare / Clinic Website URL:", "https://example.com")

if st.button("Run Medical Audit", type="primary"):
    if not api_key:
        st.error("Please enter your free Groq API Key in the sidebar to run the audit.")
    elif not target_url or not target_url.startswith(("http://", "https://)):
        st.warning("Please enter a valid website URL starting with http:// or https://")
    else:
        with st.spinner("Analyzing site structure and extracting local signals..."):
            site_data = scrape_medical_site(target_url)
            
            if "error" in site_data:
                st.error(f"Error accessing webpage: {site_data['error']}")
            else:
                # Section 1: Dashboard Metrics
                st.subheader("1. Local Signal Metrics")
                col1, col2, col3 = st.columns(3)
                
                col1.metric("Phone Number Detected", site_data['phone'])
                col2.metric("Google Maps Integration", "Yes" if site_data['has_maps'] else "No")
                col3.metric("Existing JSON-LD Schema", "Yes" if site_data['has_schema'] else "No")
                
                st.markdown("---")
                
                # Section 2: AI Audit & Schema Output
                st.subheader("2. Medical Schema Audit & JSON-LD Output")
                ai_analysis = generate_medical_schema(site_data, api_key)
                st.markdown(ai_analysis)
                
                # Section 3: Direct Download
                st.download_button(
                    label="📥 Download JSON-LD & Audit Report",
                    data=ai_analysis,
                    file_name="medical_seo_audit.md",
                    mime="text/markdown"
                )
