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
            # Each line in dictionary.txt is a JSON object describing a character.
            for line in file:
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        ch = record.get("character")
                        if ch:
                            mapping[ch] = record
                    except Exception:
                        # Skip any lines that fail to parse
                        continue
    except FileNotFoundError:
        st.error("dictionary.txt not found. Please download it from the Make Me a Hanzi repository and place it in the same directory as this app.")
    return mapping

hanzi_mapping = load_hanzi_data()

def process_text(text):
    """
    Processes each non‑whitespace character in the input text,
    looks up its full record in hanzi_mapping, and gathers all keys encountered.
    """
    rows = []
    headers_set = set()
    for ch in text:
        if ch.strip():
            # Look up the record from dictionary.txt.
            record = hanzi_mapping.get(ch)
            if record is None:
                # If the character is not in the dictionary, return a record with only the character.
                record = {"character": ch}
            rows.append(record)
            headers_set.update(record.keys())
    # Convert the set of keys into a sorted list (you can modify this order as needed)
    headers = sorted(list(headers_set))
    return rows, headers

st.title("Chinese Character Data Lookup")
st.write(
    "Enter a paragraph of Chinese text below. For every non‑whitespace character, "
    "the app retrieves its full data from the dictionary.txt file (from the Make Me a Hanzi project) and displays "
    "all fields in a table. You can then download the data as a CSV file."
)

text_input = st.text_area("Enter Chinese text here:", height=300)

if st.button("Generate Table and CSV"):
    if not text_input.strip():
        st.warning("Please enter some text to process.")
    else:
        rows, headers = process_text(text_input)
        if not rows:
            st.error("No characters found in the input.")
        else:
            # Build rows with values for all headers (missing keys become empty strings)
            data = []
            for record in rows:
                row = []
                for key in headers:
                    value = record.get(key, "")
                    if isinstance(value, dict):
                        # Convert nested dictionaries to a JSON string for display
                        value = json.dumps(value, ensure_ascii=False)
                    row.append(value)
                data.append(row)

            # Display the results in a table using a pandas DataFrame.
            df = pd.DataFrame(data, columns=headers)
            st.dataframe(df)

            # Prepare CSV content with a UTF‑8 BOM (so Chinese characters display properly in Excel).
            csv_buffer = StringIO()
            csv_buffer.write('\ufeff')  # BOM for UTF-8
            writer = csv.writer(csv_buffer)
            writer.writerow(headers)
            writer.writerows(data)
            csv_content = csv_buffer.getvalue()

            st.download_button(
                label="Download CSV",
                data=csv_content,
                file_name="character_data.csv",
                mime="text/csv"
            )
            st.success("Data table generated and CSV file is ready for download!")
