import streamlit as st
from logic import calculate_prediction
from datetime import date

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Marriage Predictor",
    page_icon="💍",
    layout="centered"
)

# -----------------------------------
# WEDDING VIBE CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #fffaf0; 
    }

    .main-title { 
        text-align: center; 
        font-size: 52px; 
        font-family: 'Georgia', serif;
        font-weight: bold; 
        color: #800000; 
        margin-bottom: 5px;
    }
    
    .subtitle { 
        text-align: center; 
        font-size: 20px; 
        font-family: 'Arial', sans-serif;
        font-style: italic;
        margin-bottom: 40px; 
        color: #b8860b; 
    }
    
    /* PINK WEDDING TILES */
    .planet-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%); 
        padding: 30px;
        border-radius: 50% 50% 10px 10px; 
        text-align: center;
        border: 3px solid #d4af37; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    
    .planet-name { 
        font-size: 22px; 
        font-weight: bold; 
        color: #800000; 
    }
    
    .house-number { 
        font-size: 58px; 
        font-weight: 900; 
        color: #ffffff; 
        text-shadow: 2px 2px 4px rgba(128, 0, 0, 0.3);
    }

    /* PEARL GRAY BUTTONS */
    div.stButton > button {
        background-color: #e5e7eb !important; 
        color: #374151 !important;
        border-radius: 20px;
        border: 1px solid #d1d5db;
        padding: 8px 15px;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 12px;
    }
    
    div.stButton > button:hover {
        background-color: #d1d5db !important;
        border-color: #b8860b;
    }

    /* ENHANCED DATE SECTION */
    .input-container {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #fad0c4;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }

    /* THE REVEAL BUTTON */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #b8860b 0%, #d4af37 100%) !important;
        color: white !important;
        font-size: 20px !important;
        height: 60px;
        border-radius: 30px;
        border: none;
        margin-top: 20px;
    }

    /* RESULT SECTION */
    .result-box {
        padding: 40px;
        border-radius: 40px;
        background-color: #ffffff;
        text-align: center;
        margin-top: 30px;
        border: 5px double #d4af37;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    .congrats-text { font-size: 26px; font-family: 'Georgia', serif; color: #800000; font-weight: bold; }
    .result-date { font-size: 38px; font-weight: 800; color: #d4af37; font-family: 'Georgia', serif; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SESSION STATE
# -----------------------------------
for planet in ["venus", "jupiter", "saturn"]:
    if f"{planet}_h" not in st.session_state:
        st.session_state[f"{planet}_h"] = 1

def increment_house(planet):
    st.session_state[f"{planet}_h"] = 1 if st.session_state[f"{planet}_h"] >= 12 else st.session_state[f"{planet}_h"] + 1

# -----------------------------------
# HEADER
# -----------------------------------
st.markdown("<div class='main-title'>✨ Shubh Vivaah ✨</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Find your auspicious marriage timings</div>", unsafe_allow_html=True)

# -----------------------------------
# BRIDAL PINK TILES
# -----------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='planet-card'><div class='planet-name'>Venus</div><div class='house-number'>{st.session_state.venus_h}</div></div>", unsafe_allow_html=True)
    if st.button("Next House", key="btn_v", use_container_width=True):
        increment_house("venus")
        st.rerun()

with col2:
    st.markdown(f"<div class='planet-card'><div class='planet-name'>Jupiter</div><div class='house-number'>{st.session_state.jupiter_h}</div></div>", unsafe_allow_html=True)
    if st.button("Next House", key="btn_j", use_container_width=True):
        increment_house("jupiter")
        st.rerun()

with col3:
    st.markdown(f"<div class='planet-card'><div class='planet-name'>Saturn</div><div class='house-number'>{st.session_state.saturn_h}</div></div>", unsafe_allow_html=True)
    if st.button("Next House", key="btn_s", use_container_width=True):
        increment_house("saturn")
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------
# ENHANCED BIRTH DETAIL SECTION
# -----------------------------------
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
st.markdown("<p style='color: #800000; font-weight: bold; font-family: Georgia; font-size: 20px; margin-bottom: -10px;'>📅 Select Auspicious Birth Date</p>", unsafe_allow_html=True)
birth_date = st.date_input(
    "", 
    value=date(1995, 5, 1),
    format="DD/MM/YYYY"  # This fixes the display format
)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------
# PREDICTION
# -----------------------------------
if st.button("✨ Reveal Auspicious Muhurat", use_container_width=True, type="primary"):
    data = calculate_prediction(
        st.session_state.venus_h,
        st.session_state.jupiter_h,
        st.session_state.saturn_h,
        birth_date.month,
        birth_date.year
    )

    passing_result = next((r for r in data["future_results"] if not r.get("eliminated")), None)

    if passing_result:
        start_month, start_year = map(int, passing_result["date"].split("-"))
        end_month, end_year = start_month + 1, start_year + 1
        
        if end_month > 12:
            end_month, end_year = 1, end_year + 1

        m1 = date(2000, start_month, 1).strftime('%B')
        m2 = date(2000, 1 if end_month > 12 else end_month, 1).strftime('%B')

        st.markdown(
            f"""
            <div class="result-box">
                <div class="congrats-text">🎊 Congratulations! 🎊</div>
                <p style="color: #555; font-size: 18px; margin-top: 10px;">The stars are aligning for a beautiful union.</p>
                <div style="margin: 25px 0;">
                    <span style="color: #800000; font-size: 20px;">Your Auspicious Window:</span><br>
                    <span class="result-date">{m1} {start_year}</span> 
                    <span style="color: #b8860b; font-size: 24px;"> ~ </span> 
                    <span class="result-date">{m2} {end_year}</span>
                </div>
                <div style="font-family: 'Georgia', serif; font-size: 16px; color: #800000; border-top: 1px solid #eee; padding-top: 20px; font-style: italic;">
                    "May your journey be filled with eternal love and joy."
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.balloons()
    else:
        st.warning("The divine timing is still unfolding. Try adjusting the planetary houses.")

# -----------------------------------
# FOOTER / COPYRIGHT
# -----------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #9ca3af; font-size: 12px; font-family: 'Arial', sans-serif;">
        <p>© 2026 Shubh Vivaah Predictor. All Rights Reserved.</p>
        <p><i>Disclaimer: This application is based on traditional calculations and it is not always true. 
        Life's journey is shaped by many stars; always follow your heart.</i></p>
    </div>
    """,
    unsafe_allow_html=True
)