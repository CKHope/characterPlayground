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

def format_with_line_breaks(text):
    # Split text into sentences (looking for period, question mark, or exclamation mark followed by space or newline)
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)
    
    # Rejoin sentences and add line break after every 3 sentences
    formatted_text = ""
    for i in range(0, len(sentences), 2):  # Step by 2 because split keeps delimiters
        if i < len(sentences):
            formatted_text += sentences[i]
            if i+1 < len(sentences):  # Add the punctuation back
                formatted_text += sentences[i+1]
            
            # Add double line break after every 3 sentences
            if (i//2 + 1) % 3 == 0 and i < len(sentences)-2:
                formatted_text += "\n\n"
    
    return formatted_text

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
    
    # Display output with line breaks after every 3 sentences
    st.subheader("Result with line breaks (every 3 sentences):")
    formatted_output = format_with_line_breaks(output_text)
    st.markdown(formatted_output)
