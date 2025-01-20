import streamlit as st
from pypinyin import pinyin, Style
import string
import re

def get_abbreviated_pinyin_with_color(char):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        return pin[:2]  # Return without color formatting since it will be handled in convert_text
    # If starts with vowel, return first letter
    elif pin[0] in 'aeiou':
        return pin[0]
    # Otherwise return first consonant
    else:
        return pin[0]

def convert_text(text):
    result = []
    i = 0
    while i < len(text):
        if text[i] in string.punctuation or text[i].isspace():
            result.append(text[i])
            i += 1
        else:
            # Get abbreviated pinyin
            pin = get_abbreviated_pinyin_with_color(text[i])
            
            # Check if it's a double consonant (ch, sh, zh) and color it blue
            if len(pin) == 2:
                result.append(f":blue[{pin}]")
            else:
                result.append(pin)
            i += 1
    return "".join(result)

def count_characters(text):
    # Count characters excluding spaces and punctuation
    return len([char for char in text if char not in string.punctuation and not char.isspace()])

def format_with_line_breaks_and_numbers(text):
    # Previous CSS remains the same
    st.markdown("""
        <style>
        /* Previous styles remain unchanged */
        .blue-consonant {
            color: #0000FF;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # In the formatting loop, replace :blue[] syntax with HTML span
    formatted_text = text.replace(":blue[", '<span class="blue-consonant">').replace("]", "</span>")
    
    # Rest of the function remains the same
    # ...

# In the main app code
if input_text:
    # Convert text
    output_text = convert_text(input_text)
    
    # Calculate total character count
    total_chars = count_characters(input_text)
    
    # Display output with proper HTML rendering
    st.markdown(f"# Recite helper - Pinyin <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    formatted_output = format_with_line_breaks_and_numbers(output_text)
    st.markdown(formatted_output, unsafe_allow_html=True)

# Create Streamlit interface
st.title("Chinese to Abbreviated Pinyin Converter")

# Input text area
input_text = st.text_area("Enter Chinese text:", "")

if input_text:
    # Convert text
    output_text = convert_text(input_text)
    
    # Calculate total character count
    total_chars = count_characters(input_text)
    
    # Display output with line breaks and styled paragraph numbers
    st.markdown(f"# Recite helper - Pinyin ({total_chars} chars)", unsafe_allow_html=True)
    formatted_output = format_with_line_breaks_and_numbers(output_text)
    st.markdown(formatted_output, unsafe_allow_html=True)
