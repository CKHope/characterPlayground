import streamlit as st
import json
import csv
from io import StringIO
import pandas as pd

# Load the full character data from dictionary.txt.
@st.cache_data
def load_hanzi_data():
    mapping = {}
    try:
        with open("dictionary.txt", "r", encoding="utf8") as file:
            # Each line in dictionary.txt is a JSON object representing one character.
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

# Load the data once per session.
hanzi_mapping = load_hanzi_data()

def process_text(text):
    """
    For each non‑whitespace character in the input text, look up the full record.
    Also, build the union of keys across all records to form table columns.
    """
    rows = []
    headers_set = set()
    for ch in text:
        if ch.strip():
            record = hanzi_mapping.get(ch)
            # If the character is not found, create a minimal record.
            if record is None:
                record = {"character": ch}
            rows.append(record)
            headers_set.update(record.keys())
    headers = sorted(list(headers_set))
    return rows, headers

st.title("Chinese Character Full Data Lookup")
st.write(
    "Enter Chinese text below. For every non‑whitespace character, the app retrieves its full record from "
    "dictionary.txt. Each field (such as 'character', 'radical', 'pinyin', etc.) is shown as a separate column. "
    "You can view the results in a table and download them as a CSV file (with UTF‑8 BOM to ensure proper display)."
)

text_input = st.text_area("Enter Chinese text:", height=300)

if st.button("Generate Table and CSV"):
    if not text_input.strip():
        st.warning("Please enter some text to process.")
    else:
        rows, headers = process_text(text_input)
        if not rows:
            st.error("No characters were processed from the input.")
        else:
            # Build a list of rows where each row is a list of string values corresponding to each header.
            data = []
            for record in rows:
                row = []
                for key in headers:
                    value = record.get(key, "")
                    # For nested types (lists, dicts), convert to JSON string so everything is uniform.
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value, ensure_ascii=False)
                    else:
                        value = str(value)
                    row.append(value)
                data.append(row)
            
            # Create DataFrame and convert all columns to string (workaround for pyarrow conversion issues).
            df = pd.DataFrame(data, columns=headers)
            df = df.astype(str)
            
            # Display the DataFrame.
            st.dataframe(df)
            
            # Prepare CSV content using a StringIO buffer.
            # Write a Byte Order Mark (BOM) so Excel correctly displays Unicode Chinese characters.
            csv_buffer = StringIO()
            csv_buffer.write('\ufeff')
            writer = csv.writer(csv_buffer)
            writer.writerow(headers)
            writer.writerows(data)
            csv_content = csv_buffer.getvalue()
            
            st.download_button(
                label="Download CSV",
                data=csv_content,
                file_name="character_full_data.csv",
                mime="text/csv"
            )
            st.success("Data table generated and CSV file is ready for download!")
