import streamlit as st

# App title
st.title("Chinese Text Grid with Customizable 9-Square Background Borders")

# Step 1: Input Chinese text from the user
user_input = st.text_area("Enter Chinese text:", height=100, placeholder="输入中文文本...")

# Step 2: Font size slider (default set to 33px)
font_size = st.slider("Adjust Font Size (px):", min_value=12, max_value=50, value=33)

# Step 3: Text color input
text_color = st.text_input("Enter Text Color (name or hex code):", value="#000000")  # Default to black

# Step 4: Font family selection (default set to FangSong)
font_family = st.selectbox(
    "Select Font Style:",
    options=["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "SimHei", "KaiTi", "FangSong", "LiSu"],
    index=7,  # Default to FangSong
)

# Step 5: Font weight selection (default set to lighter)
font_weight = st.selectbox(
    "Select Font Weight:",
    options=["normal", "bold", "lighter", "bolder", "100", "200", "300", "400", "500", "600", "700", "800", "900"],
    index=2,  # Default to lighter
)

# Step 6: Option to display unique characters only
unique_option = st.radio(
    "Display Options:",
    options=["All Characters", "Unique Characters Only"],
    index=0,  # Default to showing all characters
)

# Step 7: Border thickness input for sub-items (allows fractional values like 0.5px)
border_thickness = st.text_input(
    "Enter Border Thickness (px):",
    value="1px"  # Default to 1px
)

# Validate and sanitize border thickness input
try:
    # Ensure the input ends with 'px' and is a valid number
    if not border_thickness.endswith("px"):
        border_thickness += "px"
    float(border_thickness.replace("px", ""))  # Check if it's a valid number
except ValueError:
    st.error("Invalid border thickness! Please enter a valid number followed by 'px' (e.g., '0.5px').")
    border_thickness = "1px"  # Fallback to default

# Step 8: Border color input for sub-items
border_color = st.text_input("Enter Border Color (name or hex code):", value="#cccccc")  # Default to light gray

# Step 9: Display the text as a grid with styled tiles
if user_input:
    # Process the input based on the selected option
    if unique_option == "Unique Characters Only":
        seen = set()
        characters = [char for char in user_input if not (char in seen or seen.add(char))]  # Preserve order of unique characters
    else:
        characters = list(user_input.replace("\n", ""))  # Keep all characters and remove line breaks
    
    # Define CSS for the grid and nested grid styling
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap'); /* For fallback Chinese fonts */
        
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
            gap: 10px;
            justify-items: center;
            align-items: center;
        }}
        
        .grid-item {{
            width: 50px;
            height: 50px;
            display: grid;
            grid-template-columns: repeat(3, 1fr); /* Divide into 3x3 squares */
            grid-template-rows: repeat(3, 1fr);
            border: 2px solid #4CAF50; /* Green border */
            background-color: #f9f9f9; /* Light grey background */
            position: relative; /* For centering the character */
        }}
        
        .grid-item .character {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: {font_size}px; /* Default font size */
            font-weight: {font_weight}; /* Default font weight */
            color: {text_color}; /* Dynamic text color */
            font-family: {font_family}, 'Noto Sans SC', sans-serif; /* Dynamic font family */
        }}
        
        .grid-item .sub-item {{
            border: {border_thickness} solid {border_color}; /* Dynamic border thickness and color */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
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
