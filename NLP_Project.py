import streamlit as st
import streamlit.components.v1 as components
import joblib
import re
import pandas as pd
import numpy as np
from Spam_classifier_project import run_spam_app
from Food_Sentiment_project import run_sentiment_app

# ✅ Page config (sirf yahi file me hona chahiye)
st.set_page_config(layout="wide")

if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

if "active_page" not in st.session_state:
    st.session_state.active_page = None

# ✅ Default page
if "page" not in st.session_state:
    st.session_state.page = "home"

def NLP_sidebar():

    st.sidebar.markdown("""
    <style>
    .sidebar-banner {
        padding: 12px 15px;
        border-radius: 12px;
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        transition: all 0.4s ease;
        cursor: pointer;
        margin-bottom: 20px;
    }

    .sidebar-banner:hover {
        color: black;
        transform: scale(1.05);
    }
    </style>

    <div class="sidebar-banner">
        🤖 NLP Control Panel
    </div>
    """, unsafe_allow_html=True)
    

        # Image
    st.sidebar.image("NLP_2.jpg")

    # Welcome
    st.sidebar.markdown(
    "<h2 style='color:#00FFFF;'>👋 Welcome</h2>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown(
    "<p style='color:#FFD700;'>Explore AI-powered NLP applications 💬🧠</p>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown("---")


    # About App
    st.sidebar.markdown(
    "<h3 style='color:#FF4B4B;'>🤖 About Project</h3>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown(
    "<p style='color:#E0E0E0;'>This app combines <b style='color:#00FFFF;'>Spam Detection</b> 📩 and <b style='color:#FFD700;'>Sentiment Analysis</b> 😊 using Machine Learning & NLP.</p>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown("---")


    # Features
    st.sidebar.markdown(
    "<h3 style='color:#00FFAA;'>🚀 Features</h3>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown(
    """
    ✔ <span style='color:#FF6B6B;'>Spam Detection (Email/SMS)</span><br>
    ✔ <span style='color:#4D96FF;'>Food Sentiment Analysis</span><br>
    ✔ <span style='color:#FFD93D;'>AI-powered Text Processing</span><br>
    ✔ <span style='color:#6BCB77;'>Real-time Predictions</span><br>
    ✔ <span style='color:#A66CFF;'>Multi-Model NLP System</span>
    """,
    unsafe_allow_html=True
    )
    st.sidebar.markdown("---")


    # Modules
    st.sidebar.markdown(
    "<h3 style='color:#FFA500;'>📊 NLP Modules</h3>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown(
    """
    📩 <span style='color:red;'>Spam Classifier</span><br>
    😊 <span style='color:lightgreen;'>Sentiment Analyzer</span><br>
    📢 <span style='color:orange;'>Text Classification</span><br>
    🔍 <span style='color:#00FFFF;'>Language Processing</span>
    """,
    unsafe_allow_html=True
    )
    st.sidebar.markdown("---")


    # How to Use
    st.sidebar.markdown(
    "<h3 style='color:#00BFFF;'>📱 How to Use?</h3>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown(
    """
    1️⃣ Select Module (Spam / Sentiment)<br>
    2️⃣ Enter Text / Review<br>
    3️⃣ Click <b style='color:#FFD700;'>Analyze</b><br>
    4️⃣ View AI Prediction Results
    """,
    unsafe_allow_html=True
    )
    st.sidebar.markdown("---")


    # Fun Fact
    st.sidebar.markdown(
    "<h3 style='color:#FF69B4;'>💡 NLP Insights</h3>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown(
    """
    🔍 <span style='color:#FFD700;'>Over 80% digital text is unstructured!</span><br>
    🧠 <span style='color:#00FFAA;'>NLP helps machines understand human language</span>
    """,
    unsafe_allow_html=True
    )
    st.sidebar.markdown("---")


    # Developer
    st.sidebar.markdown(
    "<h3 style='color:#9D4EDD;'>🧑‍💻 Developer</h3>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown(
    "<p style='color:white;'>Made by: <b style='color:#00FFFF;'>Dev Varshney</b><br>AI/ML & NLP Enthusiast 🚀</p>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown("---")


    # Contact
    st.sidebar.markdown(
    "<h3 style='color:#FF4B4B;'>📞 Contact</h3>",
    unsafe_allow_html=True
    )
    st.sidebar.markdown(
    """
    📱 <span style='color:#FFD700;'>9058068999</span><br>
    📧 <a href='mailto:varshneyd110@gmail.com' style='color:#00FFFF;'>Email Me</a>
    """,
    unsafe_allow_html=True
    )
    st.sidebar.markdown("---")

    st.sidebar.image("flag.jpg")

def main_spam_sidebar():
        st.sidebar.markdown("""
        <style>
        .sidebar-banner {
            padding: 12px 15px;
            border-radius: 12px;
            background: linear-gradient(135deg, #28a745, #5cd65c);
            color: white;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            transition: all 0.4s ease;
            cursor: pointer;
            margin-bottom: 20px;
        }

        .sidebar-banner:hover {
            background: linear-gradient(135deg, #28a745, #5cd65c);
            color: black;
            transform: scale(1.05);
        }
        </style>

        <div class="sidebar-banner">
            🌿 Control Panel
        </div>
        """, unsafe_allow_html=True)


        st.sidebar.image("spam.png")

        # ✅ Logout sabse upar
        if st.sidebar.button("Logout",use_container_width=True):
            st.session_state.clear()
            st.rerun()

        st.sidebar.markdown(
        "<h2 style='color:#00FFFF;'>🤖 About Project</h2>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:#E0E0E0;'>AI-powered system to detect <b style='color:red;'>Spam</b> vs <b style='color:green;'>Safe</b> messages 📧</p>"
        "<p style='color:#FFD700;'>⚡ Real-time classification using Machine Learning</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#FF4B4B;'>🐍 Libraries Used</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        ✔ <span style='color:#FFD93D;'>Scikit-learn</span><br>
        ✔ <span style='color:#4D96FF;'>Pandas</span><br>
        ✔ <span style='color:#6BCB77;'>NumPy</span><br>
        ✔ <span style='color:#FF6B6B;'>Joblib</span><br>
        ✔ <span style='color:#00FFFF;'>Streamlit</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#00FFAA;'>☁️ Cloud & Deployment</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:#E0E0E0;'>🚀 Hosted on <b style='color:#FFD700;'>Streamlit Cloud</b></p>"
        "<p style='color:#6BCB77;'>🌍 Accessible anytime, anywhere</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#FFA500;'>📊 Model Insights</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        🤖 <span style='color:#FFD700;'>Model:</span> Naive Bayes / Logistic Regression<br>
        📈 <span style='color:#00FFAA;'>High Accuracy Spam Detection</span><br>
        ⚡ <span style='color:#4D96FF;'>Fast Prediction Speed</span><br>
        🔍 <span style='color:#FF6B6B;'>Text Vectorization (TF-IDF)</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#FF69B4;'>💡 Smart Facts</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        📌 <span style='color:#FFD700;'>80%+ emails are spam globally</span><br>
        🛡️ <span style='color:#00FFAA;'>AI filters protect users from phishing</span><br>
        ⚠️ <span style='color:#FF4B4B;'>Spam often contains suspicious links</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#9D4EDD;'>👥 About Us</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:white;'>Enter any message and let AI decide if it's <span style='color:red;'>Spam</span> or <span style='color:green;'>Safe</span>.</p>"
        "<p style='color:#00FFFF;'>Built for real-time intelligent filtering 🚀</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#FF4B4B;'>📞 Contact Us</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        📱 <span style='color:#FFD700;'>98765XXXXX</span><br>
        📧 <span style='color:#00FFFF;'>Email Support Available</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.image("flag.jpg")

def login_spam_sidebar():
        st.sidebar.markdown("""
        <style>
        .sidebar-banner {
            padding: 12px 15px;
            border-radius: 12px;
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            color: white;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            transition: all 0.4s ease;
            cursor: pointer;
            margin-bottom: 20px;
        }

        .sidebar-banner:hover {
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            color: black;
            transform: scale(1.05);
        }
        </style>

        <div class="sidebar-banner">
            🌿 Control Panel
        </div>
        """, unsafe_allow_html=True)


        st.sidebar.image("spam_3.png")

        st.sidebar.markdown(
        "<h2 style='color:#00FFFF;'>👋 Welcome</h2>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:#FFD700;'>Explore AI-powered Spam Detection insights 📧</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#FF4B4B;'>🤖 About App</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:#E0E0E0;'>Detects <b style='color:red;'>Spam</b> vs <b style='color:green;'>Valid</b> messages using Machine Learning & NLP.</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#00FFAA;'>🚀 Features</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        ✔ <span style='color:#FF6B6B;'>Spam Detection (Email/SMS)</span><br>
        ✔ <span style='color:#4D96FF;'>Bulk Message Analysis</span><br>
        ✔ <span style='color:#FFD93D;'>AI-powered Filtering</span><br>
        ✔ <span style='color:#6BCB77;'>Real-time Predictions</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#FFA500;'>📊 Categories</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        🚫 <span style='color:red;'>Spam Messages</span><br>
        ✅ <span style='color:lightgreen;'>Valid Messages</span><br>
        📢 <span style='color:orange;'>Promotional Content</span><br>
        ⚠️ <span style='color:yellow;'>Phishing Alerts</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#00BFFF;'>📱 How to Use?</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        1️⃣ Enter Message / Upload File<br>
        2️⃣ Click <b style='color:#FFD700;'>Analyze</b><br>
        3️⃣ Get <span style='color:red;'>Spam</span> or <span style='color:green;'>Valid</span> Result
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#FF69B4;'>💡 Did You Know?</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        🔍 <span style='color:#FFD700;'>80-85% emails are spam!</span><br>
        🔐 <span style='color:#00FFAA;'>ML + NLP protect users</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#9D4EDD;'>🧑‍💻 Developer</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:white;'>Made by: <b style='color:#00FFFF;'>Dev Varshney</b><br>AI/ML Enthusiast 🚀</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.markdown(
        "<h3 style='color:#FF4B4B;'>📞 Contact</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        📱 <span style='color:#FFD700;'>9058068999</span><br>
        📧 <a href='mailto:varshneyd110@gmail.com' style='color:#00FFFF;'>Email Me</a>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        st.sidebar.image("flag.jpg")

def main_sentiment_sidebar():
        st.sidebar.markdown("""
        <style>
        .sidebar-banner {
            padding: 12px 15px;
            border-radius: 12px;
            background: linear-gradient(135deg, #28a745, #5cd65c);
            color: white;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            transition: all 0.4s ease;
            cursor: pointer;
            margin-bottom: 20px;
        }

        .sidebar-banner:hover {
            color: black;
            transform: scale(1.05);
        }
        </style>

        <div class="sidebar-banner">
            🌿 Control Panel
        </div>
        """, unsafe_allow_html=True)


        # 🌄 Image
        st.sidebar.image("restaurant.jpg")


        # ✅ Logout (top pe hi best hai)
        if st.sidebar.button("Logout", key="sent_logout_btn",use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.active_page = None
            st.rerun()


        # 🤖 About Project
        st.sidebar.markdown(
        "<h2 style='color:#00FFAA;'>🤖 About Project</h2>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:#E0E0E0;'>AI-powered sentiment analysis for <b style='color:#FFD700;'>restaurant reviews</b> 🍽️</p>"
        "<p style='color:#6BCB77;'>😊 Detect Positive & Negative emotions instantly</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 🐍 Libraries
        st.sidebar.markdown(
        "<h3 style='color:#FF4B4B;'>🐍 Libraries Used</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        ✔ <span style='color:#FFD93D;'>Scikit-learn</span><br>
        ✔ <span style='color:#4D96FF;'>Pandas</span><br>
        ✔ <span style='color:#6BCB77;'>NumPy</span><br>
        ✔ <span style='color:#FF6B6B;'>Joblib</span><br>
        ✔ <span style='color:#00FFFF;'>Streamlit</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # ☁️ Cloud
        st.sidebar.markdown(
        "<h3 style='color:#00FFFF;'>☁️ Cloud & Deployment</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:#E0E0E0;'>🚀 Hosted on <b style='color:#FFD700;'>Streamlit Cloud</b></p>"
        "<p style='color:#6BCB77;'>🌍 Access anywhere anytime</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 📊 Model Insights
        st.sidebar.markdown(
        "<h3 style='color:#FFA500;'>📊 Model Insights</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        🤖 <span style='color:#FFD700;'>Model:</span> Logistic Regression / Naive Bayes<br>
        📈 <span style='color:#00FFAA;'>High Accuracy Sentiment Detection</span><br>
        ⚡ <span style='color:#4D96FF;'>Fast Predictions</span><br>
        🔍 <span style='color:#FF6B6B;'>TF-IDF Vectorization</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 💡 Fun Facts
        st.sidebar.markdown(
        "<h3 style='color:#FF69B4;'>💡 Food Review Insights</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        🍔 <span style='color:#FFD700;'>Food reviews impact 90%+ customers</span><br>
        ⭐ <span style='color:#00FFAA;'>Positive reviews boost restaurant sales</span><br>
        ⚠️ <span style='color:#FF4B4B;'>Negative reviews highlight service issues</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 👥 About Us
        st.sidebar.markdown(
        "<h3 style='color:#9D4EDD;'>👥 About Us</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:white;'>Enter your food review and let AI predict if it's <span style='color:green;'>Positive</span> or <span style='color:red;'>Negative</span>.</p>"
        "<p style='color:#00FFFF;'>Built for smart restaurant analytics 🚀</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 📞 Contact
        st.sidebar.markdown(
        "<h3 style='color:#FF4B4B;'>📞 Contact Us</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        📱 <span style='color:#FFD700;'>98765XXXXX</span><br>
        📧 <span style='color:#00FFFF;'>Support Available</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 🏁 Footer image
        st.sidebar.image("flag.jpg")


def login_sentiment_sidebar():
        st.sidebar.markdown("""
        <style>
        .sidebar-banner {
            padding: 12px 15px;
            border-radius: 12px;
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            color: white;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            transition: all 0.4s ease;
            cursor: pointer;
            margin-bottom: 20px;
        }

        .sidebar-banner:hover {
            color: black;
            transform: scale(1.05);
        }
        </style>

        <div class="sidebar-banner">
            🍽️ Restaurant Panel
        </div>
        """, unsafe_allow_html=True)


        # 🍴 Image
        st.sidebar.image("restaurant_2.jpg")


        # 👋 Welcome Section
        st.sidebar.markdown(
        "<h2 style='color:#FF4B4B;'>👋 Welcome</h2>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:#E0E0E0;'>Login to explore <b style='color:#FFD700;'>AI-powered food sentiment insights</b> 🍽️</p>"
        "<p style='color:#6BCB77;'>Understand customer emotions in seconds ⚡</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 🤖 About App
        st.sidebar.markdown(
        "<h3 style='color:#00FFFF;'>🤖 About App</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:#E0E0E0;'>This app analyzes restaurant reviews using <b style='color:#FFD700;'>Machine Learning & NLP</b>.</p>"
        "<p style='color:#6BCB77;'>Helps restaurants improve quality & customer satisfaction 📈</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 🚀 Features
        st.sidebar.markdown(
        "<h3 style='color:#FF6B6B;'>🚀 Features</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        ✔ <span style='color:#FFD93D;'>Sentiment Analysis</span><br>
        ✔ <span style='color:#4D96FF;'>Bulk Review Prediction</span><br>
        ✔ <span style='color:#6BCB77;'>AI-powered Insights</span><br>
        ✔ <span style='color:#FF9F1C;'>Customer Mood Detection</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 🍴 Restaurants
        st.sidebar.markdown(
        "<h3 style='color:#FFA500;'>🍴 Restaurants</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        • <span style='color:#FFD700;'>The Royal Saffron</span><br>
        • <span style='color:#00FFAA;'>Velvet Table</span><br>
        • <span style='color:#FF6B6B;'>Aurora Fine Dining</span><br>
        • <span style='color:#4D96FF;'>Crystal Flame</span><br>
        <p style='color:#E0E0E0;'>👉 Explore more via <b>Get Credentials</b></p>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 📱 Login Guide
        st.sidebar.markdown(
        "<h3 style='color:#9D4EDD;'>📱 How to Login?</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        1️⃣ <span style='color:#FFD700;'>Click Get Credentials</span><br>
        2️⃣ <span style='color:#00FFAA;'>Select Restaurant</span><br>
        3️⃣ <span style='color:#FF6B6B;'>Scan QR Code</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 📊 Sentiment Insights (🔥 NEW ADDITION)
        st.sidebar.markdown(
        "<h3 style='color:#00FFAA;'>📊 Sentiment Insights</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        😊 <span style='color:#6BCB77;'>Positive reviews boost trust & sales</span><br>
        😞 <span style='color:#FF4B4B;'>Negative reviews highlight weak areas</span><br>
        ⭐ <span style='color:#FFD700;'>Ratings strongly influence customer decisions</span><br>
        📈 <span style='color:#4D96FF;'>Better sentiment = Higher retention</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 💡 Smart Facts
        st.sidebar.markdown(
        "<h3 style='color:#FF69B4;'>💡 Smart Facts</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        🍔 <span style='color:#FFD700;'>90% users read reviews before visiting</span><br>
        📊 <span style='color:#00FFAA;'>Online ratings impact revenue directly</span><br>
        ⚡ <span style='color:#4D96FF;'>Fast service = Positive sentiment boost</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 👨‍💻 Developer
        st.sidebar.markdown(
        "<h3 style='color:#00FFFF;'>🧑‍💻 Developer</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        "<p style='color:white;'>Made by: <b style='color:#FFD700;'>Dev Varshney</b></p>"
        "<p style='color:#6BCB77;'>AI/ML Enthusiast 🚀</p>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")


        # 📞 Contact
        st.sidebar.markdown(
        "<h3 style='color:#FF4B4B;'>📞 Contact</h3>",
        unsafe_allow_html=True
        )
        st.sidebar.markdown(
        """
        📱 <span style='color:#FFD700;'>9058068999</span><br>
        📧 <span style='color:#00FFFF;'>varshneyd110@gmail.com</span>
        """,
        unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

        # 🏁 Footer image
        st.sidebar.image("flag.jpg")




# ✅ Default value set (first time only)
if "theme" not in st.session_state:
        st.session_state.theme = True   # 👈 True = Dark Mode default

    # Toggle (linked with session state)
theme = st.toggle("🌙 Dark Mode", value=st.session_state.theme)

    # Update state
st.session_state.theme = theme

    # Apply theme
if theme:
        # 🌙 DARK MODE
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

else:
        # ☀️ LIGHT MODE
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True)

import streamlit.components.v1 as components
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("NLP_1.jpg")

components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>

    .banner {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        padding: 70px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        position: relative;
    }}

    .banner::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: rgba(0,0,0,0.6);
        border-radius: 20px;
    }}

    .banner-content {{
        position: relative;
        z-index: 2;
    }}

    .title {{
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(90deg, #ffcc70, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    transition: 0.3s;
}}

.title:hover {{
    transform: scale(1.05);
    background: linear-gradient(90deg, #00ffcc, #00c6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

    .subtitle {{
        font-size: 18px;
        margin-top: 10px;
    }}

    .rotator {{
        height: 180px;
        overflow: hidden;
    }}

    .rotator-inner {{
        display: flex;
        flex-direction: row;
        width: 250%;
        animation: scrollLeft 8s linear infinite;
    }}

    .slide {{
        min-width: 50%;
        flex-shrink: 0;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}

    @keyframes scrollLeft {{
    0% {{
        transform: translateX(0);
    }}
    100% {{
        transform: translateX(-50%);
    }}
}}

    </style>
    </head>

    <body>

    <div class="banner">
        <div class="banner-content">

            <div class="rotator-inner">

                        <!-- ORIGINAL -->
                        <div class="slide">
                            <div class="title">🧠 Natural Language Processing(NLP) Projects</div>
                            <div class="subtitle">Smart Text Analysis for Spam Detection & Sentiment Insights 🤖📊</div>
                            <div id="clock"></div>
                        </div>

                        <div class="slide">
                            <div class="title">🧠 Natural Language Processing(NLP) Projects</div>
                            <div class="subtitle">AI-Powered NLP System for Detecting Spam & Understanding Emotions 🧠💬</div>
                            <div id="clock2"></div>
                        </div>

                        <!-- DUPLICATE (same content again) -->
                        <div class="slide">
                            <div class="title">🧠 Natural Language Processing(NLP) Projects</div>
                            <div class="subtitle">Smart Text Analysis for Spam Detection & Sentiment Insights 🤖📊</div>
                            <div id="clock3"></div>
                        </div>

                        <div class="slide">
                            <div class="title">🧠 Natural Language Processing(NLP) Projects</div>
                            <div class="subtitle">AI-Powered NLP System for Detecting Spam & Understanding Emotions 🧠💬</div>
                            <div id="clock4"></div>
                        </div>

                    </div>

        </div>
    </div>

    <script>
    function updateClock() {{
        var now = new Date();

        var options = {{
            weekday: 'long',
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        }};

        var date = now.toLocaleDateString('en-IN', options);
        var time = now.toLocaleTimeString();

        var html = `
        <div style="
            font-size:30px;
            font-weight:bold;
            color:#00ffcc;
            text-shadow:0 0 10px #00ffcc, 0 0 20px #00ffcc;
            text-align:center;
        ">
        ⏰ ${{date}} ${{time}}
        </div>
        `;

        document.getElementById("clock").innerHTML = html;
        document.getElementById("clock2").innerHTML = html;
        document.getElementById("clock3").innerHTML = html;
        document.getElementById("clock4").innerHTML = html;
    }}

    setInterval(updateClock, 1000);
    updateClock();
    </script>

    </body>
    </html>
    """, height=300)




# Tabs
tab1, tab2 = st.tabs(["📩 Spam Classifier", "😊 Sentiment Analysis"])

# ✅ Cleaning function (IMPORTANT for spam model)
def mycleaning(text):
    import re
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    return text

spam_model = joblib.load("spam_model.pkl")
sentiment_model = joblib.load("sentiment_model.pkl")

# ✅ Prediction functions
def predict_spam(text):
    text = mycleaning(text)
    return spam_model.predict([text])[0]

def predict_sentiment(text):
    return sentiment_model.predict([text])[0]

# ❌ REMOVE THESE LINES (IMPORTANT)
# from spam import predict_spam
# from sentiment import predict_sentiment


# ---------------- TAB 1 ----------------
with tab1:
    st.markdown("## 📩 Spam Message Classifier")

    message = st.text_area("Enter your message", key="spam_text")

    if st.button("Check Spam", key="spam_btn",use_container_width=True):
        if message.strip() == "":
            st.warning("Please enter a message")
        else:
            result = predict_spam(message)

            if result == 1:
                st.error("🚫 This is Spam")
            else:
                st.success("✅ This is Not Spam")


# ---------------- TAB 2 ----------------
with tab2:
    st.markdown("## 😊 Sentiment Analysis")

    review = st.text_area("Enter review", key="sent_text")

    if st.button("Analyze", key="sent_btn",use_container_width=True):
        if review.strip() == "":
            st.warning("Please enter review")
        else:
            result = predict_sentiment(review)

            if result == 1:
                st.success("😊 Positive")
            else:
                st.error("😞 Negative")






# ✅ NAVBAR
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home",use_container_width=True):
        st.session_state.page = "home"

with col2:
    if st.button("📩 Spam",use_container_width=True):
        st.session_state.page = "spam"

with col3:
    if st.button("😊 Sentiment",use_container_width=True):
        st.session_state.page = "sentiment"

st.markdown("---")

# ✅ ROUTING SYSTEM

if st.session_state.page == "home":
    st.title("🧠 NLP Dashboard")
    st.info("Choose a module above 👆")
    NLP_sidebar()

elif st.session_state.page == "spam":

    blocked = (
        st.session_state.logged_in and 
        st.session_state.active_page != "spam"
    )

    if not st.session_state.logged_in:
        login_spam_sidebar()
    else:
        main_spam_sidebar()

    # Block UI
    if blocked:
        st.error("🚫 You are already logged into Sentiment")
        st.info("👉 Please logout first to continue")

    else:
        run_spam_app()

elif st.session_state.page == "sentiment":

    blocked = (
        st.session_state.logged_in and 
        st.session_state.active_page != "sentiment"
    )
        
    if not st.session_state.logged_in:
        login_sentiment_sidebar()
    else:
        main_sentiment_sidebar()

    # ❗ Block UI
    if blocked:
        st.error("🚫 You are already logged into Spam")
        st.info("👉 Please logout first to continue")

    else:
        # ✅ ONLY RUN WHEN NOT BLOCKED
        run_sentiment_app()

st.markdown("""
        <style>

        /* 🔥 Base Button */
        div.stButton > button {
            background: linear-gradient(135deg, #ff7e00, #ffb347);
            color: white;
            border-radius: 25px;
            padding: 12px 28px;   /* 👈 size smaller */
            border: 2px solid transparent;
            font-size: 16px;
            font-weight: bold;
            width: 100%;
            margin-top: 15px;
            position: relative;
            overflow: hidden;

            /* ✨ Glow + Glass effect */
            box-shadow: 0 4px 15px rgba(255, 128, 8, 0.4);
            backdrop-filter: blur(6px);

            transition: all 0.3s ease;
        }

        /* ✨ Shining Border Effect */
        div.stButton > button::before {
            content: "";
            position: absolute;
            inset: -2px;
            border-radius: 25px;
            background: linear-gradient(90deg, #ff7e00, #00c6ff, #ff416c, #ff7e00);
            background-size: 300%;
            z-index: -1;
            animation: borderGlow 4s linear infinite;
        }

        /* 🔥 Border animation */
        @keyframes borderGlow {
            0% { background-position: 0% }
            100% { background-position: 300% }
        }

        /* ✨ Inner shine overlay */
        div.stButton > button::after {
            content: "";
            position: absolute;
            top: 0;
            left: -75%;
            width: 50%;
            height: 100%;
            background: rgba(255,255,255,0.3);
            transform: skewX(-25deg);
        }

        /* 💫 Shine animation on hover */
        div.stButton > button:hover::after {
            animation: shineMove 0.8s forwards;
        }

        @keyframes shineMove {
            100% {
                left: 125%;
            }
        }

        /* 🎯 Text styling */
        div.stButton > button p {
            font-size: 18px !important;
            font-weight: bold;
            letter-spacing: 0.5px;
        }

        /* 🚀 Hover Effect */
        div.stButton > button:hover {
            transform: translateY(-3px) scale(1.04);
            box-shadow: 0 10px 30px rgba(0, 114, 255, 0.6);
            background: linear-gradient(135deg, #005bea, #003d99);
        }

        /* 🔽 Click effect */
        div.stButton > button:active {
            transform: scale(0.97);
        }

        </style>
        """, unsafe_allow_html=True)













