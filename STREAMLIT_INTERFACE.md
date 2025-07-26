# Streamlit BMI Calculator Interface

This document contains the complete Streamlit interface code for your BMI calculator application.

## 📁 File: `ui.py`

```python
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
    weight = st.number_input(
        "Weight (kg)",
        min_value=30.0,
        max_value=300.0,
        value=70.0,
        step=0.5,
        help="Enter your weight in kilograms"
    )

with col2:
    height = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=250.0,
        value=170.0,
        step=1.0,
        help="Enter your height in centimeters"
    )

# Convert height from cm to meters
height_m = height / 100

# Calculate button
if st.button("Calculate BMI & Get Advice", type="primary", use_container_width=True):
    if weight > 0 and height > 0:
        # Calculate BMI
        bmi_value = bmi_calculator(weight, height_m)
        
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
    
    st.header("⚠️ Important")
    st.write("""
    - BMI is a screening tool, not a diagnostic tool
    - Muscle mass and body composition aren't considered
    - Always consult healthcare professionals for accurate health assessments
    """)
```

## 🚀 **Installation & Setup**

### 1. Install Streamlit
```bash
pip install streamlit
```

### 2. Run the Application
```bash
streamlit run ui.py
```

### 3. Access the Interface
Open your browser to: `http://localhost:8501`

## 📋 **Features Overview**

| Feature | Description |
|---------|-------------|
| **Inputs** | Weight (kg) and Height (cm) with validation |
| **BMI Display** | Shows calculated BMI value and category |
| **Commentary** | Sassy BMI commentary from your model |
| **Fashion Advice** | Stylist recommendations based on BMI |
| **Styling** | Custom CSS with gradient backgrounds and color-coded categories |
| **Responsive** | Works on desktop and mobile |
| **Error Handling** | Graceful handling of API failures |
| **Sidebar** | Educational content about BMI |

## 🎯 **Usage**
1. Enter your weight in kilograms
2. Enter your height in centimeters
3. Click "Calculate BMI & Get Advice"
4. View your results in three separate, clearly styled sections

## 🔧 **Dependencies**
- `streamlit`
- Your existing `main.py` functions: `bmi_calculator`, `comment_on_bmi`, `stylist`

## 📱 **Mobile Support**
The interface is fully responsive and works great on mobile devices with touch-friendly inputs and readable text sizes. 