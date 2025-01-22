import streamlit as st
from pypinyin import pinyin, Style
import string
import re
from utils import returnCharRadical

# Constants for default styling
DOUBLE_CONSONANTS = ('zh', 'ch', 'sh')
PUNCTUATION = string.punctuation

def get_abbreviated_pinyin(chars, color=False, color_value=None):
    """Convert a string of Chinese characters to its abbreviated Pinyin representation."""
    pinyin_list = pinyin(chars, style=Style.NORMAL)
    abbreviated_pinyin = []
    
    for pin in pinyin_list:
        pin_str = pin[0]
        if pin_str.startswith(DOUBLE_CONSONANTS):
            # Use specified color or default to blue
            abbreviated_pinyin.append(f'<span style="color: {color_value}">{pin_str[:2]}</span>' if color else f':blue[{pin_str[:2]}]')
        else:
            abbreviated_pinyin.append(pin_str[0] if pin_str[0] in 'aeiou' else pin_str[0])

    return ''.join(abbreviated_pinyin)

def convert_text(text, conversion_type=1, color_value=None):
    """Convert a text based on the specified conversion type: 
       0 for regular output, 1 for Pinyin output, 2 for radical representation."""
    result = []
    for char in text:
        if char in PUNCTUATION or char.isspace():
            result.append(char)
        else:
            if conversion_type == 1:
                result.append(get_abbreviated_pinyin(char, color=True, color_value=color_value))  # For Pinyin helper output
            elif conversion_type == 0:
                result.append(get_abbreviated_pinyin(char))  # For regular output
            elif conversion_type == 2:
                result.append(returnCharRadical(char))  # For radical representation
    return "".join(result)

def count_chinese_characters(text):
    """Count Chinese characters in the given text."""
    return len([char for char in text if '\u4e00' <= char <= '\u9fff'])

def format_grouped_output(sentences, original_sentences):
    """Format grouped output into HTML with counts and styling."""
    formatted_text = []
    current_group = []
    current_original_group = []
    paragraph_number = 1
    
    for i in range(0, len(sentences), 2):
        current_sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
        current_original_sentence = original_sentences[i] + (original_sentences[i + 1] if i + 1 < len(original_sentences) else "")
        
        current_group.append(current_sentence)
        current_original_group.append(current_original_sentence)
        
        if len(current_group) == 3 or i >= len(sentences) - 2:
            group_text = ''.join(current_group)
            original_group_text = ''.join(current_original_group)
            char_count = count_chinese_characters(original_group_text)
            formatted_text.append(f"""
                <span class="label-group">
                    <span class="paragraph-number">P{paragraph_number:02d}</span>
                    <span class="char-count">{char_count} chars</span>
                </span>{group_text}<br><br>
            """)
            current_group.clear()
            current_original_group.clear()
            paragraph_number += 1
            
    return ''.join(formatted_text).strip()

def setup_streamlit():
    """Setup Streamlit UI components."""
    st.title("Chinese to Abbreviated Pinyin Converter - Version 1.1")
    
    # Color pickers for customization
    default_color = st.color_picker("Select color for double consonants", "#008B8B")
    st.markdown("""
        <style>
        .paragraph-number { background-color: #8B0000; color: white; padding: 4px 6px; border-radius: 3px 0 0 3px; }
        .char-count { background-color: #00008B; color: white; padding: 4px 6px; border-radius: 0 3px 3px 0; }
        .total-count { color: #8B0000; font-weight: bold; }
        .label-group { display: inline-flex; margin-right: 10px; align-items: center; }
        </style>
    """, unsafe_allow_html=True)

    return default_color

def main():
    """Main function to run the Streamlit app for converting Chinese text to Pinyin and radicals."""
    selected_color = setup_streamlit()

    input_text = st.text_area("Enter Chinese text:", "")
    if input_text:
        # Input validation
        if not input_text.strip():
            st.error("Please enter some Chinese text.")
            return

        # Regular Output
        output_text = convert_text(input_text, conversion_type=0)
        st.subheader("Result:")
        st.markdown(output_text, unsafe_allow_html=True)

        # Pinyin Helper Output
        output_text_pinyin = convert_text(input_text, conversion_type=1, color_value=selected_color)
        total_chars = count_chinese_characters(input_text)
        st.markdown(f"### Recite helper - Pinyin <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
        formatted_output = format_grouped_output(re.split('([。！？\.\!\?][\s\n]*)', output_text_pinyin), re.split('([。！？\.\!\?][\s\n]*)', input_text))
        st.markdown(formatted_output, unsafe_allow_html=True)

        # Radical Helper Output
        output_text_radical = convert_text(input_text, conversion_type=2)
        st.markdown(f"### Recite helper - Radical <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
        formatted_output_radical = format_grouped_output(re.split('([。！？\.\!\?][\s\n]*)', output_text_radical), re.split('([。！？\.\!\?][\s\n]*)', input_text))
        st.markdown(formatted_output_radical, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
