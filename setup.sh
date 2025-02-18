#!/bin/bash
# Create project directory and virtual environment
mkdir deepseek-r1
cd deepseek-r1
python -m venv venv
source venv/bin/activate

# Install required packages
pip install requests python-dotenv streamlit 