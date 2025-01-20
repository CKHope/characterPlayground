import streamlit as st
from pypinyin import pinyin, Style
import string
import re

def get_abbreviated_pinyin_for_result(char):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        return pin[:2]  # Return just the double consonant for Result section
    # If starts with vowel, return first letter
    elif pin[0] in 'aeiou':
        return pin[0]
    # Otherwise return first consonant
    else:
        return pin[0]

def get_abbreviated_pinyin_for_helper(char):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        return f':blue[{pin[:2]}]'  # Use Streamlit color syntax for helper section
    # If starts with vowel, return first letter
    elif pin[0] in 'aeiou':
        return pin[0]
    # Otherwise return first consonant
    else:
        return pin[0]

def count_characters(text):
    # Count characters excluding spaces and punctuation
    return len([char for char in text if char not in string.punctuation and not char.isspace()])

def convert_text_for_result(text):
    result = []
    for char in text:
        if char in string.punctuation or char.isspace():
            result.append(char)
        else:
            result.append(get_abbreviated_pinyin_for_result(char))
    return "".join(result)

def convert_text_for_helper(text):
    result = []
    for char in text:
        if char in string.punctuation or char.isspace():
            result.append(char)
        else:
            result.append(get_abbreviated_pinyin_for_helper(char))
    return "".join(result)

def format_with_line_breaks_and_numbers(text):
    # Split text into sentences
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)
    
    # Group sentences into chunks of 3 and add paragraph numbers
    formatted_text = ""
    current_group = []
    paragraph_number = 1
    
    # Custom CSS for paragraph numbers and character count
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
            color: #8B0000;
            font-weight: bold;
        }
        .label-group {
            display: inline-flex;
            margin-right: 10px;
            align-items: center;
            height: 20px;
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
                
                # Create paragraph number and character count with HTML styling
                formatted_text += f"""<span class="label-group">
                    <span class="paragraph-number">P{paragraph_number:02d}</span
                    ><span class="char-count">{char_count} chars</span>
                </span>{group_text}<br><br>"""
                
                current_group = []
                paragraph_number += 1
    
    return formatted_text.strip()

# Create Streamlit interface
st.title("Chinese to Abbreviated Pinyin Converter")

# Input text area
input_text = st.text_area("Enter Chinese text:", "")

if input_text:
    # Display regular output
    st.subheader("Result:")
    result_output = convert_text_for_result(input_text)
    st.markdown(result_output)
    
    # Calculate total character count
    total_chars = count_characters(input_text)
    
    # Display helper output
    st.markdown(f"### Recite helper - Pinyin ({total_chars} chars)", unsafe_allow_html=True)
    helper_output = convert_text_for_helper(input_text)
    formatted_output = format_with_line_breaks_and_numbers(helper_output)
    st.markdown(formatted_output, unsafe_allow_html=True)
