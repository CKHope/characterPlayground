import streamlit as st
import json
import os

# Constants for default values
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "user_input": "",
    "grid_size": 200,
    "text_color": "#000000",
    "font_family": "FangSong",
    "font_weight": "normal",
    "unique_option": "Unique Characters Only",
    "border_thickness": "0.5px",
    "border_color": "#ffbebe",
    "grid_style": "Rice Grid (米字格)"
}

# Persistence functions
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                # Merge with defaults for safety
                return {**DEFAULT_SETTINGS, **saved}
        except:
            pass
    return DEFAULT_SETTINGS

def save_settings():
    settings = {
        "user_input": st.session_state.get("user_input", ""),
        "grid_size": st.session_state.get("grid_size", 200),
        "text_color": st.session_state.get("text_color", "#000000"),
        "font_family": st.session_state.get("font_family", "FangSong"),
        "font_weight": st.session_state.get("font_weight", "normal"),
        "unique_option": st.session_state.get("unique_option", "Unique Characters Only"),
        "border_thickness": st.session_state.get("border_thickness", "0.5px"),
        "border_color": st.session_state.get("border_color", "#ffbebe"),
        "grid_style": st.session_state.get("grid_style", "Rice Grid (米字格)")
    }
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

# Initialize session state from file
if "settings_loaded" not in st.session_state:
    saved_settings = load_settings()
    for key, value in saved_settings.items():
        st.session_state[key] = value
    st.session_state["settings_loaded"] = True

# Function to generate CSS styles
def generate_css(grid_size, font_size, font_weight, text_color, font_family, border_thickness, border_color, grid_style):
    
    # Grid background lines based on style
    rice_grid_css = ""
    if grid_style == "Rice Grid (米字格)":
        rice_grid_css = f"""
        background-image: 
            linear-gradient(to bottom, transparent 49.5%, {border_color} 49.5%, {border_color} 50.5%, transparent 50.5%),
            linear-gradient(to right, transparent 49.5%, {border_color} 49.5%, {border_color} 50.5%, transparent 50.5%),
            linear-gradient(to top right, transparent 49.7%, {border_color} 49.7%, {border_color} 50.3%, transparent 50.3%),
            linear-gradient(to bottom right, transparent 49.7%, {border_color} 49.7%, {border_color} 50.3%, transparent 50.3%);
        """
    elif grid_style == "Field Grid (田字格)":
        rice_grid_css = f"""
        background-image: 
            linear-gradient(to bottom, transparent 49.5%, {border_color} 49.5%, {border_color} 50.5%, transparent 50.5%),
            linear-gradient(to right, transparent 49.5%, {border_color} 49.5%, {border_color} 50.5%, transparent 50.5%);
        """
    
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap');
    
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax({grid_size}px, 1fr));
        gap: 10px;
        justify-items: center;
        align-items: center;
    }}
    
    .grid-item {{
        width: {grid_size}px;
        height: {grid_size}px;
        border: 1px solid rgb(0, 0, 0);
        background-color: #ffffff;
        position: relative;
        {rice_grid_css}
    }}
    
    .grid-item .character {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: {font_size}px;
        font-weight: {font_weight};
        color: {text_color};
        font-family: {font_family}, 'Noto Sans SC', sans-serif;
        z-index: 2;
    }}
    
    /* 9-Square Grid Specific */
    .nine-square-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
    }}
    
    .sub-item {{
        border: {border_thickness} solid {border_color};
    }}
    </style>
    """

# Function to validate border thickness input
def validate_border_thickness(thickness):
    try:
        if not thickness.endswith("px"):
            thickness += "px"
        float(thickness.replace("px", ""))
    except ValueError:
        st.error("Invalid border thickness! Please enter a valid number followed by 'px'.")
        return DEFAULT_SETTINGS["border_thickness"]
    return thickness

# App title
st.title("Chinese Text Grid with Adjustable Settings")

# Step 1: Input Chinese text
user_input = st.text_area("Enter Chinese text:", key="user_input", on_change=save_settings, height=100, placeholder="输入中文文本...")

# Step 2: Grid Type selection
grid_style = st.selectbox(
    "Select Grid Style:",
    options=["Rice Grid (米字格)", "Field Grid (田字格)", "9-Square Grid (井字格)", "Empty Grid"],
    key="grid_style",
    on_change=save_settings
)

# Step 3: Grid size slider
grid_size = st.selectbox(
    "Select Grid Item Size (px):",
    options=[50, 100, 150, 200, 250, 300],
    key="grid_size",
    on_change=save_settings
)

# Step 4: Font size calculation
font_size = int((grid_size * 45) / 50)

# Step 5: Text color
text_color = st.color_picker("Text Color:", key="text_color", on_change=save_settings)

# Step 6: Font family
font_family = st.selectbox(
    "Font Style:",
    options=["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "SimHei", "KaiTi", "FangSong", "LiSu", "TW-MOE-Li", "HanWangLiSuMedium"],
    key="font_family",
    on_change=save_settings
)

# Step 7: Font weight
font_weight = st.selectbox(
    "Font Weight:",
    options=["normal", "bold", "lighter", "bolder", "100", "200", "300", "400", "500", "600", "700", "800", "900"],
    key="font_weight",
    on_change=save_settings
)

# Step 8: Display options
unique_option = st.radio(
    "Display Options:",
    options=["All Characters", "Unique Characters Only"],
    key="unique_option",
    on_change=save_settings
)

# Step 9: Border settings
col1, col2 = st.columns(2)
with col1:
    border_thickness = st.text_input("Border Thickness (px):", key="border_thickness", on_change=save_settings)
    border_thickness = validate_border_thickness(border_thickness)
with col2:
    border_color = st.color_picker("Border Color:", key="border_color", on_change=save_settings)

# Render results
if user_input:
    # Character list based on selection
    all_chars = [char for char in user_input if not char.isspace()]
    if unique_option == "Unique Characters Only":
        seen = set()
        characters = [char for char in all_chars if not (char in seen or seen.add(char))]
    else:
        characters = all_chars

    # Statistics Section
    st.subheader("Character Statistics")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Total Characters", len(all_chars))
    with col_stat2:
        st.metric("Unique Characters", len(set(all_chars)))
    
    st.divider()

    
    css_styles = generate_css(grid_size, font_size, font_weight, text_color, font_family, border_thickness, border_color, grid_style)
    st.markdown(css_styles, unsafe_allow_html=True)
    
    grid_html = '<div class="grid-container">'
    for char in characters:
        if grid_style == "9-Square Grid (井字格)":
            grid_html += '<div class="grid-item nine-square-grid">'
            for _ in range(9):
                grid_html += '<div class="sub-item"></div>'
        else:
            grid_html += '<div class="grid-item">'
        
        grid_html += f'<span class="character">{char}</span>'
        grid_html += '</div>'
    grid_html += '</div>'
    
    st.markdown(grid_html, unsafe_allow_html=True)

