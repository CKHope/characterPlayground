import streamlit as st

# Title of the app
st.title("Chinese Character Extractor (Order Preserved)")

# User input for Chinese text
user_input = st.text_area("Enter Chinese text:", "", height=200)

# Check if input is not empty
if user_input:
    # Use an ordered approach to extract unique characters
    seen = set()
    unique_characters = []
    
    for char in user_input:
        # Check if the character is Chinese
        if '\u4e00' <= char <= '\u9fff' and char not in seen:
            unique_characters.append(char)
            seen.add(char)
    
    # Display unique characters
    if unique_characters:
        st.subheader("Unique Chinese Characters (Order Preserved):")
        unique_chars_str = "".join(unique_characters)
        st.text_area("Copy the unique characters below:", unique_chars_str, height=100)
    else:
        st.warning("No valid Chinese characters found in the input.")
else:
    st.info("Please enter some Chinese text to extract unique characters.")
