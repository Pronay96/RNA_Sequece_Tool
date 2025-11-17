"""
Extracts the data from the Amino_acid_biosynthesis_with_bold_headings xlsx file into a dataframe
"""
import pandas as pd


def extract_block(source):
    # Identify separator rows where BOTH columns are NaN
    reference_data = pd.read_excel(source)
    col1 = reference_data.iloc[:, 0]
    col2 = reference_data.iloc[:, 1]
    sep = col1.isna() & col2.isna()

    # Split into blocks
    blocks = []
    start = 0
    for idx, is_sep in enumerate(sep):
        if is_sep:
            block = reference_data.iloc[start:idx].dropna(how='all')
            if not block.empty:
                blocks.append(block)
            start = idx + 1

    # Capture the final block(because it has no blank row at the end)
    last_block = reference_data.iloc[start:].dropna(how='all')
    if not last_block.empty:
        blocks.append(last_block)
    return blocks


def process_block(block):
    # Reset index to avoid mismatch
    block = block.reset_index(drop=True)

    # Extracting the heading
    main_heading = block.columns[0]

    # Extract sub heading safely
    if len(block) > 1:
        sub_heading = block.iloc[0, 0]
    else:
        sub_heading = None

    # Extract gene rows
    if len(block) >= 2:
        data_rows = block.iloc[1:]
    else:
        # No gene rows — return empty df
        return pd.DataFrame(columns=["GeneId", "MainHeading", "SubHeading", "Description"])

    # General function to format any block from blocks
    formatted = pd.DataFrame({
        "GeneId": data_rows.iloc[:, 0].values,
        "MainHeading": main_heading,
        "SubHeading": sub_heading,
        "Description": data_rows.iloc[:, 1].values
    })
    return formatted


def amino_acid_dataframe(source):
    blocks = extract_block(source)
    final_list = []
    for block in blocks:
        # Calling the process_block function for each block for formatting
        formatted_list = process_block(block)
        final_list.append(formatted_list)

    amino_acid_dataframe_result = pd.concat(final_list, ignore_index=True)
    amino_acid_dataframe_result.index.name = 'Sl.No'
    return amino_acid_dataframe_result


# amino_acid_df = amino_acid_dataframe()
# print(amino_acid_df.to_string())
# blocks = extract_block()
# print(process_block(blocks[108]).to_string(index=False))
# print(blocks[6].reset_index(drop=True), len(blocks[6]), sep='\n')
