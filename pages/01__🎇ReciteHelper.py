"""
Chinese to Abbreviated Pinyin Converter - Version 1.1
Features:
- Converts Chinese characters to abbreviated pinyin
- Shows double consonants (ch, sh, zh) in blue
- Groups text into sections of 3 sentences
- Displays character count for each section (counting original Chinese characters)
- Shows total character count
- Consistent styling with fixed-width character count displays
New in 1.1:
- Added Kangxi radical conversion with preserved punctuation
"""

import streamlit as st
from pypinyin import pinyin, Style
import string
import re
from utils import returnCharRadical


def get_abbreviated_pinyin_with_color_break(char):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        # Remove the :blue[] syntax and use HTML span instead
        return f'<span style="color: DarkTurquoise">{pin[:2]}</span>'
    # If starts with vowel, return first letter
    elif pin[0] in 'aeiou':
        return pin[0]
    # Otherwise return first consonant
    else:
        return pin[0]

def get_abbreviated_pinyin_with_color(char):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        # Remove the :blue[] syntax and use HTML span instead
        return f':blue[{pin[:2]}]'
    # If starts with vowel, return first letter
    elif pin[0] in 'aeiou':
        return pin[0]
    # Otherwise return first consonant
    else:
        return pin[0]

def convert_text(text, type=1):
    result = []
    for char in text:
        # If character is punctuation, keep it as is
        if char in string.punctuation or char.isspace():
            result.append(char)
        else:
            if type == 1:
                # Get abbreviated pinyin with color formatting
                result.append(get_abbreviated_pinyin_with_color_break(char))
            elif type == 0:
                # Get abbreviated pinyin with color formatting
                result.append(get_abbreviated_pinyin_with_color(char))
            elif type == 2:
                # Get radical
                result.append(returnCharRadical(char))
    return "".join(result)

def count_chinese_characters(text):
    # Count only Chinese characters
    return len([char for char in text if '\u4e00' <= char <= '\u9fff'])

def format_with_line_breaks_and_numbers(text, original_text):
    # Split text into sentences for both pinyin and original text
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)
    original_sentences = re.split('([。！？\.\!\?][\s\n]*)', original_text)
    
    # Group sentences into chunks of 3 and add paragraph numbers
    formatted_text = ""
    current_group = []
    current_original_group = []
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
    
    for i in range(0, len(sentences), 2):  # Step by 2 because split keeps delimiters
        if i < len(sentences):
            current_sentence = sentences[i]
            current_original_sentence = original_sentences[i] if i < len(original_sentences) else ""
            
            if i+1 < len(sentences):  # Add the punctuation back
                current_sentence += sentences[i+1]
                if i+1 < len(original_sentences):
                    current_original_sentence += original_sentences[i+1]
            
            current_group.append(current_sentence)
            current_original_group.append(current_original_sentence)
            
            # When we have 3 sentences or it's the last group
            if len(current_group) == 3 or i >= len(sentences)-2:
                group_text = ''.join(current_group)
                original_group_text = ''.join(current_original_group)
                char_count = count_chinese_characters(original_group_text)
                
                # Create paragraph number and character count with HTML styling
                formatted_text += f"""<span class="label-group">
                    <span class="paragraph-number">P{paragraph_number:02d}</span
                    ><span class="char-count">{char_count} chars</span>
                </span>{group_text}<br><br>"""
                
                current_group = []
                current_original_group = []
                paragraph_number += 1
    
    return formatted_text.strip()  # Remove trailing whitespace

# Create Streamlit interface
st.title("Chinese to Abbreviated Pinyin Converter")

# Input text area
input_text = st.text_area("Enter Chinese text:", "")

if input_text:
    # Convert text for Result section
    output_text = convert_text(input_text, 0)
    
    # Display regular output
    st.subheader("Result:")
    st.markdown(output_text, unsafe_allow_html=True)
    
    # Convert text for Pinyin helper
    output_text_pinyin = convert_text(input_text, 1)
    # Calculate total character count
    total_chars = count_chinese_characters(input_text)
    
    # Display Pinyin helper output
    st.markdown(f"### Recite helper - Pinyin <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    formatted_output = format_with_line_breaks_and_numbers(output_text_pinyin, input_text)
    st.markdown(formatted_output, unsafe_allow_html=True)
    
    # Convert text for Radical helper
    output_text_radical = convert_text(input_text, 2)
    
    # Display Radical helper output
    st.markdown(f"### Recite helper - Radical <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    formatted_output_radical = format_with_line_breaks_and_numbers(output_text_radical, input_text)
    st.markdown(formatted_output_radical, unsafe_allow_html=True)
