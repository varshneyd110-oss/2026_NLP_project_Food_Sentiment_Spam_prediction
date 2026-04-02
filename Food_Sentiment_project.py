import streamlit as st
import streamlit.components.v1 as components
import joblib
import re
import pandas as pd
import numpy as np
import plotly.express as px
from Database import save_prediction, get_all_predictions, create_table, clear_history

create_table()



def  mycleaning(doc):
            return re.sub("[^a-zA-Z ]","",doc).lower()

if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

if "active_page" not in st.session_state:
    st.session_state.active_page = None


def run_sentiment_app():
    
    def login_sentiment_page():

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

        
        # 🎨 Banner
        st.markdown("""
            <div style="
                background: linear-gradient(90deg, #00c6ff, #0072ff);
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 30px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            ">
                <h1 style="
                    color: white;
                    font-size: 35px;
                    margin-bottom: 10px;
                ">
                    🍽️ Food Sentiment Analyzer
                </h1>
                <p style="
                    color: #e0e0e0;
                    font-size: 18px;
                ">
                    Understand customer emotions using AI 🤖
                </p>
            </div>
        """, unsafe_allow_html=True)

        # 🔐 Login Box
        st.markdown("## 🔐 Login to Continue")

        # 🔐 Login inputs
        st.write("\n")
        st.write("### 👤 Enter Username")
        username = st.text_input("",placeholder="please type User Name ......")
        st.write("### 🔑 Enter Password")
        password = st.text_input("", type="password",placeholder="please type Password ......")

        # 🍽️ Restaurant dictionary
        restaurants = {
            "Crimson Crown Dining": "CC@Royal",
            "The Velvet Ember": "VE#Luxury",
            "Golden Orchid Palace": "GO@Elite",
            "Sapphire Feast House": "SF#Fine",
            "The Imperial Platter": "IP@King",
            "Royal Spice Symphony": "RS#Chef",
            "The Grand Saffron Table": "GS@Royal",
            "Opulent Flame Bistro": "OF#Fire",
            "Silver Crest Kitchen": "SC@Elite",
            "Emerald Royal Dine": "ER#Green",
            "The Regal Spoon": "RS@Queen",
            "Aurora Palace Kitchen": "AP#Sky",
            "The Luxe Ember Table": "LE@VIP",
            "Majestic Fork Lounge": "MF#Elite",
            "The Noble Feast House": "NF@Royal",
            "Golden Crown Bistro": "GC#King",
            "The Velvet Royale": "VR@Luxury",
            "Crystal Palace Dining": "CP#Fine",
            "Imperial Orchid Table": "IO@King",
            "The Grand Velvet Bite": "GV#Luxury",
            "Saffron Majesty Kitchen": "SM@Royal",
            "Royal Ember Court": "RE#Fire",
            "The Opal Crown Dine": "OC@Elite",
            "Silver Royal Symphony": "SR#Class",
            "The Regal Orchid": "RO@Queen",
            "Aurora Luxe Dining": "AL#Sky",
            "The Golden Majesty": "GM@Royal",
            "Emerald Crown Feast": "EC#Green",
            "Imperial Velvet Kitchen": "IV@King",
            "The Crystal Royal Bite": "CR#Fine",
            "Noble Saffron Table": "NS@Royal",
            "The Luxe Crown House": "LC#VIP",
            "Grand Imperial Feast": "GI@King",
            "Royal Opulent Spoon": "RO#Elite",
            "The Velvet Spice Court": "VS@Luxury",
            "Golden Ember Palace": "GE#Fire",
            "The Regal Sapphire": "RS@Queen",
            "Silver Luxe Bistro": "SL#Class",
            "The Royal Orchid Table": "RO@Royal",
            "Imperial Flame Feast": "IF#Fire",
            "The Grand Emerald Bite": "GE#Green",
            "Aurora Crown Kitchen": "AC#Sky",
            "The Velvet Majesty": "VM@Luxury",
            "Crystal Luxe Dining": "CL#Fine",
            "The Noble Orchid Feast": "NO@Royal",
            "Golden Regal Table": "GR#King",
            "The Opulent Sapphire": "OS@Elite",
            "Royal Grand Bistro": "RG#Royal",
            "The Luxe Imperial Spoon": "LI@VIP",
            "Emerald Velvet Feast": "EV#Green",
            "The Crown Symphony Kitchen": "CS@Royal",
            "Silver Imperial Table": "SI#Class",
            "The Grand Orchid Palace": "GO@Royal",
            "Majestic Crystal Feast": "MC#Fine",
            "The Regal Flame Dining": "RF@Fire"
        }


        # 🔘 Buttons side by side
        col1, col2 = st.columns(2)

        # 1️⃣ Login Button
        with col1:
            if st.button("Login",use_container_width=True):
                if username in restaurants and password == restaurants[username]:
                    st.session_state.logged_in = True
                    st.session_state.active_page = "sentiment"
                    st.session_state.user = username
                    st.success(f"Welcome {username} 🎉")
                    st.rerun()
                else:
                    st.error("Wrong Username/Password ❌")

        # 2️⃣ Get Credentials Button
        with col2:
            if st.button("📱 Get Credentials",use_container_width=True):
                st.session_state.show_dropdown = True

        # 🔽 STEP 2 → Dropdown open
        if st.session_state.get("show_dropdown", False):

            selected = st.selectbox("🍴 Select Restaurant", list(restaurants.keys()))

        
            import qrcode
            from io import BytesIO

            if st.button("Generate QR",use_container_width=True):

                data = f"Username: {selected}\nPassword: {restaurants[selected]}"

                qr = qrcode.make(data)

                # 👉 Convert to bytes (IMPORTANT FIX)
                buf = BytesIO()
                qr.save(buf, format="PNG")
                buf.seek(0)

                st.image(buf, caption="📱 Scan to get credentials", width=200)

                
                
        st.markdown("""
        <style>
        @keyframes fadeText {
            0% {opacity: 0;}
            10% {opacity: 1;}
            25% {opacity: 1;}
            35% {opacity: 0;}
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
        }

        .text-container span {
            position: absolute;
            width: 100%;
            opacity: 0;
            animation: fadeText 8s infinite;
        }

        .text-container span:nth-child(1) { animation-delay: 0s; }
        .text-container span:nth-child(2) { animation-delay: 2s; }
        .text-container span:nth-child(3) { animation-delay: 4s; }
        .text-container span:nth-child(4) { animation-delay: 6s; }
        </style>

        <div class="text-container">
            <span>🔍 Analyze Reviews in Seconds</span>
            <span>🤖 Understand Customer Emotions</span>
            <span>📊 Get AI-Powered Insights</span>
            <span>🚀 Grow Your Restaurant Smartly</span>
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
                <h4>📊 Reviews Analyzed</h4>
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
                <h4>🎯 Accuracy</h4>
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
                <h4>🍴 Restaurants</h4>
                <h2>50+</h2>
            </div>
            """, unsafe_allow_html=True)
                
        

    def main_sentiment_app():

        st.sidebar.markdown("""
        <style>
        div.stButton > button {
            display: block;
            margin: 0 auto;
        }
        </style>
    """, unsafe_allow_html=True)


        # ✅ Logout sabse upar
        if st.sidebar.button("Logout",use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        
        # ✅ Default value set (first time only)
        if "theme" not in st.session_state:
            st.session_state.theme = True   # 👈 True = Dark Mode default

        # Toggle (linked with session state)
        theme = st.toggle("🌙 Dark Mode", value=st.session_state.theme,key="main_sentiment_toggle")

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
        
            
        st.write("Welcome to Food Sentiment Analysis 🍽️")

        # 👉 Yaha se tumhara pura code paste karo

        

        model=joblib.load("sentiment_model.pkl")

        import streamlit.components.v1 as components
        import base64

        def get_base64_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()

        img_base64 = get_base64_image("Food.jpg")

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
                                <div class="title">📩 Food Sentiment Analysis</div>
                                <div class="subtitle">📈 Improve Restaurant Experience with AI</div>
                                <div id="clock"></div>
                            </div>

                            <div class="slide">
                                <div class="title">📩 Food Sentiment Analysis</div>
                                <div class="subtitle">💬 Real-time Customer Feedback Analysis</div>
                                <div id="clock2"></div>
                            </div>

                            <!-- DUPLICATE (same content again) -->
                            <div class="slide">
                                <div class="title">📩 Food Sentiment Analysis</div>
                                <div class="subtitle">📈 Improve Restaurant Experience with AI</div>
                                <div id="clock3"></div>
                            </div>

                            <div class="slide">
                                <div class="title">📩 Food Sentiment Analysis</div>
                                <div class="subtitle">💬 Real-time Customer Feedback Analysis</div>
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



        
        st.markdown("""
        <style>

        /* 🎯 Predict Button Styling */
        div.stButton > button {
            background: linear-gradient(90deg, #ff8008, #ffc837);
            color: white;
            font-size: 30px;
            font-weight: bold;
            padding: 18px 50px;           
            border-radius: 14px;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 6px 18px rgba(40, 167, 69, 0.4);
            width: auto;
            margin-top: 20px;
        }

        /* 🔥 Hover Effect */
        div.stButton > button:hover {
            transform: translateY(-2px) scale(1.03);
            background: linear-gradient(90deg, #218838, #4cd137);
            box-shadow: 0 10px 25px rgba(40, 167, 69, 0.6);
        }

        /* Click Effect */
        div.stButton > button:active {
            transform: scale(0.98);
        }

        </style>
        """, unsafe_allow_html=True)



        st.write("\n")
        st.markdown("""
        <h2 style="
            background: linear-gradient(90deg, #28a745, #5cd65c);
            -webkit-background-clip: text;
            letter-spacing: 1px;
            font-weight: bold;
            -webkit-text-fill-color: transparent;">
            🌿 Predict Single Review 
        </h2>
        """, unsafe_allow_html=True)
        sample=st.text_input("",placeholder="type something cool ......")

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            if st.button("Predict",use_container_width=True):

                pred = model.predict([sample])
                prob = model.predict_proba([sample])

                # 🎯 Sentiment decide karo
                if pred[0] == 0:
                    sentiment = "👎 Negative Review"
                    confidence = prob[0][0]
                else:
                    sentiment = "👍 Positive Review"
                    confidence = prob[0][1]

                # 🔥 SAVE TO DATABASE
                save_prediction(sample, sentiment, confidence)

                # 🎨 UI Display (SIRF EK BAAR)
                if pred[0] == 0:
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
                            👎 <b>Negative Review</b><br><br>
                            Confidence Score: <b>{confidence:.2f}</b>
                        </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(90deg, #28a745, #5cd65c);
                            padding: 20px;
                            border-radius: 15px;
                            text-align: center;
                            color: white;
                            font-size: 20px;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                        ">
                            👍 <b>Positive Review</b><br><br>
                            Confidence Score: <b>{confidence:.2f}</b>
                        </div>
                    """, unsafe_allow_html=True)

                    st.balloons()
                    st.snow()


        st.markdown("""
        <h2 style="
            background: linear-gradient(90deg, #28a745, #5cd65c);
            -webkit-background-clip: text;
            letter-spacing: 1px;
            font-weight: bold;
            -webkit-text-fill-color: transparent;">
            🌿 Predict Bulk Review
        </h2>
        """, unsafe_allow_html=True)
        file=st.file_uploader("select file",type=["csv","txt"])
        if file:
            df=pd.read_csv(file,names=["Review"])
            placeholder=st.empty()
            placeholder.dataframe(df)
            

        st.markdown("""
            <style>
            div.stTextInput > div > div > input {
                background: rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                border: 1px solid rgba(255,255,255,0.3);
                color: white;
                padding: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            # Button
            if st.button("Predict",key="b2",use_container_width=True):
                corpus=df.Review
                pred=model.predict(corpus)
                prob=np.max(model.predict_proba(corpus),axis=1)
                df["Sentiment"]=pred
                df["Confidence"]=prob
                df["Sentiment"]=df["Sentiment"].map({0:"👎Negative Review",1:"👍Positive Review"})
                placeholder.dataframe(df)

                # 🔥 SAVE BULK DATA TO DATABASE
                for i in range(len(df)):
                    save_prediction(
                        df["Review"][i],
                        df["Sentiment"][i],
                        df["Confidence"][i]
                    )

                # 📊 Summary calculation
                positive_count = (df["Sentiment"] == "👍Positive Review").sum()
                negative_count = (df["Sentiment"] == "👎Negative Review").sum()

                # 🎉 Attractive Result Card
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        label="👍 Positive Reviews",
                        value=positive_count
                    )

                with col2:
                    st.metric(
                        label="👎 Negative Reviews",
                        value=negative_count
                    )
                
                with col3:
                    st.metric(
                        label="📊 Total Reviews",
                        value=negative_count + positive_count
                    )
                st.success("🎉 Bulk Prediction Completed!")
                st.markdown("""
                    ### 💬 Insight
                    Turning customer feedback into powerful insights!
                    """)
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
                    "Sentiment": ["Positive", "Negative"],
                    "Count": [positive_count, negative_count]
                }

                fig = px.pie(
                    values=data["Count"],
                    names=data["Sentiment"],
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
        sample_data = pd.DataFrame({
            "review": [
                "Food was amazing and delicious",
                "Worst service ever",
                "Loved the ambiance",
                "Not worth the money",
                "Highly recommended place",
                "Very bad experience",
                "Loved this place.",
                "Crust is not good.",
                "Not tasty and the texture was just nasty.",
                "The selection on the menu was great and so were the prices.",
                "Now I am getting angry and I want my damn pho.",
                "The fries were great too.",
                "A great touch.",
                "Service was very prompt.",
                "Would not go back.",
                "I was disgusted because I was pretty sure that was human hair.",
                "Highly recommended.",
                "Waitress was a little slow in service.",
                "did not like at all.",
                "The food, amazing.",
                "Service is also cute.",
                "They never brought a salad we asked for.",
            ]
        })

        csv = sample_data.to_csv(index=False, header=False).encode('utf-8')

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

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            st.download_button(
                label="⬇️ Download Sample Dataset",
                data=csv,
                file_name="sample_reviews.csv",
                mime="text/csv"
            )
        
        st.markdown("""
        <style>
        div.stDownloadButton > button {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 25px;
            border-radius: 12px;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 6px 18px rgba(0, 114, 255, 0.4);
            width: 100%;
            margin-top: 40px;
            
        }

        /* Hover Effect 🔥 */
        div.stDownloadButton > button:hover {
            transform: translateY(-2px) scale(1.03);
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            box-shadow: 0 10px 25px rgba(0, 114, 255, 0.6);
        }

        /* Click Effect */
        div.stDownloadButton > button:active {
            transform: scale(0.98);
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            show_btn = st.button("📂 Show History",use_container_width=True)

        with col2:
            if st.button("🗑️ Clear History",use_container_width=True):
                clear_history()
                st.success("🗑️ History Cleared!")

        if show_btn:
            data = get_all_predictions()

            
            history_df = pd.DataFrame(
                data,
                columns=["ID", "Review", "Sentiment", "Confidence"]
            )

            st.dataframe(history_df)


        

        st.markdown("""
        <style>

        /* 🎯 All Buttons Styling */
        div.stButton > button {
            background: linear-gradient(90deg, #ff8008, #ffc837);
            color: white;
            font-size: 40px;
            font-weight: bold;
            padding: 18px 50px;
            border-radius: 12px;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 6px 18px rgba(0, 114, 255, 0.4);
            width: 100%;
            margin-top: 20px;
        }

        /* 🔥 Hover Effect */
        div.stButton > button:hover {
            transform: translateY(-2px) scale(1.03);
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            box-shadow: 0 10px 25px rgba(0, 114, 255, 0.6);
            font-size: 50px;
            font-weight: bold;
            padding: 20px 55px;
        }

        /* Click Effect */
        div.stButton > button:active {
            transform: scale(0.98);
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


        st.markdown("""
        <style>
        @keyframes fadeText {
            0% {opacity: 0;}
            10% {opacity: 1;}
            25% {opacity: 1;}
            35% {opacity: 0;}
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
        }

        .text-container span {
            position: absolute;
            width: 100%;
            opacity: 0;
            animation: fadeText 8s infinite;
        }

        .text-container span:nth-child(1) { animation-delay: 0s; }
        .text-container span:nth-child(2) { animation-delay: 2s; }
        .text-container span:nth-child(3) { animation-delay: 4s; }
        .text-container span:nth-child(4) { animation-delay: 6s; }
        </style>

        <div class="text-container">
            <span>🔍 Analyze Reviews in Seconds</span>
            <span>🤖 Understand Customer Emotions</span>
            <span>📊 Get AI-Powered Insights</span>
            <span>🚀 Grow Your Restaurant Smartly</span>
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
                <h4>📊 Reviews Analyzed</h4>
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
                <h4>🎯 Accuracy</h4>
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
                <h4>🍴 Restaurants</h4>
                <h2>50+</h2>
            </div>
            """, unsafe_allow_html=True)

        
        

    if st.session_state.logged_in == False:
        login_sentiment_page()
    else:
        main_sentiment_app()

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

        /* Button base */
        div.stButton > button {
            background: linear-gradient(90deg, #ff7e00, #ffb347);
            background-size: 200% 200%;
            color: white;
            border-radius: 30px;
            padding: 18px 50px;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 6px 18px rgba(255, 128, 8, 0.4);
            width: 100%;
            margin-top: 20px;
        }

        /* 🎯 IMPORTANT: text ko target karo */
        div.stButton > button p {
            font-size: 40px !important;
            font-weight: bold;
        }

        /* Hover */
        div.stButton > button:hover {
            background-position: right center;
            box-shadow: 0 12px 30px rgba(0, 114, 255, 0.8);
            transform: translateY(-3px) scale(1.05);
            background: linear-gradient(90deg, #005bea, #003d99);
        }

        /* Hover text */
        div.stButton > button:hover p {
            font-size: 45px !important;
        }

        </style>
        """, unsafe_allow_html=True)

    def run_sentiment_app():
        import streamlit as st
        import joblib

        model = joblib.load("sentiment_model.pkl")

        st.markdown("## 😊 Sentiment Analysis")

        review = st.text_area("Enter review", key="sent_text")

        if st.button("Analyze"):
            if review.strip() == "":
                st.warning("Enter review")
            else:
                result = model.predict([review])[0]

                if result == 1:
                    st.success("😊 Positive")
                else:
                    st.error("😞 Negative")











        

