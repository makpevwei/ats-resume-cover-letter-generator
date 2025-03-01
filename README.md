# AI Resume and Cover Letter Generator App

A simple Streamlit app for generating ATS-friendly resumes and cover letters template using Google's Gemini API and which can be downloaded and modified in your word document.

## Overview

This project provides a template for creating professional, ATS-optimized resumes and cover letters. The app uses Google's Gemini API (via `google.generativeai`) to generate text content based on user inputs. It is designed with simplicity in mind so that beginners can easily understand and customize the code.

## Features

- **Resume/Cover Letter Generation:** Create tailored documents by providing job title, company name, and job description.
- **AI-Powered Content:** Uses the Gemini API to generate professional text.
- **Downloadable Output:** Generated documents can be downloaded as a Word (.docx) file.
- **Easy Customization:** Modify model settings, system instructions, and prompt templates as needed.

## Prerequisites

- Python 3.7 or later
- [Streamlit](https://streamlit.io/)
- [google-generativeai](https://pypi.org/project/google-generativeai/)
- [python-docx](https://python-docx.readthedocs.io/en/latest/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd gemini-resume-app
