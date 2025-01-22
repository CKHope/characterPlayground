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

def get_abbreviated_pinyin(char, colorize=False, use_html=False):
    """
    Get the abbreviated pinyin for a Chinese character.
    Optionally colorize the output and choose between HTML or Streamlit syntax.

    Args:
        char (str): The Chinese character to process.
        colorize (bool): Whether to apply color formatting.
        use_html (bool): Whether to use HTML for color formatting.

    Returns:
        str: The abbreviated pinyin or radical for the character.
    """
    pin = pinyin(char, style=Style.NORMAL)[0][0]  # Get the first pronunciation of the character

    # Check if the pinyin starts with double consonants (zh, ch, sh)
    if pin.startswith(('zh', 'ch', 'sh')):
        formatted_pin = pin[:2]  # Extract the first two letters
        if colorize:  # Apply color formatting if requested
            if use_html:
                return f'<span style="color: DarkTurquoise">{formatted_pin}</span>'  # HTML formatting
            else:
                return f':blue[{formatted_pin}]'  # Streamlit formatting
        return formatted_pin  # Return the double consonant without formatting

    # Return the first letter if it starts with a vowel; otherwise, return the first consonant
    return pin[0] if pin[0] in 'aeiou' else pin[0]

def convert_text(text, type=1):
    """
    Convert Chinese text to abbreviated pinyin, radicals, or keep punctuation.

    Args:
        text (str): The input text to process.
        type (int): The conversion type (0: pinyin, 1: colorized pinyin, 2: radicals).

    Returns:
        str: The converted text.
    """
    result = []  # Initialize an empty list to store the converted characters

    for char in text:
        if char in string.punctuation or char.isspace():  # Preserve punctuation and spaces
            result.append(char)
        else:
            if type == 0:  # Convert to abbreviated pinyin without color
                result.append(get_abbreviated_pinyin(char))
            elif type == 1:  # Convert to colorized pinyin with HTML formatting
                result.append(get_abbreviated_pinyin(char, colorize=True, use_html=True))
            elif type == 2:  # Convert to radicals using the utility function
                result.append(returnCharRadical(char))

    return "".join(result)  # Join the list into a single string and return

def count_chinese_characters(text):
    """
    Count only Chinese characters within the specified Unicode range.

    Args:
        text (str): The input text to count characters from.

    Returns:
        int: The count of Chinese characters.
    """
    return len([char for char in text if '\u4e00' <= char <= '\u9fff'])

def format_with_line_breaks_and_numbers(text, original_text):
    """
    Format text with line breaks and paragraph numbers.

    Args:
        text (str): The converted text to format.
        original_text (str): The original text for reference.

    Returns:
        str: Formatted text with paragraph numbers and character counts.
    """
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)  # Split into sentences while preserving punctuation
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
            
            if i + 1 < len(sentences):  
                current_sentence += sentences[i + 1]  
                if i + 1 < len(original_sentences):
                    current_original_sentence += original_sentences[i + 1]
            
            current_group.append(current_sentence)  
            current_original_group.append(current_original_sentence)  
            
            if len(current_group) == 3 or i >= len(sentences) - 2:
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
    output_text = convert_text(input_text, type=0)  
    
    st.subheader("Result:")
    st.markdown(output_text, unsafe_allow_html=True)  
    
    output_text_pinyin = convert_text(input_text, type=1)  
    total_chars = count_chinese_characters(input_text)  
    
    st.markdown(f"### Recite helper - Pinyin <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    
    formatted_output = format_with_line_breaks_and_numbers(output_text_pinyin, input_text)
    
    st.markdown(formatted_output, unsafe_allow_html=True)  
    
    output_text_radical = convert_text(input_text, type=2)  
    
    st.markdown(f"### Recite helper - Radical <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
    
    formatted_output_radical = format_with_line_breaks_and_numbers(output_text_radical, input_text)
    
    st.markdown(formatted_output_radical, unsafe_allow_html=True)
