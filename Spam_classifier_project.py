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
from Database import save_spam_prediction, get_all_spam_predictions, create_spam_table, clear_spam_history

create_spam_table()



def mycleaning(doc):
        return re.sub("[^a-zA-Z ]","",doc).lower()

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

def run_spam_app():
    
    def login_spam_page():
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
                                <div class="title">🛡️ Spam Shield AI 📩</div>
                                <div class="subtitle">Defending you from spam, phishing & digital fraud using intelligent AI 🚀</div>
                                <div id="clock"></div>
                            </div>

                            <div class="slide">
                                <div class="title">🛡️ Spam Shield AI 📩</div>
                                <div class="subtitle">Protecting your inbox from spam, scams & phishing with smart AI 🛡️</div>
                                <div id="clock2"></div>
                            </div>

                            <!-- DUPLICATE (same content again) -->
                            <div class="slide">
                                <div class="title">🛡️ Spam Shield AI 📩</div>
                                <div class="subtitle">Defending you from spam, phishing & digital fraud using intelligent AI 🚀</div>
                                <div id="clock3"></div>
                            </div>

                            <div class="slide">
                                <div class="title">🛡️ Spam Shield AI 📩</div>
                                <div class="subtitle">Protecting your inbox from spam, scams & phishing with smart AI 🛡️</div>
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

            col1, col2, col3 = st.columns(3)

            with col2:
                if st.button("Continue",use_container_width=True):
                    if email:
                        st.session_state.email = email
                        st.session_state.step = "inbox"
                    else:
                        st.warning("⚠️ Enter Email First")

        import random

        if st.session_state.step == "inbox":

            st.subheader("📥 Select the REAL (Valid) Message")

            # ✅ Only generate once
            if "messages" not in st.session_state:

                valid_messages = [
                "📦 Your Amazon order has been shipped",
                "📬 Your bank statement is ready",
                "🧾 Electricity bill generated for this month",
                "📚 Your course has been successfully enrolled",
                "🏦 Your account balance has been updated",
                "💳 Payment of ₹1,200 successful via UPI",
                "📨 You have received a new message",
                "📅 Your appointment is confirmed for tomorrow",
                "🚚 Your package will be delivered today",
                "📊 Your monthly report is now available",
                "🔔 Reminder: Meeting scheduled at 3 PM",
                "🏫 Your exam schedule has been released",
                "📥 New email received in your inbox",
                "🎓 Certificate of completion is available",
                "🛒 Your order has been delivered successfully",
                "📱 OTP for your login is 4821",
                "💼 Job application submitted successfully",
                "🏥 Your medical report is ready",
                "📦 Return request has been processed",
                "📈 Your investment summary is available",
                "🚆 Train ticket booking confirmed",
                "✈️ Flight booking confirmation received",
                "📍 Your cab has arrived at your location",
                "🔐 Password changed successfully",
                "📄 Your document has been uploaded",
                "🧑‍💻 Login successful from a new device",
                "💡 Your electricity payment was received",
                "📦 Your Flipkart order is out for delivery",
                "📢 Official update from your organization",
                "🪪 KYC verification completed successfully"
            ]

                spam_messages = [
                "🔥 You won ₹50,000! Click now",
                "💳 Update your bank details urgently",
                "🎉 Free iPhone giveaway",
                "🚨 Your account will be blocked! Login now",
                "💰 Earn money fast from home",
                "🎁 Claim your reward now",
                "⚠️ Your bank account is suspended! Verify immediately",
                "📢 Limited offer! Get 90% discount now",
                "💵 Double your money in 24 hours",
                "📲 Click here to claim your cashback reward",
                "🎊 Congratulations! You are selected as a winner",
                "🔓 Your account has been hacked! Secure it now",
                "💸 Instant loan approved! Apply now",
                "📩 You have a pending refund, claim now",
                "🤑 Earn ₹5000 daily without investment",
                "🚀 Work from home & earn unlimited money",
                "📛 Your PAN card will be blocked! Update now",
                "💥 Urgent! Verify your KYC or account will close",
                "🎯 You’ve been selected for a lucky draw",
                "📦 Your parcel is on hold! Pay delivery charges",
                "💳 Suspicious transaction detected! Click to resolve",
                "📢 Get free Netflix subscription now",
                "🎁 Special gift waiting for you! Claim now",
                "⚡ Hurry! Offer expires in 10 minutes",
                "📲 Download this app & earn money instantly",
                "🔗 Click this link to secure your account",
                "💰 You have won a lottery of ₹10 lakh",
                "📩 IRS refund pending – submit details now",
                "🧾 Tax issue detected! Fix immediately",
                "🚨 Your SIM card will be blocked! Update details now"
            ]

                # 👉 1 VALID
                correct_msg = random.choice(valid_messages)

                # 👉 ONLY SPAM (3 random)
                random_spam = random.sample(spam_messages, 3)

                # 👉 Combine
                messages = random_spam + [correct_msg]
                random.shuffle(messages)

                # 🔥 STORE in session (IMPORTANT)
                st.session_state.messages = messages
                st.session_state.correct_msg = correct_msg

            # 👉 Show messages
            choice = st.radio("Choose correct message:", st.session_state.messages)

            if st.button("Verify Selection",use_container_width=True):

                if choice == st.session_state.correct_msg:
                    st.success("✅ Correct! Moving to OTP verification...")
                    
                    # 🔥 RESET for next login (important)
                    del st.session_state.messages
                    del st.session_state.correct_msg

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

            # 🔥 BUTTON LAYOUT (better UX)
            col1, col2 = st.columns(2)

            # 🔄 RESEND OTP
            with col1:
                if st.button("🔄 Resend OTP",use_container_width=True):

                    st.session_state.otp = str(random.randint(1000, 9999))

                    if USE_REAL_EMAIL:
                        send_otp_email(st.session_state.email, st.session_state.otp)
                        st.success("📩 New OTP sent to your email!")
                    else:
                        st.success("📩 New OTP generated!")
                        st.code(f"New OTP: {st.session_state.otp}")

            # ✅ VERIFY OTP
            with col2:
                if st.button("Verify OTP",use_container_width=True):

                    if user_otp == st.session_state.otp:
                        st.success("🎉 Login Successful!")

                        st.session_state.logged_in = True
                        st.session_state.active_page = "spam"

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
            <span>🔍 Detect Spam Messages in Seconds</span>
            <span>🤖 Identify Fraud & Suspicious Content</span>
            <span>📊 Get AI-Powered Spam Insights</span>
            <span>🛡️ Protect Yourself from Scam Messages</span>
            <span>📩 Classify Messages Instantly</span>
            <span>🚫 Filter Out Spam & Scams</span>
            <span>🤖 Powered by Machine Learning</span>
            <span>🔐 Stay Safe from Fraud Messages</span>
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
                <h4>📩 Total Messages Scanned</h4>
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
                <h2>92%</h2>
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
                <h4>⚠️ Spam Messages Blocked</h4>
                <h2>10K+</h2>
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


    def main_spam_app():

        

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

        model=joblib.load("spam_model.pkl")

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
                                <div class="title">📩 Spam Message Classifier</div>
                                <div class="subtitle">Intelligent Protection Against Spam & Scam Messages</div>
                                <div id="clock"></div>
                            </div>

                            <div class="slide">
                                <div class="title">📩 Spam Message Classifier</div>
                                <div class="subtitle">Stay Safe from Fraud & Spam Messages</div>
                                <div id="clock2"></div>
                            </div>

                            <!-- DUPLICATE (same content again) -->
                            <div class="slide">
                                <div class="title">📩 Spam Message Classifier</div>
                                <div class="subtitle">Intelligent Protection Against Spam & Scam Messages</div>
                                <div id="clock3"></div>
                            </div>

                            <div class="slide">
                                <div class="title">📩 Spam Message Classifier</div>
                                <div class="subtitle">Stay Safe from Fraud & Spam Messages</div>
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
                📩 Enter Message
            </div>
            """, unsafe_allow_html=True)

        Message=st.text_input("",placeholder="📩 Enter your message here")
        
        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            if st.button("Predict",use_container_width=True):

                pred = model.predict([Message])
                prob = model.predict_proba([Message])

                # 🎯 Sentiment decide karo
                if pred[0] == "ham":
                    Prediction = "👍 Valid Message"
                    Confidence = prob[0][0]
                else:
                    Prediction = "👎 SPAM Message"
                    Confidence = prob[0][1]

                # 🔥 SAVE TO DATABASE
                save_spam_prediction(Message, Prediction, Confidence)

                # 🎨 UI Display (SIRF EK BAAR)
                if pred[0] == "ham":
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(90deg, #ff4b5c, #ff6b6b);
                            background: linear-gradient(90deg, #28a745, #5cd65c);
                            padding: 20px;
                            border-radius: 15px;
                            text-align: center;
                            color: white;
                            font-size: 20px;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                        ">
                            👍 <b>Valid Message</b><br><br>
                            Confidence Score: <b>{Confidence:.2f}</b>
                        </div>
                    """, unsafe_allow_html=True)


                    st.balloons()
                    st.snow()

                else:
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(90deg, #ff4b5c, #ff6b6b);
                            padding: 20px;
                            border-radius: 15px;
                            text-align: center;
                            color: white;
                            font-size: 20px;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                        ">
                            👎 <b>SPAM Message</b><br><br>
                            Confidence Score: <b>{Confidence:.2f}</b>
                        </div>
                    """, unsafe_allow_html=True)

                    

                    
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

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            # Button
            if st.button("Predict",key="b2",use_container_width=True):
                corpus=df.Message
                pred=model.predict(corpus)
                prob=np.max(model.predict_proba(corpus),axis=1)
                df["Prediction"]=pred
                df["Confidence"]=prob
                df["Prediction"]=df["Prediction"].map({"ham":"👍Valid Message","spam":"👎SPAM Message"})
                placeholder.dataframe(df)

                # 🔥 SAVE BULK DATA TO DATABASE
                for i in range(len(df)):
                    save_spam_prediction(
                        df["Message"][i],
                        df["Prediction"][i],
                        df["Confidence"][i]
                    )

                # 📊 Summary calculation
                Valid_count = (df["Prediction"] == "👍Valid Message").sum()
                SPAM_count = (df["Prediction"] == "👎SPAM Message").sum()

                # 🎉 Attractive Result Card
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        label="👍 Valid Message",
                        value=Valid_count
                    )

                with col2:
                    st.metric(
                        label="👎 SPAM Message",
                        value=SPAM_count
                    )
                
                with col3:
                    st.metric(
                        label="📊 Total Messages",
                        value=SPAM_count + Valid_count
                    )
                st.success("🎉 Bulk Prediction Completed!")
                st.markdown("""
                    <div style="
                        background: linear-gradient(90deg, #ff416c, #ff4b2b);
                        padding: 12px;
                        border-radius: 10px;
                        color: white;
                        font-weight: bold;
                        text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    ">
                    💬 AI detecting spam & protecting users from scams in real-time 🚀
                    </div>
                    """, unsafe_allow_html=True)
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

                

                data = {
                    "Prediction": ["Valid Message", "SPAM Message"],
                    "Count": [Valid_count, SPAM_count]
                }

                fig = px.pie(
                    values=data["Count"],
                    names=data["Prediction"],
                    hole=0.4   # donut style (optional)
                )

                fig.update_layout(
                    width=350,   # 👈 size control
                    height=350
                )

                st.plotly_chart(fig, use_container_width=False)
                st.balloons()
                st.snow()

        


        # Sample dataset (tum apna bhi bana sakte ho)
        sample_spam_email_data = pd.DataFrame({
            "message": [
        "Subject: Congratulations! You have won a free iPhone. Click here to claim your reward.",
        r"Subject: Meeting Today\nHi, are we still meeting today. Please confirm.",
        r"Subject: Urgent Security Alert\nYour account has been compromised. Kindly verify immediately.",
        r"Subject: Lunch Plan\nHi, let's catch up tomorrow for lunch.",
        r"Subject: Cash Prize Notification\nYou have been selected for a ₹50,000 cash prize. Claim now.",
        r"Subject: Reach Home Safely\nPlease call me when you reach home.",
        r"Subject: Travel Offer\nWin a free vacation to Goa! Limited time offer.",
        r"Subject: Assignment Reminder\nDon't forget to submit your assignment on time.",
        r"Subject: Loan Offer\nGet cheap loans at 0% interest. Apply today.",
        r"Subject: Notes Request\nCan you please send me the notes.",
        r"Subject: Exclusive Deal\nSpecial deal just for you. Click to explore now.",
        r"Subject: Meeting Update\nThe meeting has been postponed to 5 PM.",
        r"Subject: Work From Home Opportunity\nEarn money from home easily. No experience required.",
        r"Subject: Birthday Wishes\nHappy Birthday! Wishing you a great day ahead.",
        r"Subject: OTP Verification\nYour OTP is 456789. Do not share it with anyone.",
        r"Subject: Electronics Sale\nLowest prices on electronics. Shop now.",
        r"Subject: Party Invitation\nAre you coming to the party tonight.",
        r"Subject: Lottery Winner\nCongratulations! You have won ₹10 lakhs.",
        r"Subject: Document Review\nPlease review the attached document.",
        r"Subject: Competition Entry\nFree entry in a weekly competition to win tickets.",
        r"Subject: Movie Plan\nLet's go for a movie this weekend.",
        r"Subject: Limited Time Offer\nAct now! Don't miss this discount offer.",
        r"Subject: Call Later\nI'll call you later.",
        r"Subject: Quick Money Trick\nGet rich quickly with this simple trick.",
        r"Subject: Order Update\nYour order has been shipped successfully.",
        r"Subject: Recharge Offer\nClaim your free recharge now.",
        r"Subject: Location Check\nWhere are you right now.",
        r"Subject: Prize Reward\nCongratulations! You are selected for a reward.",
        r"Subject: Appointment Reminder\nDoctor appointment scheduled at 6 PM.",
        r"Subject: Gift Voucher\nYou have won a gift voucher worth ₹5000.",
        r"Subject: Dinner Invitation\nJoin us for dinner tonight.",
        r"Subject: BOGO Offer\nLimited time offer: Buy one get one free.",
        r"Subject: Address Request\nPlease send me your address.",
        r"Subject: Credit Card Offer\nYou have been pre-approved for a credit card.",
        r"Subject: Greetings\nGood morning! Have a nice day.",
        r"Subject: Reward Link\nClick this link to claim your reward.",
        r"Subject: Meeting Reschedule\nCan we reschedule our meeting.",
        r"Subject: Bonus Offer\nExclusive bonus waiting for you.",
        r"Subject: Delivery Update\nYour package will arrive tomorrow.",
        r"Subject: Cash Prize Contest\nWin cash prizes by participating now."
        r"Subject: You've Won a ₹25,00,000 Lottery Prize!\nCongratulations! Your email has been selected as a winner. Claim your prize by submitting your bank details immediately.",
        r"Subject: Security Alert from Gmail\nSuspicious login attempt detected. If this wasn't you, please reset your password immediately using the link below.",
        r"Subject: Amazon Order Confirmation (Fake)\nYour order for iPhone 15 has been successfully placed. If you did not make this purchase, cancel it now.",
        r"Subject: Income Tax Refund Notification\nYou are eligible for a tax refund of ₹48,500. Submit your details to receive the amount within 24 hours.",
        r"Subject: Job Offer - Earn ₹80,000/month from Home\nNo experience required. Limited slots available. Register now by paying a small fee.",
        r"Subject: Netflix Subscription Expired\nYour account has been suspended due to failed payment. Renew now to continue watching.",
        r"Subject: Bank Alert: Account Locked\nYour account has been temporarily locked due to suspicious activity. Verify your identity immediately.",
        r"Subject: Free Gift Card Inside 🎁\nYou have been selected to receive a ₹5000 gift card. Click here to claim before it expires.",
        r"Subject: Urgent Invoice Attached\nPlease find the attached invoice for your recent transaction. Pay immediately to avoid penalties.",
        r"Subject: Google Security Warning\nYour account storage is full. Upgrade now or your emails will be deleted permanently.",
        r"Subject: WhatsApp Account Banned\nYour number will be banned permanently. Verify your account immediately.",
        r"Subject: Congratulations! You Are Selected\nYou have been shortlisted for an exclusive reward program. Submit your details now.",
        r"Subject: Crypto Investment Opportunity\nDouble your money in 7 days with this guaranteed crypto plan. Join now.", 
        r"Subject: Electricity Bill Overdue\nYour power supply will be disconnected today. Pay your bill immediately to avoid disruption.",
    
    ]
                
        })

        sample_spam_whatsapp_data = pd.DataFrame({
            "message": [
            "Congrats! You won a free iPhone  Click here to claim now  bit.ly/offer",
            "Hey bro, kal mil rahe ho kya?",
            " Urgent: Your bank account will be blocked! Verify now  link",
            "Aaj ka plan kya hai?",
            " You have won ₹50,000 cash prize! Claim now fast!",
            "Ghar pahunch ke call kar dena",
            " Goa trip FREE! Limited offer, jaldi click karo!",
            "Assignment submit kar diya kya?",
            " Get instant loan at 0'%' interest  Apply now!",
            "Notes bhej de please",
            " Exclusive deal just for you! Grab now  link",
            "Meeting 5 baje shift ho gayi hai",
            " Work from home job! Earn ₹80k/month easily",
            "Happy Birthday bhai ",
            "Your OTP is 456789. Kisi ko mat batana",
            " Electronics sale! Cheapest prices available",
            "Party me aa raha hai na?",
            " Lottery winner! ₹10 lakh jeet gaye ho!",
            "Document check kar lena ek baar",
            " Free tickets jeeto! Participate now",
            "Movie chalein weekend pe?",
            " Limited offer! Abhi buy karo warna miss ho jayega",
            "Baad me call karta hu",
            " Paisa double in 7 days! Try this trick now",
            "Order deliver ho gaya hai",
            " Free recharge pao abhi!",
            "Kaha ho abhi?",
            " Reward jeetne ka mauka! Click now",
            "Doctor appointment yaad hai na 6 baje",
            " ₹5000 gift voucher jeeto abhi!",
            "Dinner ke liye aa jana",
            " Buy 1 Get 1 FREE offer!",
            "Address send kar de",
            " Credit card approved! Activate now",
            "Good morning  have a nice day",
            " Link pe click karo aur reward lo",
            "Meeting reschedule kar sakte hain kya?",
            " Bonus waiting for you! Claim fast",
            " Parcel kal deliver ho jayega",
            " Cash prize jeetne ka chance! Participate now",
            " WhatsApp account banned hone wala hai! Verify now",
            " Electricity bill pending! Pay immediately",
            " Earn money daily from home! Join now",
            "Kal class hai kya?",
            " Crypto me invest karo aur paisa double karo",
            "Are you free right now?",
            " Bank alert: account locked! Update details now"
        ]
                
        })

        sample_spam_sms_data = pd.DataFrame({
            "message": [
            "Congrats! You won a free iPhone. Claim now at link",
            "Hey, where are you?",
            "URGENT: Your bank account will be blocked. Verify now",
            "Call me when you reach",
            "You have won ₹50,000 cash prize. Claim immediately",
            "Meeting at 5 PM today",
            "Win free Goa trip. Limited offer. Click now",
            "Don't forget to submit your assignment",
            "Get instant loan at 0'%' interest. Apply now",
            "Send me the notes",
            "Exclusive deal for you. Click now",
            "Meeting postponed to 5 PM",
            "Earn ₹80k/month from home. No experience needed",
            "Happy Birthday! Have a great day",
            "Your OTP is 456789. Do not share",
            "Lowest prices on electronics. Shop now",
            "Are you coming tonight?",
            "Lottery winner! You won ₹10 lakhs",
            "Please review the document",
            "Free entry in contest. Win prizes now",
            "Let's go for a movie this weekend",
            "Limited offer. Buy now",
            "I'll call you later",
            "Double your money in 7 days",
            "Your order has been delivered",
            "Claim free recharge now",
            "Where are you now?",
            "Congratulations! You are selected for reward",
            "Reminder: Appointment at 6 PM",
            "You won ₹5000 gift voucher",
            "Join us for dinner tonight",
            "Buy 1 Get 1 Free. Offer ends soon",
            "Send your address",
            "Pre-approved credit card. Apply now",
            "Good morning. Have a nice day",
            "Click link to claim reward",
            "Can we reschedule meeting?",
            "Bonus waiting. Claim now",
            "Your parcel will arrive tomorrow",
            "Win cash prizes. Participate now",
            "Electricity bill pending. Pay now",
            "Your SIM will be blocked. Update KYC now",
            "Recharge successful",
            "Are you free now?",
            "Bank alert: suspicious activity detected",
            "Call me ASAP",
            "Get job offer. Pay registration fee",
            "Your account will be suspended today"
        ]
                
        })

        csv1 = sample_spam_email_data.to_csv(index=False, header=False).encode('utf-8')
        csv2 = sample_spam_whatsapp_data.to_csv(index=False, header=False).encode('utf-8')
        csv3 = sample_spam_sms_data.to_csv(index=False, header=False).encode('utf-8')

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

        /* 🟢 WhatsApp */
        .whatsapp {
            background: linear-gradient(90deg, #25D366, #128C7E);
            box-shadow: 0 6px 20px rgba(37, 211, 102, 0.5);
            border: 1.5px solid #00ff87; 
                    
        }
        .whatsapp:hover {
            background: linear-gradient(90deg, #128C7E, #075E54);
            box-shadow: 0 12px 30px rgba(18, 140, 126, 0.9);
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

        /* 🔴 SMS */
        .sms {
            background: linear-gradient(90deg, #ff416c, #ff0000);
            box-shadow: 0 6px 20px rgba(255, 65, 108, 0.5);
            border: 1.5px solid #ff416c;
        }
        .sms:hover {
            background: linear-gradient(90deg, #cc2b5e, #753a88);
            box-shadow: 0 12px 30px rgba(255, 65, 108, 0.9);
        }

        </style>
        """, unsafe_allow_html=True)

        # 🔥 Layout
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                create_download_link(csv2, "whatsapp.csv", "⬇️ WhatsApp Dataset", "whatsapp"),
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                create_download_link(csv1, "email.csv", "⬇️ Email Dataset", "email"),
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                create_download_link(csv3, "sms.csv", "⬇️ SMS Dataset", "sms"),
                unsafe_allow_html=True
            )

        col1, col2 = st.columns(2)

        with col1:
            show_btn = st.button("📂 Show History",use_container_width=True)

        with col2:
            if st.button("🗑️ Clear History"):
                clear_spam_history()
                st.success("🗑️ History Cleared!",use_container_width=True)

        if show_btn:
            data = get_all_spam_predictions()

            
            history_df = pd.DataFrame(
                data,
                columns=["ID", "Message", "Prediction", "Confidence"]
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
            <span>🔍 Detect Spam Messages in Seconds</span>
            <span>🤖 Identify Fraud & Suspicious Content</span>
            <span>📊 Get AI-Powered Spam Insights</span>
            <span>🛡️ Protect Yourself from Scam Messages</span>
            <span>📩 Classify Messages Instantly</span>
            <span>🚫 Filter Out Spam & Scams</span>
            <span>🤖 Powered by Machine Learning</span>
            <span>🔐 Stay Safe from Fraud Messages</span>
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
                <h4>📩 Total Messages Scanned</h4>
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
                <h2>92%</h2>
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
                <h4>⚠️ Spam Messages Blocked</h4>
                <h2>10K+</h2>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.logged_in == False:
        login_spam_page()
    else:
        main_spam_app()


