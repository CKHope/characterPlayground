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

def get_abbreviated_pinyin(char, color=False):
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh and format them accordingly
    if pin.startswith(('zh', 'ch', 'sh')):
        return f'<span style="color: DarkTurquoise">{pin[:2]}</span>' if color else f':blue[{pin[:2]}]'
    
    # Return the first letter based on whether it starts with a vowel or consonant
    return pin[0] if pin[0] in 'aeiou' else pin[0]

def convert_text(text, type=1):
    result = []
    for char in text:
        # Keep punctuation and whitespace as is
        if char in string.punctuation or char.isspace():
            result.append(char)
        else:
            # Convert based on the specified type
            if type == 1:
                result.append(get_abbreviated_pinyin(char, color=True))  # For Pinyin helper
            elif type == 0:
                result.append(get_abbreviated_pinyin(char))  # For regular output
            elif type == 2:
                result.append(returnCharRadical(char))  # For radical representation
    return "".join(result)  # Join the list into a single string

def count_chinese_characters(text):
    # Count only Chinese characters within the specified Unicode range
    return len([char for char in text if '\u4e00' <= char <= '\u9fff'])

def format_with_line_breaks_and_numbers(text, original_text):
    # Split text into sentences while preserving punctuation for both pinyin and original text
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)
    original_sentences = re.split('([。！？\.\!\?][\s\n]*)', original_text)
    
    formatted_text = ""
    current_group = []
    current_original_group = []
    paragraph_number = 1
    
    # Custom CSS for paragraph numbers and character count display
    st.markdown("""
        <style>
        .paragraph-number {
            background-color: #8B0000;  /* Dark red background */
            color: white;  /* White text */
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
            background-color: #00008B; /* Dark blue background */
            color: white; /* White text */
            padding: 4px 6px;
            border-radius: 0 3px 3px 0; 
            margin-right: 10px;
            font-size: 0.9em;
            display: inline-flex;
            align-items: center;
            width: 70px; /* Fixed width for consistency */
            justify-content: center;
            height: 20px;
            line-height: 20px;
        }
        .total-count {
            color: #8B0000; /* Dark red text */
            font-weight: bold; /* Bold text */
        }
        .label-group {
            display: inline-flex;
            margin-right: 10px; 
            align-items: center; 
            height: 20px; 
        }
        </style>
    """, unsafe_allow_html=True)
    
    for i in range(0, len(sentences), 2):  # Step by two to include punctuation correctly
        if i < len(sentences):
            current_sentence = sentences[i]
            current_original_sentence = original_sentences[i] if i < len(original_sentences) else ""
            
            if i + 1 < len(sentences):  # Add punctuation back to the sentence
                current_sentence += sentences[i + 1]
                if i + 1 < len(original_sentences):
                    current_original_sentence += original_sentences[i + 1]
            
            current_group.append(current_sentence)
            current_original_group.append(current_original_sentence)
            
            # When we have three sentences or it's the last group, format and add to output
            if len(current_group) == 3 or i >= len(sentences) - 2:
                group_text = ''.join(current_group)
                original_group_text = ''.join(current_original_group)
                char_count = count_chinese_characters(original_group_text)
                
                formatted_text += f"""<span class="label-group">
                    <span class="paragraph-number">P{paragraph_number:02d}</span>
                    <span class="char-count">{char_count} chars</span>
                </span>{group_text}<br><br>"""
                
                current_group = []   # Reset for next group of sentences
                current_original_group = []
                paragraph_number += 1
    
    return formatted_text.strip()  # Remove any trailing whitespace

# Create Streamlit interface for user input and output display
st.title("Chinese to Abbreviated Pinyin Converter")

# Input text area for user to enter Chinese text
input_text = st.text_area("Enter Chinese text:", "")

if input_text:
    # Convert input text for Result section (regular output)
    output_text = convert_text(input_text, 0)
    
    st.subheader("Result:")
    st.markdown(output_text, unsafe_allow_html=True)   # Display converted output
    
    # Convert input text for Pinyin helper output (for recitation assistance)
    output_text_pinyin = convert_text(input_text, 1)
    
    total_chars = count_chinese_characters(input_text)   # Calculate total character count
    
    st.markdown(f"### Recite helper - Pinyin <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    
    formatted_output = format_with_line_breaks_and_numbers(output_text_pinyin, input_text)   # Format output with line breaks and numbers
    
    st.markdown(formatted_output, unsafe_allow_html=True)   # Display formatted Pinyin helper output
    
    # Convert input text for Radical helper output (for additional learning aid)
    output_text_radical = convert_text(input_text, 2)
    
    st.markdown(f"### Recite helper - Radical <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    
    formatted_output_radical = format_with_line_breaks_and_numbers(output_text_radical, input_text)   # Format radical output
    
    st.markdown(formatted_output_radical, unsafe_allow_html=True)   # Display formatted Radical helper output
