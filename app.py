import streamlit as st
from logic import calculate_prediction
from datetime import date
import base64
from pathlib import Path
# -----------------------------------
# 1. PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Marriage Predictor",
    page_icon="💍",
    layout="centered"
)

# -----------------------------------
# 2. WEDDING VIBE CUSTOM CSS
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

    .input-container {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #fad0c4;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #b8860b 0%, #d4af37 100%) !important;
        color: white !important;
        font-size: 20px !important;
        height: 60px;
        border-radius: 30px;
        border: none;
        margin-top: 20px;
    }

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
# 3. SESSION STATE LOGIC
# -----------------------------------
for planet in ["venus", "jupiter", "saturn"]:
    if f"{planet}_h" not in st.session_state:
        st.session_state[f"{planet}_h"] = 1

def increment_house(planet):
    st.session_state[f"{planet}_h"] = 1 if st.session_state[f"{planet}_h"] >= 12 else st.session_state[f"{planet}_h"] + 1

# -----------------------------------
# 4. NAVIGATION TABS (Added Guide Tab)
# -----------------------------------
tab_predict, tab_guide, tab_about = st.tabs(["✨ Prediction", "📖 User Guide", "📜 About the Journey"])

with tab_predict:
    st.markdown("<div class='main-title'>✨ Shubh Vivaah ✨</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Find your auspicious marriage timings</div>", unsafe_allow_html=True)

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

    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #800000; font-weight: bold; font-family: Georgia; font-size: 20px; margin-bottom: -10px;'>📅 Select Auspicious Birth Date</p>", unsafe_allow_html=True)
    birth_date = st.date_input("", value=date(1995, 5, 1), format="DD/MM/YYYY")
    st.markdown("</div>", unsafe_allow_html=True)

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

            res_html = (
                f'<div class="result-box">'
                f'<div class="congrats-text">🎊 Congratulations! 🎊</div>'
                f'<p style="color: #555; font-size: 18px; margin-top: 10px;">The stars are aligning for a beautiful union.</p>'
                f'<div style="margin: 25px 0;">'
                f'<span style="color: #800000; font-size: 20px;">Your Auspicious Window:</span><br>'
                f'<span class="result-date">{m1} {start_year}</span> '
                f'<span style="color: #b8860b; font-size: 24px;"> ~ </span> '
                f'<span class="result-date">{m2} {end_year}</span>'
                f'</div>'
                f'<div style="font-family: Georgia, serif; font-size: 16px; color: #800000; border-top: 1px solid #eee; padding-top: 20px; font-style: italic;">'
                f'"May your journey be filled with eternal love and joy."</div></div>'
            )
            st.markdown(res_html, unsafe_allow_html=True)
            st.balloons()
        else:
            st.warning("The divine timing is still unfolding. Try adjusting the planetary houses.")


# --- TAB 2: THE USER GUIDE ---
with tab_guide:
    # 1. Convert your local image to a Base64 string safely
    img_path = "kundali_guide.png"
    img_base64 = ""
    
    if Path(img_path).exists():
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            img_base64 = f"data:image/png;base64,{encoded_string}"
    
    # 2. Render everything inside a single, seamless HTML container
    guide_html = (
        '<div class="result-box" style="text-align: left; background-color: #ffffff; border: 3px double #d4af37; border-radius: 40px; padding: 10px 0;">'
        '<h2 style="color: #800000; font-family: Georgia, serif; text-align: center; margin-bottom: 20px;">📖 How to Find Your Planetary Houses</h2>'
        '<hr style="border-top: 1px solid #eee; margin-bottom: 20px;">'
        
        '<div style="padding: 0 20px;">'
        '<p style="color: #4b5563; font-size: 16px; line-height: 1.6;">'
        'To get an accurate prediction, you need to check your <b>Lagna Kundali</b> (Birth Chart). '
        'Follow these simple steps to find the house numbers for Venus, Jupiter, and Saturn:</p>'
        
        '<h3 style="color: #b8860b; font-family: Georgia, serif; font-size: 20px; margin-top: 20px;">1. Understanding the House Numbers</h3>'
        '<p style="color: #4b5563; font-size: 16px; line-height: 1.6;">'
        'In a traditional North Indian Kundali, the layout positions are fixed. '
        '<b>The top-middle diamond is always the 1st House.</b> From there, move <b>counter-clockwise</b> to count houses 2 through 12, exactly as shown in the reference map below:</p>'
    )

    # Inject the image dynamically if the file exists, otherwise show a friendly warning inside the box
    if img_base64:
        guide_html += (
            f'<div style="text-align: center; margin: 25px 0;">'
            f'<img src="{img_base64}" style="max-width: 100%; max-height: 400px; object-fit: contain; border-radius: 10px; border: 1px solid #fad0c4; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">'
            f'<p style="color: #9ca3af; font-size: 13px; margin-top: 8px; font-style: italic;">Reference Map: North Indian Kundali House Positions (1-12)</p>'
            f'</div>'
        )
    else:
        guide_html += (
            '<div style="background-color: #fff5f5; border: 1px dashed #e53e3e; padding: 15px; text-align: center; border-radius: 10px; margin: 25px 0; color: #c53030;">'
            '⚠️ <b>Image asset missing:</b> Please upload "kundali_guide.png" to your main GitHub folder!</div>'
        )

    guide_html += (
        '<div style="background-color: #fffaf0; border: 1px dashed #b8860b; padding: 15px; text-align: center; border-radius: 10px; margin-bottom: 25px; font-style: italic; color: #800000;">'
        '✨ Tip: Ignore the small numbers printed in the corners of your chart layout—those represent Zodiac Signs (Rashi). '
        'Always count the physical layout diamonds and triangles starting from the top-center as House 1.</div>'
        
        '<h3 style="color: #b8860b; font-family: Georgia, serif; font-size: 20px;">2. Locate Your Key Planets</h3>'
        '<p style="color: #4b5563; font-size: 16px; line-height: 1.6;">Look into the corresponding sections of your personal chart to locate these specific abbreviations:</p>'
        '<ul style="color: #4b5563; line-height: 1.8; font-size: 16px; margin-left: 20px;">'
        '<li><b style="color: #800000;">Venus:</b> Written as <b>Ve</b> or <b>Sk</b> (Sukra)</li>'
        '<li><b style="color: #800000;">Jupiter:</b> Written as <b>Ju</b> or <b>Gu</b> (Guru)</li>'
        '<li><b style="color: #800000;">Saturn:</b> Written as <b>Sa</b> or <b>Sh</b> (Shani)</li>'
        '</ul>'
        '<p style="color: #4b5563; font-size: 16px; line-height: 1.6;">Like in above chart, Venus is in 10th House, Jupiter is in 5th House and Saturn is in 11th House.</p>'
        
        
        '<h3 style="color: #b8860b; font-family: Georgia, serif; font-size: 20px; margin-top: 25px;">3. Set and Reveal</h3>'
        '<p style="color: #4b5563; font-size: 16px; line-height: 1.6;">'
        'Once you note which house number each planet occupies on your chart, switch over to the <b>"✨ Prediction"</b> tab, match the values using the counters, and hit reveal!</p>'
        '</div>'
        
        '</div>'
    )
    
    st.markdown(guide_html, unsafe_allow_html=True)

# --- TAB 3: THE ABOUT PAGE ---
with tab_about:
    about_text = (
        '<div class="result-box" style="text-align: left; background-color: #ffffff; border: 3px double #d4af37;">'
        '<h2 style="color: #800000; font-family: Georgia, serif; text-align: center; margin-bottom: 20px;">📜 The Story of Shubh Vivaah</h2>'
        '<hr style="border-top: 1px solid #eee; margin-bottom: 20px;">'
        '<div style="padding: 0 20px;">'
        '<h3 style="color: #b8860b; font-family: Georgia, serif; font-size: 22px; margin-bottom: 10px;">The Vision</h3>'
        '<p style="color: #4b5563; line-height: 1.6; font-size: 16px;">'
        '<b>Shubh Vivaah</b> blends celestial wisdom with modern technology. Marriage is a sacred milestone, and we believe the stars provide a gentle guide toward that beautiful union.</p>'
        '<h3 style="color: #b8860b; font-family: Georgia, serif; font-size: 22px; margin-top: 25px; margin-bottom: 10px;">The Celestial Pillars</h3>'
        '<p style="color: #4b5563; line-height: 1.6; font-size: 16px;">Our predictive logic focuses on the alignment of three essential planets:</p>'
        '<ul style="color: #4b5563; line-height: 1.8; font-size: 16px; margin-left: 20px;">'
        '<li><b style="color: #800000;">Venus:</b> The eternal planet of love, beauty, and harmony.</li>'
        '<li><b style="color: #800000;">Jupiter:</b> The bringer of wisdom, growth, and divine blessings.</li>'
        '<li><b style="color: #800000;">Saturn:</b> The symbol of commitment, time, and lasting bonds.</li>'
        '</ul>'
        '<h3 style="color: #b8860b; font-family: Georgia, serif; font-size: 22px; margin-top: 25px; margin-bottom: 10px;">A Message for You</h3>'
        '<p style="color: #4b5563; line-height: 1.6; font-style: italic; font-size: 16px;">'
        'While the stars provide a map, you are the traveler. The best time for marriage is when two hearts feel truly at home with one another.</p>'
        '</div>'
        '<div style="margin-top: 40px; padding-top: 20px; border-top: 1px dashed #d1d5db; text-align: center;">'
        '<p style="color: #800000; font-weight: bold; font-family: Georgia, serif; font-size: 18px;">Made with ❤️ for your beautiful future</p>'
        '</div>'
        '</div>'
    )
    st.markdown(about_text, unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align: center; color: #9ca3af; font-size: 12px;">'
            '<p>© 2026 Shubh Vivaah Predictor | Vikash Kumar.</p></div>', 
            unsafe_allow_html=True)