import streamlit as st
import functools
import csv
from io import StringIO
from cjklib.characterlookup import CharacterLookup

# Initialize the lookup instance (supports both simplified and traditional Chinese)
lookup = CharacterLookup('C')

# Cache the results for faster repeated lookups.
@functools.lru_cache(maxsize=1024)
def get_kangxi_radical(character):
    result = lookup.getCharacterKangxiRadical(character)
    # If multiple forms are returned, join them by comma
    if isinstance(result, list):
        return ','.join(result)
    return result

def process_paragraph(text):
    """Process the input paragraph, returning a list of [character, radical] pairs."""
    pairs = []
    for char in text:
        if char.strip():  # skip empty or whitespace characters
            try:
                radical = get_kangxi_radical(char)
            except Exception:
                radical = None
            pairs.append([char, radical])
    return pairs

# Streamlit App UI
st.title("Chinese Kangxi Radical Lookup")
st.write("Enter a paragraph of Chinese text below. The app will generate a CSV file mapping each "
         "character to its corresponding Kangxi radical.")

text_paragraph = st.text_area("Enter Chinese text here:", height=300)

if st.button("Generate CSV"):
    if not text_paragraph:
        st.warning("Please enter some text to process.")
    else:
        data_pairs = process_paragraph(text_paragraph)
        
        # Use StringIO to create a CSV in-memory.
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Character", "Kangxi Radical"])
        writer.writerows(data_pairs)
        csv_content = csv_buffer.getvalue()
        
        st.download_button(
            label="Download CSV",
            data=csv_content,
            file_name="kangxi_radicals.csv",
            mime="text/csv"
        )
        st.success("CSV file is ready for download!")
