import streamlit as st
from pypinyin import pinyin, Style
import string
import re

def get_abbreviated_pinyin_with_color(char):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        return f'<span class="blue-text">{pin[:2]}</span>'
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

def count_characters(text):
    # Count characters excluding spaces and punctuation
    return len([char for char in text if char not in string.punctuation and not char.isspace()])

def format_with_line_breaks_and_numbers(text):
    # Split text into sentences
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)
    
    # Group sentences into chunks of 3 and add paragraph numbers
    formatted_text = ""
    current_group = []
    paragraph_number = 1
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .paragraph-number {
            background-color: #8B0000;
            color: white;
            padding: 4px 6px;
            border-radius: 3px 0 0 3px;
            margin-right: 0;
            display: inline-flex;
            align-items: center;
            height: 20px;
            line-height: 20px;
            font-size: 0.9em;
        }
        .char-count {
            background-color: #00008B;
            color: white;
            padding: 4px 6px;
            border-radius: 0 3px 3px 0;
            margin-right: 10px;
            font-size: 0.9em;
            display: inline-flex;
            align-items: center;
            width: 70px;
            justify-content: center;
            height: 20px;
            line-height: 20px;
        }
        .total-count {
            color: #FF0000;
        }
        .label-group {
            display: inline-flex;
            margin-right: 10px;
            align-items: center;
            height: 20px;
        }
        .blue-text {
            color: #0000FF;
        }
        .output-text {
            color: white;
            font-family: monospace;
        }
        </style>
    """, unsafe_allow_html=True)
    
    for i in range(0, len(sentences), 2):
        if i < len(sentences):
            current_sentence = sentences[i]
            if i+1 < len(sentences):
                current_sentence += sentences[i+1]
            
            current_group.append(current_sentence)
            
            if len(current_group) == 3 or i >= len(sentences)-2:
                group_text = ''.join(current_group)
                char_count = count_characters(group_text)
                
                formatted_text += f"""<div class="output-text">
                    <span class="label-group">
                        <span class="paragraph-number">P{paragraph_number:02d}</span
                        ><span class="char-count">{char_count} chars</span>
                    </span>{group_text}</div><br>"""
                
                current_group = []
                paragraph_number += 1
    
    return formatted_text.strip()

# Create Streamlit interface with dark theme
st.set_page_config(page_title="Chinese to Pinyin Converter", layout="wide")

# Input text area
input_text = st.text_area("Enter Chinese text:", "", key="input")

if input_text:
    # Convert text
    output_text = convert_text(input_text)
    
    # Calculate total character count
    total_chars = count_characters(input_text)
    
    # Display output with styling
    st.markdown(f'<h1 class="output-text">Recite helper - Pinyin <span class="total-count">({total_chars} chars)</span></h1>', 
               unsafe_allow_html=True)
    formatted_output = format_with_line_breaks_and_numbers(output_text)
    st.markdown(formatted_output, unsafe_allow_html=True)
