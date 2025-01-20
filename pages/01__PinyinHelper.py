import streamlit as st
from pypinyin import pinyin, Style
import string
import re

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
            if type == 0:
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
            char_count = count_characters(current_sentence)
            if i+1 < len(sentences):  # Add the punctuation back
                current_sentence += sentences[i+1]
                # char_count = count_characters(current_sentence)
            current_group.append(current_sentence)
            
            # When we have 3 sentences or it's the last group
            if len(current_group) == 3 or i >= len(sentences)-2:
                group_text = ''.join(current_group)
                # char_count = count_characters(group_text)
                
                # Create paragraph number and character count with HTML styling
                formatted_text += f"""<span class="label-group">
                    <span class="paragraph-number">P{paragraph_number:02d}</span
                    ><span class="char-count">{char_count} chars</span>
                </span>{group_text}<br><br>"""
                
                current_group = []
                paragraph_number += 1
    
    return formatted_text.strip()  # Remove trailing whitespace

# Create Streamlit interface
st.title("Chinese to Abbreviated Pinyin Converter")

# Input text area
input_text = st.text_area("Enter Chinese text:", "")

if input_text:
    # Convert text
    output_text = convert_text(input_text,0)
    
    # Display regular output
    st.subheader("Result:")
    st.markdown(output_text,unsafe_allow_html=True)
    
    
    output_text = convert_text(input_text,1)
    # Calculate total character count
    total_chars = count_characters(input_text)
    
    # Display output with line breaks and styled paragraph numbers
    st.markdown(f"### Recite helper - Pinyin <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    formatted_output = format_with_line_breaks_and_numbers(output_text)
    st.markdown(formatted_output, unsafe_allow_html=True)
