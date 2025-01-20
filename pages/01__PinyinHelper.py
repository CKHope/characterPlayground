import streamlit as st
from pypinyin import pinyin, Style
import string

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

# Create Streamlit interface
st.title("Chinese to Abbreviated Pinyin Converter")

# Input text area
input_text = st.text_area("Enter Chinese text:", "")

if input_text:
    # Convert and display result
    output_text = convert_text(input_text)
    st.subheader("Result:")
    st.markdown(output_text)  # Using markdown instead of text to render colored text
