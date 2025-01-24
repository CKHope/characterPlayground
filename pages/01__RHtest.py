import streamlit as st
from pypinyin import pinyin, Style
import string
import re
from utils import returnCharRadical
import time

# Caching results for repeated conversions
pinyin_cache = {}
radical_cache = {}

def get_abbreviated_pinyin_with_color_break(char):
    """Get abbreviated pinyin with HTML color formatting for double consonants."""
    if char in pinyin_cache:
        return pinyin_cache[char]
    
    try:
        pin = pinyin(char, style=Style.NORMAL)[0][0]
        if pin.startswith(('zh', 'ch', 'sh')):
            result = f'<span style="color: DarkTurquoise">{pin[:2]}</span>'
        elif pin[0] in 'aeiou':
            result = pin[0]
        else:
            result = pin[0]
        pinyin_cache[char] = result
        return result
    except IndexError:
        return char  # Return the character itself if conversion fails

def get_abbreviated_pinyin_with_color(char):
    """Get abbreviated pinyin with Streamlit color formatting."""
    if char in pinyin_cache:
        return pinyin_cache[char]
    
    try:
        pin = pinyin(char, style=Style.NORMAL)[0][0]
        if pin.startswith(('zh', 'ch', 'sh')):
            result = f':blue[{pin[:2]}]'
        elif pin[0] in 'aeiou':
            result = pin[0]
        else:
            result = pin[0]
        pinyin_cache[char] = result
        return result
    except IndexError:
        return char

def convert_text(text, type=1):
    """Convert text based on the specified type: Pinyin, Radical, or Original."""
    result = []
    for char in text:
        if char in string.punctuation or char.isspace():
            result.append(char)
        else:
            if type == 1:
                result.append(get_abbreviated_pinyin_with_color_break(char))
            elif type == 0:
                result.append(get_abbreviated_pinyin_with_color(char))
            elif type == 2:
                if char in radical_cache:
                    result.append(radical_cache[char])
                else:
                    radical = returnCharRadical(char)
                    radical_cache[char] = radical
                    result.append(radical)
    return "".join(result)

def count_chinese_characters(text):
    """Count only Chinese characters in the given text."""
    return len([char for char in text if '\u4e00' <= char <= '\u9fff'])

def format_with_line_breaks_and_numbers(text, original_text, sentences_per_group=3):
    """Format text into groups of sentences with paragraph numbers and character counts."""
    sentences = re.split('([。！？\.\!\?][\s\n]*)', text)
    original_sentences = re.split('([。！？\.\!\?][\s\n]*)', original_text)
    
    formatted_text = ""
    current_group = []
    current_original_group = []
    paragraph_number = 1
    
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
            
            if len(current_group) == sentences_per_group or i >= len(sentences)-2:
                group_text = ''.join(current_group)
                original_group_text = ''.join(current_original_group)
                char_count = count_chinese_characters(original_group_text)
                
                formatted_text += f"""<span class="label-group">
                    <span class="paragraph-number">P{paragraph_number:02d}</span
                    ><span class="char-count">{char_count} chars</span>
                </span>{group_text}<br><br>"""
                
                current_group.clear()
                current_original_group.clear()
                paragraph_number += 1
    
    return formatted_text.strip()

# Streamlit Interface
st.title("Chinese to Abbreviated Pinyin Converter")

input_text = st.text_area("Enter Chinese text:", "")

if input_text.strip():
    st.sidebar.title("Settings")
    
    # Dynamic sentence grouping slider
    sentences_per_group = st.sidebar.slider("Sentences per group:", min_value=1, max_value=5, value=3)
    
    # Output type selection
    output_type = st.sidebar.radio("Select Output Type:", ["Pinyin", "Radical"], index=0)
    
    # Timer for performance monitoring
    start_time = time.time()
    
    type_mapping = {"Pinyin": 1, "Radical": 2}
    output_text = convert_text(input_text, type_mapping[output_type])
    
    st.subheader(f"Converted Text ({output_type}):")
    st.markdown(output_text, unsafe_allow_html=True)
    
    total_chars = count_chinese_characters(input_text)
    
    st.markdown(f"### Recite Helper ({total_chars} chars)")
    formatted_output = format_with_line_breaks_and_numbers(output_text, input_text, sentences_per_group)
    st.markdown(formatted_output, unsafe_allow_html=True)
    
    elapsed_time = time.time() - start_time
    st.sidebar.write(f"Processing Time: {elapsed_time:.2f} seconds")
