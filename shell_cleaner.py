# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 10:51:26 2025

@author: User
"""

import streamlit as st
import pandas as pd
import io

# --- Streamlit App ---
st.title("Shell Transaction File Cleaner")

# Upload CSV file
uploaded_file = st.file_uploader("Upload Shell Transaction CSV", type=["csv"])

# List of vehicle license numbers to remove
vehicles_to_remove = [
    "BLQ 8802", "BLQ 8809", "BLR 9800", "BLW 8817", "BLW 8819",
    "BND 7288", "BND 7838", "BNH 7388", "BNH 7488", "BNH 7588",
    "BNJ 7988", "PATRIOT 8308", "PATRIOT 8830", "VDT 7722",
    "VDT 7788", "VDU 3300", "VDU 9922", "VDU 9977"
]

if uploaded_file:
    # Read the uploaded CSV
    df = pd.read_csv(uploaded_file)

    # Initial record count
    st.write(f"Original rows: {len(df)}")

    # Step 2: Remove rows where 'Site Name' == 'DUMMY SITE FOR EPT'
    df = df[df['Site Name'] != 'DUMMY SITE FOR EPT']

    # Step 3: Remove rows where 'Vehicle License Number' is in the list
    df = df[~df['Vehicle License Number'].isin(vehicles_to_remove)]
    
    # Step 4: Clean whitespace in 'Vehicle License Number'
    df['Vehicle License Number'] = df['Vehicle License Number'].astype(str).str.replace(" ", "", regex=False)

    # Final record count
    st.write(f"Filtered rows: {len(df)}")

    # Prepare updated file name
    original_filename = uploaded_file.name.rsplit(".", 1)[0]
    updated_filename = f"{original_filename}_updated.csv"

    # Create CSV in memory
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    # Download button
    st.download_button(
        label="Download Updated CSV",
        data=csv_data,
        file_name=updated_filename,
        mime="text/csv"
    )
