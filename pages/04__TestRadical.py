import streamlit as st
import json
import csv
from io import StringIO
import pandas as pd

# Load the Make Me a Hanzi data from dictionary.txt
@st.cache_data
def load_hanzi_data():
    mapping = {}
    try:
        with open("dictionary.txt", "r", encoding="utf8") as file:
            # Each line is a JSON object for one character.
            for line in file:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        char = entry.get("character")
                        # Use the field "radical" provided in the data.
                        radical = entry.get("radical", "")
                        if char:
                            mapping[char] = radical
                    except Exception:
                        # Skip lines that fail to parse.
                        continue
    except FileNotFoundError:
        st.error("dictionary.txt not found. Please download it from the Make Me a Hanzi repository and place it in the same directory.")
    return mapping

hanzi_mapping = load_hanzi_data()

def get_kangxi_radical(character):
    """
    Look up the radical for the given character.
    Returns an empty string if not found.
    """
    return hanzi_mapping.get(character, "")

def process_paragraph(text):
    """
    Process each non‑whitespace character in the text and return
    a list of [character, radical] pairs.
    """
    pairs = []
    for ch in text:
        if ch.strip():
            radical = get_kangxi_radical(ch)
            pairs.append([ch, radical])
    return pairs

# Streamlit App UI
st.title("Chinese Kangxi Radical Lookup")
st.write(
    "Enter a paragraph of Chinese text below. The app will look up each character's "
    "radical and display the results in a table. You can also download the results as a CSV file. "
    "The CSV is encoded with a UTF-8 BOM so that Chinese characters appear correctly in programs like Excel."
)

text_paragraph = st.text_area("Enter Chinese text here:", height=300)

if st.button("Generate CSV and Show Table"):
    if not text_paragraph.strip():
        st.warning("Please enter some text to process.")
    else:
        data_pairs = process_paragraph(text_paragraph)
        if not data_pairs:
            st.error("No characters were found in the input.")
        else:
            # Display the results in a table using a pandas DataFrame.
            df = pd.DataFrame(data_pairs, columns=["Character", "Kangxi Radical"])
            st.dataframe(df)

            # Prepare CSV data: add the UTF-8 BOM so that Excel displays Chinese correctly.
            csv_buffer = StringIO()
            csv_buffer.write('\ufeff')  # Write BOM header
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
