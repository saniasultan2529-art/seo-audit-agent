# 🩺 Autonomous Medical Local SEO & Schema Audit Agent

An AI-powered technical SEO auditor and JSON-LD Schema generator built specifically for healthcare practices, medical clinics, and dental offices.

## 🚀 Live Demo
[Access Live Streamlit Web Application](https://seo-audit-agent-24b4jzmhjwt2s4gemhbjzz.streamlit.app)

## 🛠 Tech Stack & Architecture
- **Language:** Python 3.10+
- **Frontend Framework:** Streamlit
- **Scraper / Parser:** BeautifulSoup4, Requests, Regex
- **LLM Orchestration:** Groq API (`openai/gpt-oss-20b`)
- **Deployment:** Streamlit Community Cloud

## 📋 Features
- **Local Signal Detection:** Scrapes phone formats, embedded Google Maps, and existing structured data tags.
- **Automated JSON-LD Generation:** Outputs Schema.org compliant `@type: MedicalClinic` and `@type: Dentist` JSON-LD blocks.
- **Instant Diagnostics:** Generates a 3-bullet executive local SEO report.

## ⚙️ Installation & Local Setup
```bash
git clone https://github.com/saniasultan2529-art/seo-audit-agent.git
cd seo-audit-agent
pip install -r requirements.txt
streamlit run app.py
"""
## 📐 Design & Engineering Decisions

### Scraper Architecture: BeautifulSoup4 vs. Selenium
- **Lightweight Overhead:** `BeautifulSoup4` parses static HTML content in milliseconds without requiring heavy browser binaries or ChromeDriver dependencies.
- **Resource Limits:** Streamlit Cloud has limited RAM resources. Avoiding dynamic browser automation prevents container out-of-memory errors and keeps deployment lightweight.

### Defensive Error Handling & Input Validation
- **URL Sanitization:** Validates URL prefixes (`http://` / `https://`) before sending HTTP requests to avoid malformed target exceptions.
- **Resilient Request Headers:** Enforces standard browser `User-Agent` strings and request timeouts (12s) to reduce blocks by security firewalls.
- **Schema Validation:** Programmatically checks for pre-existing `application/ld+json` script tags before passing site context to the Groq API.
-
