import streamlit as st

# Constants for default values
DEFAULT_TEXT_COLOR = "#000000"
DEFAULT_BORDER_COLOR = "#ffbebe"
DEFAULT_BORDER_THICKNESS = "0.5px"
DEFAULT_FONT_FAMILY = "FangSong"
DEFAULT_GRID_SIZE = 200
DEFAULT_FONT_WEIGHT = "lighter"
DEFAULT_UNIQUE_OPTION = "Unique Characters Only"

# Function to generate CSS styles
def generate_css(grid_size, font_size, font_weight, text_color, font_family, border_thickness, border_color):
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap'); /* For fallback Chinese fonts */
    
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
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* Divide into 3x3 squares */
        grid-template-rows: repeat(3, 1fr);
        border: 1px solid rgb(0, 0, 0); /* Black border */
        background-color: #f9f9f9; /* Light grey background */
        position: relative; /* For centering the character */
    }}
    
    .grid-item .character {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: {font_size}px; /* Dynamic font size */
        font-weight: {font_weight}; /* Dynamic font weight */
        color: {text_color}; /* Dynamic text color */
        font-family: {font_family}, 'Noto Sans SC', sans-serif; /* Dynamic font family */
    }}
    
    .grid-item .sub-item {{
        border: {border_thickness} solid {border_color}; /* Dynamic border thickness and color */
    }}
    </style>
    """

# Function to validate border thickness input
def validate_border_thickness(thickness):
    try:
        if not thickness.endswith("px"):
            thickness += "px"
        float(thickness.replace("px", ""))  # Check if it's a valid number
    except ValueError:
        st.error("Invalid border thickness! Please enter a valid number followed by 'px' (e.g., '0.5px').")
        return DEFAULT_BORDER_THICKNESS  # Fallback to default
    return thickness

# App title
st.title("Chinese Text Grid with Adjustable Grid Item and Font Size")

# Step 1: Input Chinese text from the user
user_input = st.text_area("Enter Chinese text:", height=100, placeholder="输入中文文本...")

# Step 2: Grid size slider (width = height, default 200)
grid_size = st.selectbox(
    "Select Grid Item Width and Height (px):",
    options=[50, 100, 150, 200],  # Predefined sizes
    index=3,  # Default is 200
)

# Step 3: Automatically adjust font size based on grid size
font_size = int((grid_size * 45) / 50)  # Calculate font size with a ratio of 45/50

# Step 4: Text color input
text_color = st.color_picker("Enter Text Color (name or hex code):", value=DEFAULT_TEXT_COLOR)

# Step 5: Font family selection (default set to FangSong)
font_family = st.selectbox(
    "Select Font Style:",
    options=["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "SimHei", "KaiTi", "FangSong", "LiSu"],
    index=7,  # Default to FangSong
)

# Step 6: Font weight selection (default set to lighter)
font_weight = st.selectbox(
    "Select Font Weight:",
    options=["normal", "bold", "lighter", "bolder", "100", "200", "300", "400", "500", "600", "700", "800", "900"],
    index=0,  # Default to lighter
)

# Step 7: Option to display unique characters only
unique_option = st.radio(
    "Display Options:",
    options=["All Characters", "Unique Characters Only"],
    index=1,  # Default to "Unique Characters Only"
)

# Step 8: Border thickness input for sub-items (allows fractional values like 0.5px)
border_thickness = st.text_input(
    "Enter Border Thickness (px):",
    value=DEFAULT_BORDER_THICKNESS
)

# Validate and sanitize border thickness input
border_thickness = validate_border_thickness(border_thickness)

# Step 9: Border color input for sub-items
border_color = st.color_picker("Enter Border Color (name or hex code):", value=DEFAULT_BORDER_COLOR)

# Step 10: Display the text as a grid with styled tiles
if user_input:
    # Process the input based on the selected option
    if unique_option == "Unique Characters Only":
        seen = set()
        characters = [char for char in user_input if not (char in seen or seen.add(char))]  # Preserve order of unique characters
    else:
        characters = list(user_input.replace("\n", ""))  # Keep all characters and remove line breaks
    
    # Generate CSS styles
    css_styles = generate_css(grid_size, font_size, font_weight, text_color, font_family, border_thickness, border_color)
    
    # Render CSS in Streamlit
    st.markdown(css_styles, unsafe_allow_html=True)
    
    # Generate the HTML grid with nested grids and centered character
    grid_html = '<div class="grid-container">'
    for char in characters:
        grid_html += '<div class="grid-item">'  # Outer grid item with nested squares
        for _ in range(9):  # Add nine sub-items inside each item for background
            grid_html += '<div class="sub-item"></div>'
        grid_html += f'<span class="character">{char}</span>'  # Centered character overlay
        grid_html += '</div>'
    grid_html += '</div>'
    
    # Render the nested grid in Streamlit
    st.markdown(grid_html, unsafe_allow_html=True)
