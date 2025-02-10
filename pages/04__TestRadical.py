import streamlit as st
import json
import csv
import unicodedata
from io import StringIO
import pandas as pd
from typing import Dict, Any

# ========================================================
# Data Loading and Utility Functions
# ========================================================

@st.cache_data
def load_hanzi_data():
    """
    Load and parse the Make Me a Hanzi dictionary data from dictionary.txt.
    If an 'etymology' field is present, it is flattened so that each key becomes
    a new field prefixed with 'etymology_'.
    Additional processing:
      - If etymology_hint contains " also provides the pronunciation" and
        etymology_phonetic is empty, automatically extract the character immediately preceding the phrase 
        (ignoring whitespace) and assign it to etymology_phonetic.
      - If etymology_semantic is empty, assign the radical to etymology_semantic.
    """
    mapping = {}
    try:
        with open("dictionary.txt", "r", encoding="utf8") as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        ch = record.get("character")
                        if ch:
                            if "etymology" in record:
                                etymology = record.pop("etymology")
                                if isinstance(etymology, dict):
                                    for key, value in etymology.items():
                                        record[f"etymology_{key}"] = value

                            # Check etymology_hint for phonetic info.
                            if "etymology_hint" in record and isinstance(record["etymology_hint"], str):
                                hint_str = record["etymology_hint"]
                                if " also provides the pronunciation" in hint_str:
                                    # Only add phonetic info if etymology_phonetic is empty.
                                    if not record.get("etymology_phonetic", "").strip():
                                        idx = hint_str.find(" also provides the pronunciation")
                                        j = idx - 1
                                        # Skip any whitespace before the phrase.
                                        while j >= 0 and hint_str[j].isspace():
                                            j -= 1
                                        if j >= 0:
                                            record["etymology_phonetic"] = hint_str[j]

                            # If etymology_semantic is empty, use the radical.
                            if not record.get("etymology_semantic", "").strip():
                                radical = record.get("radical", "").strip()
                                if radical:
                                    record["etymology_semantic"] = radical

                            mapping[ch] = record
                    except Exception:
                        continue
    except FileNotFoundError:
        st.error("dictionary.txt not found. Please download it from the Make Me a Hanzi repository and place it with this app.")
    return mapping

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Flatten a nested dictionary so that each nested key is appended to the parent key.
    For instance, {'a': {'b': 1}} becomes {'a_b': 1}.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def process_text(text, hanzi_mapping):
    """
    Process the input text by:
      • Extracting unique characters (ignoring whitespace and punctuation; order preserved)
      • For each character, obtaining its full (flattened) record.
    Returns a list of records (rows) and the union of keys (headers) encountered.
    """
    unique_chars = []
    seen = set()
    for ch in text:
        if ch.isspace():
            continue
        if unicodedata.category(ch).startswith("P"):
            continue
        if ch not in seen:
            seen.add(ch)
            unique_chars.append(ch)
    
    rows = []
    headers_set = set()
    for ch in unique_chars:
        record = hanzi_mapping.get(ch)
        if record is None:
            record = {"character": ch}
        # Flatten any nested dictionaries in the record.
        flat_record = {}
        for key, value in record.items():
            if isinstance(value, dict):
                flat_record.update(flatten_dict(value, key))
            else:
                flat_record[key] = value
        rows.append(flat_record)
        headers_set.update(flat_record.keys())
    
    headers = sorted(list(headers_set))
    if 'character' in headers:
        headers.remove('character')
        headers = ['character'] + headers
    return rows, headers

# ========================================================
# Load Data
# ========================================================
hanzi_mapping = load_hanzi_data()

# ========================================================
# Streamlit User Interface
# ========================================================
st.title("Chinese Character Data Lookup")
st.write(
    "Enter a paragraph of Chinese text below. The app will extract each unique character "
    "(excluding punctuation and whitespace), look up its complete record (with etymology details flattened), "
    "and display all the data in one table. You can also download the full data as a CSV file."
)

text_input = st.text_area("Enter Chinese text here:", height=300)

if st.button("Analyze Characters"):
    if not text_input.strip():
        st.warning("Please enter some text to process.")
    else:
        # Process the input text and obtain full records.
        rows, headers = process_text(text_input, hanzi_mapping)
        
        # Convert all values to strings for display and CSV export.
        data = []
        for record in rows:
            row = []
            for key in headers:
                value = record.get(key, "")
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                else:
                    value = str(value) if value is not None else ""
                row.append(value)
            data.append(row)
        
        # Create a DataFrame for display.
        df = pd.DataFrame(data, columns=headers).astype(str)
        df = df.replace('None', '')
        
        st.subheader("Character Data")
        st.dataframe(df)
        
        # Prepare CSV content with a UTF-8 BOM for proper Unicode handling.
        csv_buffer = StringIO()
        csv_buffer.write('\ufeff')
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
        st.success("Analysis complete!")
