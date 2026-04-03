import streamlit as st
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit.components.v1 as components
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
from Database import save_news_prediction, get_all_news_predictions, create_news_table, clear_news_history

create_news_table()


if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

if "active_page" not in st.session_state:
    st.session_state.active_page = None




def send_otp_email(receiver_email, otp):

    sender_email = st.secrets["email"]["user"]
    app_password = st.secrets["email"]["password"]

    # ✅ Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🔐 OTP Verification - NLP Dashboard"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # ✅ HTML Email Content
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color:#f4f4f4; padding:20px;">
        <div style="
            max-width:500px;
            margin:auto;
            background:white;
            padding:20px;
            border-radius:10px;
            box-shadow:0 4px 10px rgba(0,0,0,0.1);
            text-align:center;
        ">
            <h2 style="color:#4CAF50;">🔐 OTP Verification</h2>
            
            <p style="font-size:16px; color:#333;">
                Dear User,
            </p>

            <p style="font-size:15px; color:#555;">
                Your One-Time Password (OTP) for secure login is:
            </p>

            <h1 style="
                background:#4CAF50;
                color:white;
                display:inline-block;
                padding:10px 20px;
                border-radius:8px;
                letter-spacing:3px;
            ">
                {otp}
            </h1>

            <p style="color:#777; font-size:14px;">
                This OTP is valid for a limited time. Please do not share it with anyone.
            </p>

            <hr style="margin:20px 0;">

            <p style="font-size:13px; color:#aaa;">
                If you did not request this, please ignore this email.
            </p>

            <p style="font-size:14px; color:#333;">
                Regards,<br>
                <b>NLP Dashboard Team 🤖</b>
            </p>
        </div>
    </body>
    </html>
    """

    # ✅ Attach HTML
    msg.attach(MIMEText(html, "html"))

    # ✅ Send email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()


def run_news_app():

    def login_news_page():
        USE_REAL_EMAIL = False   


        # ✅ Default value set (first time only)
        if "theme" not in st.session_state:
            st.session_state.theme = True   # 👈 True = Dark Mode default

        # Toggle (linked with session state)
        theme = st.toggle("🌙 Dark Mode", value=st.session_state.theme,key="spam_toggle")

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

        img_base64 = get_base64_image("background_1.png")

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
                                <div class="title">📰 News Classifier AI 🤖</div>
                                <div class="subtitle">Smartly categorizing news into Politics, Sports, Entertainment & more using AI 🚀</div>
                                <div id="clock"></div>
                            </div>

                            <div class="slide">
                                <div class="title">📰 News Classifier AI 🤖</div>
                                <div class="subtitle">Transforming headlines into meaningful insights with Machine Learning 📊</div>
                                <div id="clock2"></div>
                            </div>

                            <!-- DUPLICATE (same content again) -->
                            <div class="slide">
                                <div class="title">📰 News Classifier AI 🤖</div>
                                <div class="subtitle">Smartly categorizing news into Politics, Sports, Entertainment & more using AI 🚀</div>
                                <div id="clock3"></div>
                            </div>

                            <div class="slide">
                                <div class="title">📰 News Classifier AI 🤖</div>
                                <div class="subtitle">Transforming headlines into meaningful insights with Machine Learning 📊</div>
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

        col1,col2,col3=st.columns(3)

        with col2:
            st.markdown("## 🔐 Login to Continue")
            
        col1, col2,col3 = st.columns(3)

        with col1:
            st.markdown("""
        <style>
        .banner-enter {
            padding: 14px 22px;
            border-radius: 14px;

            /* 🔥 Email theme gradient */
            background: linear-gradient(135deg, #1e90ff, #00c6ff);

            color: white;
            font-size: 20px;
            font-weight: bold;
            text-align: center;

            /* ✨ Glow */
            box-shadow: 0 0 15px rgba(0,198,255,0.6);

            transition: all 0.4s ease;
            cursor: pointer;
            margin-top:40px;
        }

        /* ✨ Hover = more attractive */
        .banner-enter:hover {
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            transform: scale(1.07);
            box-shadow: 0 0 25px rgba(0,198,255,1);
            color: black;
        }

        /* ✨ Icon glow */
        .banner-enter::before {
            content: "📧 ";
            font-size: 22px;
        }
        </style>

        <div class="banner-enter">
            Enter your Email
        </div>
        """, unsafe_allow_html=True)
            

        if "step" not in st.session_state:
            st.session_state.step = "email"

        # ✅ STEP 1
        if st.session_state.step == "email":

            email = st.text_input("", placeholder="📩 Enter your email here")

            col1, col2, col3 = st.columns([1,3,1])

            with col2:
                if st.button("Continue",use_container_width=True):
                    if email:
                        st.session_state.email = email
                        st.session_state.step = "inbox"
                    else:
                        st.warning("⚠️ Enter Email First")

        import random


        if st.session_state.step == "inbox":

            st.subheader("📰 Select the Correct News Category")

            if "messages" not in st.session_state:

                # 📂 Categories
                news_data = {

                    "SPORTS": [
                        "🏏 India wins thrilling cricket match",
                        "⚽ Football team secures last-minute victory",
                        "🔥 Player scores hat-trick in final",
                        "🏅 Olympics training begins",
                        "🎾 Tennis star wins grand slam title",
                        "🌍 Team qualifies for world cup",
                        "🚀 Athlete breaks national record",
                        "🏀 Basketball finals draw huge crowd",
                        "📢 Coach announces new strategy",
                        "🌟 Cricket league attracts global audience",
                        "👟 Young player shines in debut match",
                        "🏆 Team wins championship after tough battle"
                    ],

                    "POLITICS": [
                        "🏛️ Government passes new bill in parliament",
                        "🗳️ Election results announced nationwide",
                        "⚖️ Opposition criticizes new policy",
                        "🎤 PM addresses the nation",
                        "📜 New law proposed for digital media",
                        "🏗️ Cabinet approves infrastructure project",
                        "🤝 Political leaders meet for discussion",
                        "📊 State elections see record turnout",
                        "💼 New tax reforms introduced",
                        "🚀 Government launches welfare scheme",
                        "🔥 Debate intensifies over policy changes",
                        "📣 Minister announces new development plan"
                    ],

                    "ENTERTAINMENT": [
                        "🎬 New movie breaks box office records",
                        "🌟 Actor announces upcoming project",
                        "🎵 Music album tops charts",
                        "🏆 Award show celebrates artists",
                        "💍 Celebrity wedding trends online",
                        "🎥 Director releases teaser of film",
                        "📺 Streaming platform launches new series",
                        "🌍 Film festival showcases global cinema",
                        "💰 Actor signs big budget deal",
                        "🔥 Web series gains popularity",
                        "🎤 Singer releases new hit song",
                        "📢 Reality show finale attracts audience"
                    ],

                    "ECONOMICS": [
                        "📈 Stock market hits record high",
                        "📉 Inflation rate drops this month",
                        "🚀 Startup raises funding",
                        "⛽ Oil prices increase globally",
                        "🏦 Central bank changes interest rates",
                        "🌍 Economy shows signs of recovery",
                        "📊 New business policy announced",
                        "📉 Unemployment rate decreases",
                        "💻 Tech companies report profits",
                        "🌐 Global trade sees growth",
                        "⚠️ Market volatility concerns investors",
                        "💼 Government plans economic reforms"
                    ],

                    "RELIGIOUS": [
                        "🙏 Festival celebrated with devotion",
                        "🛕 Temple ceremony attracts devotees",
                        "🚶 Pilgrimage begins this week",
                        "🕊️ Religious leaders promote peace",
                        "🌸 Spiritual event held in city",
                        "🛐 Devotees gather for prayer",
                        "🤲 Charity event organized by group",
                        "📿 Religious rituals performed traditionally",
                        "✨ Holy celebration unites communities",
                        "🕌 Faith-based gathering draws crowd",
                        "📢 Ceremony marks important occasion",
                        "🕯️ Prayer meetings held across region"
                    ]
                }
                

                # 🎯 Random category choose karo
                correct_category = random.choice(list(news_data.keys()))

                # ✅ Correct news
                correct_msg = random.choice(news_data[correct_category])

                # ❌ Wrong categories
                other_categories = [cat for cat in news_data if cat != correct_category]

                wrong_msgs = []
                for cat in random.sample(other_categories, 3):
                    wrong_msgs.append(random.choice(news_data[cat]))

                # 🔀 Combine & shuffle
                messages = wrong_msgs + [correct_msg]
                random.shuffle(messages)

                # 🔥 Save in session
                st.session_state.messages = messages
                st.session_state.correct_msg = correct_msg
                st.session_state.correct_category = correct_category

            # 🎯 Show target category
            st.info(f"👉 Select the **{st.session_state.correct_category}** news")

            # 📻 Options
            choice = st.radio("Choose correct news:", st.session_state.messages)

            col1, col2, col3 = st.columns([1,3,1])

            with col2:

                if st.button("Verify Selection", use_container_width=True):

                    if choice == st.session_state.correct_msg:
                        st.success("✅ Correct! You selected the right category news 🎉")

                        # reset
                        del st.session_state.messages
                        del st.session_state.correct_msg
                        del st.session_state.correct_category

                        st.session_state.step = "otp"

                    else:
                        st.error("❌ Wrong selection! Try again.")
        if st.session_state.step == "otp":

            st.subheader("🔐 OTP Verification")

            # ✅ Generate OTP only once
            if "otp" not in st.session_state:
                st.session_state.otp = str(random.randint(1000, 9999))

                # 🔥 MODE SWITCH
                if USE_REAL_EMAIL:
                    send_otp_email(st.session_state.email, st.session_state.otp)
                    st.success(f"📩 OTP sent to {st.session_state.email}")
                else:
                    st.info("📩 Demo Mode OTP")
                    st.code(f"Your OTP: {st.session_state.otp}")

            # 👉 User input
            user_otp = st.text_input("Enter OTP", placeholder="🔢 4-digit OTP")

            col1,col2,col3=st.columns([1,3,1])

            with col2:

            
                if st.button("🔄 Resend OTP",use_container_width=True):

                    st.session_state.otp = str(random.randint(1000, 9999))

                    if USE_REAL_EMAIL:
                        send_otp_email(st.session_state.email, st.session_state.otp)
                        st.success("📩 New OTP sent to your email!")
                    else:
                        st.success("📩 New OTP generated!")
                        st.code(f"New OTP: {st.session_state.otp}")

            col1,col2,col3=st.columns([1,3,1])

            with col2:

        
                if st.button("Verify OTP",use_container_width=True):

                    if user_otp == st.session_state.otp:
                        st.success("🎉 Login Successful!")

                        st.session_state.logged_in = True
                        st.session_state.active_page = "news"

                        # 🔥 RESET (important)
                        del st.session_state.otp
                        st.rerun()

                    else:
                        st.error("❌ Invalid OTP")

        st.markdown("""
        <style>

        /* Input box styling */
        .stTextInput > div > div > input {
            background: linear-gradient(135deg, #1f1f2e, #2c2c54);
            color: #ffffff;
            font-size: 20px;
            padding: 12px;
            border-radius: 12px;
            border: 2px solid #00c6ff;
            outline: none;
            transition: all 0.4s ease;
        }

        /* Placeholder color */
        .stTextInput > div > div > input::placeholder {
            color: #bbbbbb;
            font-size: 16px;
        }

        /* Hover effect */
        .stTextInput > div > div > input:hover {
            border: 2px solid #00f2fe;
            box-shadow: 0 0 10px #00c6ff;
        }

        /* Focus (click) effect 🔥 */
        .stTextInput > div > div > input:focus {
            border: 2px solid #00f2fe;
            box-shadow: 0 0 15px #00f2fe, 0 0 25px #00c6ff;
            background: linear-gradient(135deg, #141e30, #243b55);
        }

        </style>
        """, unsafe_allow_html=True)

        



        st.markdown("""
        <style>
        @keyframes fadeText {
            0% {opacity: 0;}
            5% {opacity: 1;}
            12% {opacity: 1;}
            17% {opacity: 0;}
            100% {opacity: 0;}
        }

        .text-container {
            position: relative;
            height: 40px;
            text-align: left;
            color: #00c6ff;
            font-size: 22px;
            font-weight: bold;
            margin-top: 40px;
            overflow: hidden; /* 🔥 important */
        }

        .text-container span {
            position: absolute;
            width: 100%;
            opacity: 0;
            animation: fadeText 16s linear infinite; /* 🔥 total = 8 × 2s */
        }

        /* Proper spacing */
        .text-container span:nth-child(1) { animation-delay: 0s; }
        .text-container span:nth-child(2) { animation-delay: 2s; }
        .text-container span:nth-child(3) { animation-delay: 4s; }
        .text-container span:nth-child(4) { animation-delay: 6s; }
        .text-container span:nth-child(5) { animation-delay: 8s; }
        .text-container span:nth-child(6) { animation-delay: 10s; }
        .text-container span:nth-child(7) { animation-delay: 12s; }
        .text-container span:nth-child(8) { animation-delay: 14s; }
        </style>

        <div class="text-container">
            <span>📰 Classify News Headlines in Seconds</span>
            <span>🤖 AI-Powered News Categorization</span>
            <span>📊 Get Smart Insights from News Data</span>
            <span>⚡ Real-Time News Classification</span>
            <span>🔍 Identify News Categories Instantly</span>
            <span>🧠 Powered by Machine Learning & NLP</span>
            <span>📂 Organize News into Smart Categories</span>
            <span>🚀 Fast & Accurate News Predictions</span>
        </div>
        """, unsafe_allow_html=True)

        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1f4037, #99f2c8);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin-top: 40px;
            ">
                <h4>📰 Total News Classified</h4>
                <h2>25K+</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #141e30, #243b55);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin-top: 40px;
            ">
                <h4>🎯 Model Accuracy</h4>
                <h2>93%</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #42275a, #734b6d);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin-top: 40px;
            ">
                <h4>📊 Categories Covered</h4>
                <h2>5 Types</h2>
            </div>
            """, unsafe_allow_html=True)


        
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

        
    def main_news_app():

        

        # ✅ Default value set (first time only)
        if "theme" not in st.session_state:
            st.session_state.theme = True   # 👈 True = Dark Mode default

        # Toggle (linked with session state)
        theme = st.toggle("🌙 Dark Mode", value=st.session_state.theme,key="main_spam_toggle")

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

        st.write("Welcome to 🛡️ AI-Powered Spam Detection System")

        model=joblib.load("news_model.pkl")

        import streamlit.components.v1 as components
        import base64

        def get_base64_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()

        img_base64 = get_base64_image("spam_1.jpg")

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
                                <div class="title">📰 Intelligent News Classification System</div>
                                <div class="subtitle">Classifying Headlines into Sports, Politics, Entertainment & More</div>
                                <div id="clock"></div>
                            </div>

                            <div class="slide">
                                <div class="title">📰 Intelligent News Classification System</div>
                                <div class="subtitle">Automatically Classify News into Categories</div>
                                <div id="clock2"></div>
                            </div>

                            <!-- DUPLICATE (same content again) -->
                            <div class="slide">
                                <div class="title">📰 Intelligent News Classification System</div>
                                <div class="subtitle">Classifying Headlines into Sports, Politics, Entertainment & More</div>
                                <div id="clock3"></div>
                            </div>

                            <div class="slide">
                                <div class="title">📰 Intelligent News Classification System</div>
                                <div class="subtitle">Automatically Classify News into Categories</div>
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


        

        st.write("\n")
        col1, col2,col3 = st.columns(3)

        with col1:
            st.markdown("""
            <style>
            .banner-enter {
                padding: 12px 20px;
                border-radius: 12px;
                background: linear-gradient(135deg, #ff416c, #ff4b2b);
                color: white;
                font-size: 20px;
                font-weight: bold;
                text-align: center;
                transition: all 0.4s ease;
                cursor: pointer;
                margin-top:40px;
            }

            .banner-enter:hover {
                background: linear-gradient(135deg, #ff416c, #ff4b2b);
                color: black;
                transform: scale(1.05);
            }
            </style>

            <div class="banner-enter">
                📰 Enter News Headlines
            </div>
            """, unsafe_allow_html=True)

        News = st.text_input("", placeholder="📰 Enter your News Headlines here")

        col1, col2, col3 = st.columns([1,3,1])

        with col2:

            if st.button("Predict", use_container_width=True):

                pred = model.classify(News)
                pred_prob = model.prob_classify(News)

                labels = pred_prob.samples()

                # best label
                best_label = max(labels, key=lambda label: pred_prob.prob(label))

                # confidence
                Confidence = round(pred_prob.prob(best_label) * 100, 2)

                # 🎯 Emoji Mapping
                emoji_map = {
                    "SPORTS": "⚽",
                    "POLITICS": "🏛️",
                    "ENTERTAINMENT": "🎬",
                    "ECONOMICS": "💰",
                    "RELIGIOUS": "🙏"
                    }

                Prediction = f"{emoji_map.get(best_label, '')} {best_label} News"

                    # 🔥 SAVE TO DATABASE
                save_news_prediction(News, Prediction, Confidence)

                   # 🎨 Category-based styles
                category_styles = {
                    "SPORTS": {
                        "color": "linear-gradient(90deg, #11998e, #38ef7d)",
                        "emoji": "⚽"
                    },
                    "POLITICS": {
                        "color": "linear-gradient(90deg, #1e3c72, #2a5298)",
                        "emoji": "🏛️"
                    },
                    "ENTERTAINMENT": {
                        "color": "linear-gradient(90deg, #ff416c, #ff4b2b)",
                        "emoji": "🎬"
                    },
                    "ECONOMICS": {
                        "color": "linear-gradient(90deg, #f7971e, #ffd200)",
                        "emoji": "💰"
                    },
                    "RELIGIOUS": {
                        "color": "linear-gradient(90deg, #8e2de2, #4a00e0)",
                        "emoji": "🙏"
                    }
                }

                # 🎯 Get style based on prediction
                style = category_styles.get(pred, {
                    "color": "linear-gradient(90deg, #333, #777)",
                    "emoji": "📰"
                })

                # 🎨 UI Card
                st.markdown(f"""
                    <div style="
                        background: {style['color']};
                        padding: 20px;
                        border-radius: 15px;
                        text-align: center;
                        color: white;
                        font-size: 22px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                        transition: 0.3s;
                    ">
                        {style['emoji']} <b>{pred}</b><br><br>
                        Confidence Score: <b>{Confidence:.2f}%</b>
                    </div>
                """, unsafe_allow_html=True)

                st.balloons()
                st.snow()
                                

                    
        col1, col2 , col3 = st.columns(3)

        with col1:

            st.markdown("""
            <style>
            .banner-bulk {
                padding: 12px 20px;
                border-radius: 12px;
                background: linear-gradient(135deg, #1d976c, #93f9b9);
                color: white;
                font-size: 20px;
                font-weight: bold;
                text-align: center;
                transition: all 0.4s ease;
                cursor: pointer;
                margin-top:40px;
                margin-bottom:20px;
                
            }

            .banner-bulk:hover {
                background: linear-gradient(135deg, #1d976c, #93f9b9);
                color: black;
                transform: scale(1.05);
            }
            </style>

            <div class="banner-bulk">
                📊 Bulk Prediction
            </div>
            """, unsafe_allow_html=True)

        file=st.file_uploader("select file",type=["csv","txt"])
        if file:
            df=pd.read_csv(file,names=["Message"])
            placeholder=st.empty()
            placeholder.dataframe(df)

        st.markdown("""
        <style>

        /* Input box styling */
        .stTextInput > div > div > input {
            background: linear-gradient(135deg, #1f1f2e, #2c2c54);
            color: #ffffff;
            font-size: 20px;
            padding: 12px;
            border-radius: 12px;
            border: 2px solid #00c6ff;
            outline: none;
            transition: all 0.4s ease;
        }

        /* Placeholder color */
        .stTextInput > div > div > input::placeholder {
            color: #bbbbbb;
            font-size: 16px;
        }

        /* Hover effect */
        .stTextInput > div > div > input:hover {
            border: 2px solid #00f2fe;
            box-shadow: 0 0 10px #00c6ff;
        }

        /* Focus (click) effect 🔥 */
        .stTextInput > div > div > input:focus {
            border: 2px solid #00f2fe;
            box-shadow: 0 0 15px #00f2fe, 0 0 25px #00c6ff;
            background: linear-gradient(135deg, #141e30, #243b55);
        }

        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <style>

        /* File uploader container */
        .stFileUploader {
            border: 2px dashed #00c6ff;
            border-radius: 15px;
            padding: 20px;
            background: linear-gradient(135deg, #1f1f2e, #2c2c54);
            transition: all 0.4s ease;
        }

        /* Hover effect */
        .stFileUploader:hover {
            border: 2px solid #00f2fe;
            box-shadow: 0 0 15px #00c6ff;
        }

        /* Upload button */
        .stFileUploader button {
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 8px 15px;
            border: none;
            transition: all 0.3s ease;
        }

        /* Button hover */
        .stFileUploader button:hover {
            background: linear-gradient(135deg, #ff512f, #dd2476);
            color: black;
            transform: scale(1.05);
        }

        /* Uploaded file text */
        .stFileUploader div {
            color: #ffffff;
            font-size: 16px;
        }

        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,3,1])

        with col2:

            if st.button("Predict", key="b2", use_container_width=True):

                df.columns = df.columns.str.strip().str.lower()
                corpus = df.iloc[:, 0]
                df.rename(columns={df.columns[0]: "news"}, inplace=True)

                # Prediction
                pred = [model.classify(text) for text in corpus]

                # Probability (confidence)
                prob = [
                    max(model.prob_classify(text).prob(label) 
                        for label in model.prob_classify(text).samples())
                    for text in corpus
                ]

                df["Prediction"] = pred
                df["Confidence"] = [round(p * 100, 2) for p in prob]

                # 🎯 Emoji Mapping
                emoji_map = {
                    "SPORTS": "⚽ Sports",
                    "POLITICS": "🏛️ Politics",
                    "ENTERTAINMENT": "🎬 Entertainment",
                    "ECONOMICS": "💰 Economics",
                    "RELIGIOUS": "🙏 Religious"
                }

                df["Prediction"] = df["Prediction"].map(emoji_map)

                placeholder.dataframe(df)

                # 🔥 SAVE BULK DATA
                for i in range(len(df)):
                    save_news_prediction(
                        df["news"][i],
                        df["Prediction"][i],
                        df["Confidence"][i]
                    )

                # 📊 Summary Calculation
                counts = df["Prediction"].value_counts()

                # 🎉 UI Metrics
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("⚽ Sports", counts.get("⚽ Sports", 0))

                with col2:
                    st.metric("🏛️ Politics", counts.get("🏛️ Politics", 0))

                with col3:
                    st.metric("🎬 Entertainment", counts.get("🎬 Entertainment", 0))

                col4, col5 = st.columns(2)

                with col4:
                    st.metric("💰 Economics", counts.get("💰 Economics", 0))

                with col5:
                    st.metric("🙏 Religious", counts.get("🙏 Religious", 0))

                st.metric("📊 Total News", len(df))

                st.success("🎉 Bulk Prediction Completed!")
                st.markdown("""
                <div style="
                    background: linear-gradient(90deg, #1e3c72, #2a5298);
                    padding: 12px;
                    border-radius: 10px;
                    color: white;
                    font-weight: bold;
                    text-align: center;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                ">
                📰 AI classifying news into multiple categories in real-time 🚀
                </div>
                """, unsafe_allow_html=True)


                # 🎨 Metric Styling
                st.markdown("""
                <style>
                [data-testid="metric-container"] {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    padding: 15px;
                    border-radius: 12px;
                    color: white;
                }
                </style>
                """, unsafe_allow_html=True)


                # 📊 Category Count (IMPORTANT)
                counts = df["Prediction"].value_counts()

                data = {
                    "Prediction": counts.index.tolist(),
                    "Count": counts.values.tolist()
                }

                import plotly.express as px

                fig = px.pie(
                    values=data["Count"],
                    names=data["Prediction"],
                    hole=0.4
                )

                fig.update_layout(
                    width=400,
                    height=400
                )

                st.plotly_chart(fig, use_container_width=False)


                # 🎉 Effects
                st.balloons()
                st.snow()
        


        
        

        
        sample_news_data = pd.DataFrame({

            "news": [

            # 🏛️ POLITICS
            "Government passes new education reform bill",
            "Prime Minister addresses the nation on economic growth",
            "Election results spark debate across the country",
            "Opposition criticizes new tax policy",
            "Parliament session adjourned after heated arguments",
            "New foreign policy strategy announced",
            "State elections see record voter turnout",
            "Government launches new welfare scheme",
            "Political leaders meet to discuss national security",
            "New law proposed to regulate digital media",
            "Cabinet approves major infrastructure project",
            "Election campaign intensifies across states",

            # ⚽ SPORTS
            "India wins thrilling cricket match against Australia",
            "Football team secures victory in final minutes",
            "Olympic preparations begin with strong training camp",
            "Star player scores hat-trick in championship game",
            "Tennis champion wins grand slam title",
            "Team qualifies for world cup after intense match",
            "Coach announces new squad for upcoming series",
            "Basketball league finals attract huge audience",
            "Athlete breaks national record in sprint",
            "Cricket series postponed due to weather conditions",
            "India defeats England in a nail-biting cricket series",
            "Football club wins league title after dramatic comeback",
            "National team begins training camp ahead of tournament",
            "Striker scores winning goal in final seconds of match",
            "Tennis player advances to finals after tough semifinal",
            "Team secures spot in playoffs with crucial victory",
            "Coach reveals strategy for upcoming international games",
            "Athlete sets new world record in marathon race",
            "Cricket board announces new domestic tournament",
            "Fans celebrate massive win in stadium",
            "Youth sports program launched to promote fitness",
            "International player signs contract with top club"
            
            # 🎬 ENTERTAINMENT
            "New Bollywood movie breaks box office records",
            "Famous actor announces upcoming film project",
            "Music album tops global charts in first week",
            "Celebrity wedding becomes trending topic online",
            "Streaming platform releases highly anticipated series",
            "Director reveals teaser of upcoming blockbuster",
            "Award show celebrates best performances of the year",
            "Actor signs multi-million dollar film deal",
            "New web series gains massive popularity",
            "Film festival showcases international cinema",

            # 💰 ECONOMICS
            "Stock market reaches all-time high this week",
            "Central bank increases interest rates",
            "Inflation rate shows slight decline this month",
            "Global economy expected to grow steadily",
            "New startup raises millions in funding round",
            "Oil prices rise due to global demand",
            "Government announces new economic stimulus package",
            "Cryptocurrency market sees major fluctuations",
            "Unemployment rate drops significantly",
            "Tech companies report strong quarterly earnings",

            # 🙏 RELIGIOUS
            "Thousands gather for annual religious festival",
            "Temple inauguration ceremony attracts devotees",
            "Pilgrimage season begins with large crowds",
            "Religious leaders promote peace and unity",
            "Festival celebrations bring communities together",
            "Spiritual event held with traditional rituals",
            "Devotees visit shrine during holy occasion",
            "Religious ceremony conducted with great enthusiasm",
            "Charity event organized by religious group",
            "Prayer meetings held across the city"
            ]
        })

        
            
           

        csv = sample_news_data.to_csv(index=False, header=False).encode('utf-8')
        
        # 🎨 Banner
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                margin-top: 20px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
                    ">
                <h1 style="
                    color: white;
                    margin-bottom: 10px;
                    font-size: 24px;
                    letter-spacing: 1px;
                        ">
                    📥 Don't have a dataset?
                </h1>
                <p style="
                    color: #dcdcdc;
                    font-size: 14px;
                    margin-bottom: 20px;
                        ">
                    Download a ready-to-use sample dataset and start predicting instantly 🚀
                </p>
            </div>
        """, unsafe_allow_html=True)

        import base64

        def create_download_link(csv, filename, text, cls):
            b64 = base64.b64encode(csv).decode()
            return f'<a class="custom-btn {cls}" href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'


        st.markdown("""
        <style>

        /* 🔥 Base Button */
        .custom-btn {
            display: block;
            width: 85%;              /* width increase */
            margin: auto;            /* center align */
            padding: 18px 0;
            border-radius: 15px;
            font-weight: bold;
            font-size: 18px;
            text-decoration: none;
            text-align: center;
            color: #ffffff;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            backdrop-filter: blur(5px);
                    
            animation: glow 2s infinite alternate;

            @keyframes glow {
                from { box-shadow: 0 0 10px rgba(255,255,255,0.2); }
                to { box-shadow: 0 0 25px rgba(255,255,255,0.6); }
            }
        }

        /* ✨ Hover Common */
        .custom-btn:hover {
            transform: translateY(-4px) scale(1.05);
            box-shadow: 0 12px 30px rgba(0,0,0,0.5);
        }

        

        /* 🔵 Email */
        .email {
            background: rgba(0, 114, 255, 0.25);
            border: 1px solid rgba(0, 114, 255, 0.4);
            color: #ffffff;
            text-shadow: 0 0 8px rgba(255,255,255,0.7);
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6);
            
        }
        .email:hover {
            background: rgba(0, 114, 255, 0.4);
            transform: translateY(-5px) scale(1.07);
            box-shadow: 0 12px 40px rgba(0, 114, 255, 0.6);
        }

        

        </style>
        """, unsafe_allow_html=True)

        # 🔥 Layout
        col1, col2, col3 = st.columns(3)

        

        with col2:
            st.markdown(
                create_download_link(csv, "news.csv", "⬇️ Different News Dataset", "news"),
                unsafe_allow_html=True
            )

        

        col1, col2 = st.columns(2)

        with col1:
            show_btn = st.button("📂 Show History",use_container_width=True)

        

        with col2:
            if st.button("🗑️ Clear History"):
                clear_news_history()
                st.success("🗑️ History Cleared!",use_container_width=True)

        if show_btn:
            data = get_all_news_predictions()

            
            history_df = pd.DataFrame(
                data,
                columns=["ID", "News", "Prediction", "Confidence"]
            )

            st.dataframe(history_df)

        

        st.markdown("""
        <style>

        /* File uploader container */
        .stFileUploader {
            border: 2px dashed #00c6ff;
            border-radius: 15px;
            padding: 20px;
            background: linear-gradient(135deg, #1f1f2e, #2c2c54);
            transition: all 0.4s ease;
        }

        /* Hover effect */
        .stFileUploader:hover {
            border: 2px solid #00f2fe;
            box-shadow: 0 0 15px #00c6ff;
        }

        /* Upload button */
        .stFileUploader button {
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 8px 15px;
            border: none;
            transition: all 0.3s ease;
        }

        /* Button hover */
        .stFileUploader button:hover {
            background: linear-gradient(135deg, #ff512f, #dd2476);
            color: black;
            transform: scale(1.05);
        }

        /* Uploaded file text */
        .stFileUploader div {
            color: #ffffff;
            font-size: 16px;
        }

        </style>
        """, unsafe_allow_html=True)


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

        

        st.markdown("""
        <style>
        @keyframes fadeText {
            0% {opacity: 0;}
            5% {opacity: 1;}
            12% {opacity: 1;}
            17% {opacity: 0;}
            100% {opacity: 0;}
        }

        .text-container {
            position: relative;
            height: 40px;
            text-align: left;
            color: #00c6ff;
            font-size: 22px;
            font-weight: bold;
            margin-top: 40px;
            overflow: hidden; /* 🔥 important */
        }

        .text-container span {
            position: absolute;
            width: 100%;
            opacity: 0;
            animation: fadeText 16s linear infinite; /* 🔥 total = 8 × 2s */
        }

        /* Proper spacing */
        .text-container span:nth-child(1) { animation-delay: 0s; }
        .text-container span:nth-child(2) { animation-delay: 2s; }
        .text-container span:nth-child(3) { animation-delay: 4s; }
        .text-container span:nth-child(4) { animation-delay: 6s; }
        .text-container span:nth-child(5) { animation-delay: 8s; }
        .text-container span:nth-child(6) { animation-delay: 10s; }
        .text-container span:nth-child(7) { animation-delay: 12s; }
        .text-container span:nth-child(8) { animation-delay: 14s; }
        </style>

        <div class="text-container">
            <span>📰 Classify News Headlines in Seconds</span>
            <span>🤖 AI-Powered News Categorization</span>
            <span>📊 Get Smart Insights from News Data</span>
            <span>⚡ Real-Time News Classification</span>
            <span>🔍 Identify News Categories Instantly</span>
            <span>🧠 Powered by Machine Learning & NLP</span>
            <span>📂 Organize News into Smart Categories</span>
            <span>🚀 Fast & Accurate News Predictions</span>
        </div>
        """, unsafe_allow_html=True)


        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1f4037, #99f2c8);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin-top: 40px;
            ">
                <h4>📰 Total News Classified</h4>
                <h2>25K+</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #141e30, #243b55);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin-top: 40px;
            ">
                <h4>🎯 Model Accuracy</h4>
                <h2>93%</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #42275a, #734b6d);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin-top: 40px;
            ">
                <h4>📊 Categories Covered</h4>
                <h2>5 Types</h2>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.logged_in == False:
        login_news_page()
    else:
        main_news_app()


