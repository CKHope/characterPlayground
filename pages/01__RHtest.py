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

import streamlit as st  # Import Streamlit for creating web apps
from pypinyin import pinyin, Style  # Import pinyin library for converting Chinese characters to pinyin
import string  # Import string module for string operations
import re  # Import regular expressions for text processing
from utils import returnCharRadical  # Import utility function for getting radicals

def get_abbreviated_pinyin_with_color_break(char):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        # Return the first two letters in blue color using HTML span
        return f'<span style="color: DarkTurquoise">{pin[:2]}</span>'
    # If it starts with a vowel, return the first letter
    elif pin[0] in 'aeiou':
        return pin[0]
    # Otherwise, return the first consonant
    else:
        return pin[0]

def get_abbreviated_pinyin_with_color(char):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        # Return the first two letters in blue color using a different syntax
        return f':blue[{pin[:2]}]'
    # If it starts with a vowel, return the first letter
    elif pin[0] in 'aeiou':
        return pin[0]
    # Otherwise, return the first consonant
    else:
        return pin[0]

def convert_text(text, type=1):
    result = []  # Initialize an empty list to store results
    for char in text:
        # If character is punctuation or whitespace, keep it as is
        if char in string.punctuation or char.isspace():
            result.append(char)
        else:
            if type == 1:
                # Get abbreviated pinyin with color formatting (for Pinyin helper)
                result.append(get_abbreviated_pinyin_with_color_break(char))
            elif type == 0:
                # Get abbreviated pinyin without color formatting (for regular output)
                result.append(get_abbreviated_pinyin_with_color(char))
            elif type == 2:
                # Get radical representation of the character (for Radical helper)
                result.append(returnCharRadical(char))
    return "".join(result)  # Join and return the results as a single string

def count_chinese_characters(text):
    # Count only Chinese characters within the specified Unicode range
    return len([char for char in text if '\u4e00' <= char <= '\u9fff'])

def format_with_line_breaks_and_numbers(text, original_text):
    # Split text into sentences while preserving delimiters (punctuation)
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)
    original_sentences = re.split('([。！？\.\!\?][\s\n]*)', original_text)
    
    formatted_text = ""  # Initialize formatted text output
    current_group = []  # Store current group of sentences
    current_original_group = []  # Store corresponding original sentences
    paragraph_number = 1  # Initialize paragraph numbering
    
    # Custom CSS for styling paragraph numbers and character counts
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
            current_original_sentence = original_sentences[i] if i < len(original_sentences) else ""
            
            if i+1 < len(sentences):  
                current_sentence += sentences[i+1]  
                if i+1 < len(original_sentences):
                    current_original_sentence += original_sentences[i+1]
            
            current_group.append(current_sentence)  
            current_original_group.append(current_original_sentence)  
            
            if len(current_group) == 3 or i >= len(sentences)-2:
                group_text = ''.join(current_group)  
                original_group_text = ''.join(current_original_group)  
                char_count = count_chinese_characters(original_group_text)  
                
                formatted_text += f"""<span class="label-group">
                    <span class="paragraph-number">P{paragraph_number:02d}</span>
                    ><span class="char-count">{char_count} chars</span>
                </span>{group_text}<br><br>"""
                
                current_group = []  
                current_original_group = []  
                paragraph_number += 1  
    
    return formatted_text.strip()  

# Create Streamlit interface to interact with users
st.title("Chinese to Abbreviated Pinyin Converter")

# Input text area for user to enter Chinese text
input_text = st.text_area("Enter Chinese text:", "")

if input_text:
    output_text = convert_text(input_text, 0)  
    
    st.subheader("Result:")
    st.markdown(output_text, unsafe_allow_html=True)  
    
    output_text_pinyin = convert_text(input_text, 1)  
    total_chars = count_chinese_characters(input_text)  
    
    st.markdown(f"### Recite helper - Pinyin <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    
    formatted_output = format_with_line_breaks_and_numbers(output_text_pinyin, input_text)
    
    st.markdown(formatted_output, unsafe_allow_html=True)  
    
    output_text_radical = convert_text(input_text, 2)  
    
    st.markdown(f"### Recite helper - Radical <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    
    formatted_output_radical = format_with_line_breaks_and_numbers(output_text_radical, input_text)
    
    st.markdown(formatted_output_radical, unsafe_allow_html=True)
