import streamlit as st
import sys
import os

# Add the current directory to the path so we can import from main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import bmi_calculator, comment_on_bmi, stylist

# Page configuration
st.set_page_config(
    page_title="BMI Calculator & Style Advisor",
    page_icon="👗",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .bmi-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .comment-box {
        background: #f8f9fa;
        border-left: 5px solid #FF6B6B;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
    }
    .stylist-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">BMI Calculator & Style Advisor</h1>', unsafe_allow_html=True)
st.markdown("### Get your BMI calculated with sassy commentary and fashion advice!")

# Input section
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Weight")
    weight_unit = st.selectbox(
        "Weight Unit",
        ["kg", "lbs", "stones"],
        index=0,
        help="Select your preferred weight unit"
    )
    
    # Set min/max values based on unit
    if weight_unit == "kg":
        min_weight, max_weight, default_weight, step = 30.0, 300.0, 70.0, 0.5
    elif weight_unit == "lbs":
        min_weight, max_weight, default_weight, step = 66.0, 661.0, 154.0, 1.0
    else:  # stones
        min_weight, max_weight, default_weight, step = 4.7, 47.2, 11.0, 0.1
    
    weight_input = st.number_input(
        f"Weight ({weight_unit})",
        min_value=min_weight,
        max_value=max_weight,
        value=default_weight,
        step=step,
        help=f"Enter your weight in {weight_unit}"
    )

with col2:
    st.markdown("#### Height")
    height_unit = st.selectbox(
        "Height Unit",
        ["cm", "meters", "feet", "inches"],
        index=0,
        help="Select your preferred height unit"
    )
    
    # Set min/max values based on unit
    if height_unit == "cm":
        min_height, max_height, default_height, step = 100.0, 250.0, 170.0, 1.0
    elif height_unit == "meters":
        min_height, max_height, default_height, step = 1.0, 2.5, 1.7, 0.01
    elif height_unit == "feet":
        min_height, max_height, default_height, step = 3.0, 8.0, 5.7, 0.1
    else:  # inches
        min_height, max_height, default_height, step = 39.0, 96.0, 67.0, 1.0
    
    height_input = st.number_input(
        f"Height ({height_unit})",
        min_value=min_height,
        max_value=max_height,
        value=default_height,
        step=step,
        help=f"Enter your height in {height_unit}"
    )

# Calculate button
if st.button("Calculate BMI & Get Advice", type="primary", use_container_width=True):
    if weight_input > 0 and height_input > 0:
        # Format the input for the LLM to convert units and calculate BMI
        user_input = f"My weight is {weight_input}{weight_unit} and my height is {height_input}{height_unit}"
        
        # Let the LLM handle unit conversion and get the BMI calculation call
        with st.spinner("Converting units and calculating BMI..."):
            from main import ask_llm, function_lookup
            response = ask_llm(user_input)
            
            # Parse the LLM response to get the function call
            try:
                func_name, weight_kg, height_m = response.split(" ")
                bmi_value = function_lookup[func_name](float(weight_kg), float(height_m))
            except:
                st.error("Error processing your input. Please try again.")
                st.stop()
        
        # Create three columns for the outputs
        st.markdown("---")
        
        # BMI Display Section
        st.markdown("### 📊 Your BMI Result")
        bmi_category = ""
        if bmi_value < 18.5:
            bmi_category = "Underweight"
            color = "#3498db"
        elif 18.5 <= bmi_value < 25:
            bmi_category = "Normal weight"
            color = "#2ecc71"
        elif 25 <= bmi_value < 30:
            bmi_category = "Overweight"
            color = "#f39c12"
        else:
            bmi_category = "Obese"
            color = "#e74c3c"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="bmi-display">
                <h2 style="margin: 0;">{bmi_value:.1f}</h2>
                <p style="margin: 0.5rem 0; font-size: 1.2rem;">{bmi_category}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # BMI Commentary Section
        st.markdown("### 💬 BMI Commentary")
        with st.spinner("Getting sassy commentary..."):
            try:
                bmi_comment = comment_on_bmi(bmi_value)
                st.markdown(f'<div class="comment-box">{bmi_comment}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error getting BMI commentary: {str(e)}")
        
        # Fashion Advice Section
        st.markdown("### 👗 Fashion Stylist Advice")
        with st.spinner("Getting fashion advice..."):
            try:
                fashion_advice = stylist(bmi_value)
                st.markdown(f'<div class="stylist-box">{fashion_advice}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error getting fashion advice: {str(e)}")
        
    else:
        st.error("Please enter valid weight and height values!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><em>Note: This BMI calculator provides general guidance. Consult healthcare professionals for personalized advice.</em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar with additional info
with st.sidebar:
    st.header("📋 About BMI")
    st.write("""
    **BMI Categories:**
    - **Underweight:** BMI < 18.5
    - **Normal weight:** 18.5 ≤ BMI < 25
    - **Overweight:** 25 ≤ BMI < 30
    - **Obese:** BMI ≥ 30
    
    **How it's calculated:**
    BMI = weight (kg) ÷ height² (m²)
    """)
    
    st.header("📏 Unit Conversions")
    st.write("""
    **Weight Units:**
    - 1 kg = 2.20462 lbs
    - 1 stone = 14 lbs = 6.35 kg
    
    **Height Units:**
    - 1 m = 100 cm = 3.28084 ft = 39.3701 in
    - 1 ft = 12 in
    """)
    
    st.header("⚠️ Important")
    st.write("""
    - BMI is a screening tool, not a diagnostic tool
    - Muscle mass and body composition aren't considered
    - Always consult healthcare professionals for accurate health assessments
    """)
