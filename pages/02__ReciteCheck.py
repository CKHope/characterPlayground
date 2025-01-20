# import streamlit as st
# from difflib import ndiff

# def compare_texts(text_a, text_b):
#     # Perform character-level comparison
#     diff = list(ndiff(text_a, text_b))
#     html_diff = ''
#     incorrect_count = 0
    
#     for s in diff:
#         if s.startswith('+ '):
#             html_diff += f'<span style="background-color: #b22222;">{s[2:]}</span>'
#         elif s.startswith('- '):
#             html_diff += f'<span style="background-color: #000080;">{s[2:]}</span>'
#             incorrect_count += 1
#         else:
#             html_diff += s[2:]
    
#     return html_diff, incorrect_count

# st.title("Text Comparison App")

# st.write("Enter the original text (Text A) and the text to compare (Text B) to highlight the differences.")

# # Descriptions for highlight colors
# st.markdown("""
# **Legend:**
# - <span style="background-color: #000080; color: white;">Original text (Navy)</span>
# - <span style="background-color: #b22222; color: white;">Incorrect text (Fire Brick)</span>
# """, unsafe_allow_html=True)

# text_a = st.text_area("Original Text (Text A)", height=200)
# text_b = st.text_area("Text to Compare (Text B)", height=200)

# if st.button("Compare"):
#     if text_a and text_b:
#         comparison_result, incorrect_count = compare_texts(text_a, text_b)
#         st.markdown(f'<div style="white-space: pre-wrap; font-family: monospace;">{comparison_result}</div>', unsafe_allow_html=True)
        
#         # Display summary of incorrect characters
#         st.write(f"**Summary:** There are {incorrect_count} incorrect character(s) in Text B compared to Text A.")
#     else:
#         st.error("Please enter text in both Text A and Text B areas.")

import streamlit as st
from difflib import ndiff

def compare_texts(text_a, text_b):
    # Perform character-level comparison
    diff = list(ndiff(text_a, text_b))
    html_diff = ''
    incorrect_count = 0
    
    for s in diff:
        if s.startswith('+ '):
            html_diff += f'<span style="background-color: #b22222; font-size: 130%;">{s[2:]}</span>'
        elif s.startswith('- '):
            html_diff += f'<span style="background-color: #000080; font-size: 130%;">{s[2:]}</span>'
            incorrect_count += 1
        else:
            html_diff += s[2:]
    
    return html_diff, incorrect_count

st.title("Text Comparison App")

st.write("Enter the original text (Text A) and the text to compare (Text B) to highlight the differences.")

# Descriptions for highlight colors
st.markdown("""
**Legend:**
- <span style="background-color: #000080; color: white; font-size: 130%;">Original text (Navy)</span>
- <span style="background-color: #b22222; color: white; font-size: 130%;">Incorrect text (Fire Brick)</span>
""", unsafe_allow_html=True)

text_a = st.text_area("Original Text (Text A)", height=200)
text_b = st.text_area("Text to Compare (Text B)", height=200)

if st.button("Compare"):
    if text_a and text_b:
        comparison_result, incorrect_count = compare_texts(text_a, text_b)
        st.markdown(f'<div style="white-space: pre-wrap; font-family: monospace;">{comparison_result}</div>', unsafe_allow_html=True)
        
        # Display summary of incorrect characters
        st.write(f"**Summary:** There are {incorrect_count} incorrect character(s) in Text B compared to Text A.")
    else:
        st.error("Please enter text in both Text A and Text B areas.")
