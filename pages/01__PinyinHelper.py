import streamlit as st
from pypinyin import pinyin, Style
import string
import re

def get_abbreviated_pinyin_with_color(char):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        return f":blue[{pin[:2]}]"  # Wrap in Streamlit color syntax
    # If starts with vowel, return first letter
    elif pin[0] in 'aeiou':
        return pin[0]
    # Otherwise return first consonant
    else:
        return pin[0]

def convert_text(text):
    result = []
    for char in text:
        # If character is punctuation, keep it as is
        if char in string.punctuation or char.isspace():
            result.append(char)
        else:
            # Get abbreviated pinyin with color formatting
            result.append(get_abbreviated_pinyin_with_color(char))
    return "".join(result)

def format_with_line_breaks_and_numbers(text):
    # Split text into sentences
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)
    
    # Group sentences into chunks of 3 and add paragraph numbers
    formatted_text = ""
    current_group = []
    paragraph_number = 1
    
    for i in range(0, len(sentences), 2):  # Step by 2 because split keeps delimiters
        if i < len(sentences):
            current_sentence = sentences[i]
            if i+1 < len(sentences):  # Add the punctuation back
                current_sentence += sentences[i+1]
            
            current_group.append(current_sentence)
            
            # When we have 3 sentences or it's the last group
            if len(current_group) == 3 or i >= len(sentences)-2:
                paragraph_mark = f"P{paragraph_number:02d}: "  # Format as P01, P02, etc.
                formatted_text += paragraph_mark + "".join(current_group) + "\n\n"
                current_group = []
                paragraph_number += 1
    
    return formatted_text.strip()  # Remove trailing whitespace

# Create Streamlit interface
st.title("Chinese to Abbreviated Pinyin Converter")

# Input text area
input_text = st.text_area("Enter Chinese text:", "")

if input_text:
    # Convert text
    output_text = convert_text(input_text)
    
    # Display regular output
    st.subheader("Result:")
    st.markdown(output_text)
    
    # Display output with line breaks and paragraph numbers
    st.subheader("Result with line breaks (every 3 sentences):")
    formatted_output = format_with_line_breaks_and_numbers(output_text)
    st.markdown(formatted_output)
