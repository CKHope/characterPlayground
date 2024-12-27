import streamlit as st

# App title
st.title("Chinese Text Grid Display with Customizable Font, Color, Weight, and Unique Characters")

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

# Step 7: Display the text as a grid with styled tiles
if user_input:
    # Process the input based on the selected option
    if unique_option == "Unique Characters Only":
        seen = set()
        characters = [char for char in user_input if not (char in seen or seen.add(char))]  # Preserve order of unique characters
    else:
        characters = list(user_input.replace("\n", ""))  # Keep all characters and remove line breaks
    
    # Define CSS for the grid and tile styling
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
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: {font_size}px;
            font-weight: {font_weight}; /* Dynamic font weight */
            border: 2px solid #4CAF50; /* Green border */
            background-color: #f9f9f9; /* Light grey background */
            color: {text_color}; /* Dynamic text color */
            font-family: {font_family}, 'Noto Sans SC', sans-serif; /* Dynamic font family */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Generate the HTML grid
    grid_html = '<div class="grid-container">'
    for char in characters:
        grid_html += f'<div class="grid-item">{char}</div>'
    grid_html += '</div>'
    
    # Render the grid in Streamlit
    st.markdown(grid_html, unsafe_allow_html=True)
