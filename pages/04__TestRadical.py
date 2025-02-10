import streamlit as st
import json
import csv
from io import StringIO

# Load the Make Me a Hanzi dictionary data from dictionary.txt
@st.cache_data
def load_hanzi_data():
    mapping = {}
    try:
        with open("dictionary.txt", "r", encoding="utf8") as file:
            # Each line in dictionary.txt is a JSON object.
            for line in file:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        char = entry.get("character")
                        # Use the "radical" field provided in the data.
                        radical = entry.get("radical", "")
                        if char:
                            mapping[char] = radical
                    except Exception as e:
                        # Skip lines that fail to parse.
                        continue
    except FileNotFoundError:
        st.error("dictionary.txt not found. Please download it from the Make Me a Hanzi repository and place it in the same directory as this app.")
    return mapping

hanzi_mapping = load_hanzi_data()

def get_kangxi_radical(character):
    """
    Look up the radical for a given character using the preloaded data.
    Returns an empty string if no entry is found.
    """
    return hanzi_mapping.get(character, "")

def process_paragraph(text):
    """
    Process each non-whitespace character in the provided text,
    and return a list of [character, radical] pairs.
    """
    pairs = []
    for ch in text:
        if ch.strip():
            radical = get_kangxi_radical(ch)
            pairs.append([ch, radical])
    return pairs

# Streamlit App UI
st.title("Chinese Kangxi Radical Lookup")
st.write("Paste a paragraph of Chinese text below. The app will look up each character’s radical "
         "(using Make Me a Hanzi's dictionary.txt data) and generate a downloadable CSV file.")

text_paragraph = st.text_area("Enter Chinese text here:", height=300)

if st.button("Generate CSV"):
    if not text_paragraph.strip():
        st.warning("Please enter some text to process.")
    else:
        data_pairs = process_paragraph(text_paragraph)
        if not data_pairs:
            st.error("No characters were found in the input.")
        else:
            # Create CSV in memory.
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
