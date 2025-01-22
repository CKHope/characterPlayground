import logging
import unittest
import streamlit as st
import string
import re
from pypinyin import pinyin, Style
from utils import returnCharRadical

# Configure logging settings with timestamps
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def count_chinese_characters(text: str) -> int:
    """Counts the number of Chinese characters in the input text."""
    return len([char for char in text if '\u4e00' <= char <= '\u9fff'])

def get_abbreviated_pinyin_with_color(char: str) -> str:
    """Returns the abbreviated Pinyin of a character with color formatting for double consonants."""
    # Get pinyin for the character (taking first pronunciation)
    pin = pinyin(char, style=Style.NORMAL)[0][0]
    
    # Check if pinyin starts with zh, ch, sh
    if pin.startswith(('zh', 'ch', 'sh')):
        # Return the first two letters in blue color using HTML span
        return f'<span style="color: DarkTurquoise">{pin[:2]}</span>'
    # If starts with vowel, return first letter
    elif pin[0] in 'aeiou':
        return pin[0]
    # Otherwise return first consonant
    else:
        return pin[0]

def inject_css():
    # Injects CSS styles for the Streamlit interface
    css_styles = """
        <style>
        .paragraph-number {
            background-color: #8B0000; /* Dark Red */
            color: white; /* Text color */
            padding: 4px 6px; /* Padding */
            border-radius: 3px 0 0 3px; /* Rounded corners */
        }
        .char-count {
            background-color: #00008B; /* Dark Blue */
            color: white; /* Text color */
            padding: 4px 6px; /* Padding */
            border-radius: 0 3px 3px 0; /* Rounded corners */
            margin-right: 10px; /* Margin */
        }
        .total-count {
            color: #8B0000; /* Dark Red */
            font-weight: bold; /* Bold text */
        }
        .label-group {
           display: inline-flex; /* Flex layout */
           margin-right: 10px; /* Margin */
           align-items: center; /* Center items vertically */
           height: 20px; /* Height for alignment */
        }
        </style>
    """
    st.markdown(css_styles, unsafe_allow_html=True)

def validate_input(text: str) -> bool:
    """Validates if the input text contains valid Chinese characters."""
    if not text.strip():
        st.error("Input cannot be empty.")
        return False
    if not any('\u4e00' <= char <= '\u9fff' for char in text):
        st.error("Input must contain at least one Chinese character.")
        return False
    return True

@st.cache_data
def convert_text(text: str, conversion_type: str = 'regular') -> str:
    """Converts the input text based on the specified conversion type."""
    logging.info(f"Converting text with type '{conversion_type}'")
    
    result = []
    
    for char in text:
        if char in string.punctuation or char.isspace():
            result.append(char)
        else:
            try:
                if conversion_type == 'pinyin_helper':
                    result.append(get_abbreviated_pinyin_with_color(char))
                elif conversion_type == 'radical':
                    result.append(returnCharRadical(char))
            except Exception as e:
                logging.error(f"Error converting character '{char}': {e}")
                st.error(f"Error processing character '{char}'. Please check your input.")
    
    return "".join(result)

def format_with_line_breaks_and_numbers(text: str, original_text: str) -> str:
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)
    original_sentences = re.split('([。！？\.\!\?][\s\n]*)', original_text)
    
    formatted_text = ""
    current_group = []
    current_original_group = []
    paragraph_number = 1
    
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
                    <span class="char-count">{char_count} chars</span>
                </span>{group_text}<br><br>"""
                
                current_group.clear()  
                current_original_group.clear()  
                paragraph_number += 1
    
    return formatted_text.strip()  

# Create Streamlit interface to interact with the converter tool
st.title("Chinese to Abbreviated Pinyin Converter")

# Inject CSS styles into the Streamlit application
inject_css()

# Input text area for user to enter Chinese text
input_text = st.text_area("Enter Chinese text:", "")

if validate_input(input_text):
    with st.spinner('Processing...'):
        # Convert text for Result section using type='regular' (regular output)
        output_text = convert_text(input_text, 'regular')
        
        st.subheader("Result:")
        st.markdown(output_text, unsafe_allow_html=True)
        
        # Convert text for Pinyin helper using type='pinyin_helper' 
        output_text_pinyin = convert_text(input_text, 'pinyin_helper')
        
        total_chars = count_chinese_characters(input_text)  
        
        st.markdown(f"### Recite helper - Pinyin <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)
        
        formatted_output = format_with_line_breaks_and_numbers(output_text_pinyin, input_text)
        
        st.markdown(formatted_output, unsafe_allow_html=True)
        
        # Convert text for Radical helper using type='radical' 
        output_text_radical = convert_text(input_text, 'radical')

        st.markdown(f"### Recite helper - Radical <span class='total-count'>({total_chars} chars)</span>", unsafe_allow_html=True)

        formatted_output_radical = format_with_line_breaks_and_numbers(output_text_radical, input_text)
        
        st.markdown(formatted_output_radical, unsafe_allow_html=True)

# Reset button to clear inputs and outputs
if st.button('Reset'):
    input_text = ""
    st.experimental_rerun()  # Rerun the script to reset the state

# Download button for results with format selection
download_format = st.selectbox("Choose download format:", ["TXT", "CSV"])

if st.button('Download Results'):
    if download_format == "CSV":
        results_to_download = "Original Text,Converted Text\n"
        results_to_download += f"{input_text},{output_text}\n"
    else:
        results_to_download = f"Original Text:\n{input_text}\n\nConverted Text:\n{output_text}\n"
    
    # Create a download link for results
    st.download_button(
        label="Download Results",
        data=results_to_download,
        file_name=f'conversion_results.{download_format.lower()}',
        mime='text/csv' if download_format == "CSV" else 'text/plain'
    )

# Unit Tests
class TestChineseConverter(unittest.TestCase):

    def test_count_chinese_characters(self):
        self.assertEqual(count_chinese_characters("汉字"), 2)
        self.assertEqual(count_chinese_characters("Hello!"), 0)
        self.assertEqual(count_chinese_characters("汉字Hello"), 2)

    def test_validate_input(self):
        self.assertTrue(validate_input("汉字"))
        self.assertFalse(validate_input(""))
        self.assertFalse(validate_input("Hello!"))

if __name__ == '__main__':
    unittest.main()
