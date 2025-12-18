"""
Extracts the data from the Amino_acid_biosynthesis_with_bold_headings xlsx file into a dataframe
"""
import pandas as pd


# Block Extraction based on header column
def extract_header_blocks(dataframe):
    block_list = []
    start = 0

    # Finding the empty rows
    empty_rows = dataframe.isna().all(axis=1)

    # Find the point where the blocks should split
    split_points = empty_rows & empty_rows.shift(1)

    # Splitting and appending the blocks with 2 empty rows
    # split_points[split_points] means split_points[ split_points == True ]
    for index in split_points[split_points].index:
        block = dataframe.iloc[start:index-1]
        if not block.empty:
            block_list.append(block.reset_index(drop=True))
        start = index + 1

    # Appending the last block
    last_block = dataframe.iloc[start:]
    if not last_block.empty:
        block_list.append(last_block.reset_index(drop=True))

    return block_list

# Formating 1st column for each block
def format_header_column(listed_blocks):
    # Formating all the rows for column 0 with header column
    for block in listed_blocks:
        header_value = block.iloc[0 ,0]
        block.iloc[:,0] = block.iloc[:,0].fillna(header_value)

    return listed_blocks

# Block Extraction based on subheading column
def extract_subheader_block(formated_blocks):
    subblock = []

    for block in formated_blocks:
        start = 0
        # Finding the empty sub rows
        empty_row = block[[1, 2]].isna().all(axis=1)

        # Find the point where the sub-blocks should split
        split_points = empty_row & empty_row.shift(1).notna()

        # Splitting and appending the blocks with col1 and col2 empty row
        # split_points[split_points] means split_points[ split_points == True ]
        for index in split_points[split_points].index:
            sub_block = block.iloc[start:index]
            if not sub_block.empty:
                subblock.append(sub_block.reset_index(drop=True))
            start = index + 1

        # Appending the last block
        last_block = block.iloc[start:]
        if not last_block.empty:
            subblock.append(last_block.reset_index(drop=True))

    return subblock

def format_final(final_blocks):
    formatted_blocks = []
    for final_block in final_blocks:
        header_col = final_block.iloc[0 ,0]
        sub_header_col = final_block.iloc[0 ,1]
        # Need the least one data row
        if len(final_block) < 2:
            continue

        data_rows = final_block.iloc[1:]

        formatted = pd.DataFrame({
            "GeneId": data_rows.iloc[:, 1].values,
            "MainHeading": header_col,
            "SubHeading": sub_header_col,
            "Description": data_rows.iloc[:, 2].values
        })

        formatted_blocks.append(formatted)

    return pd.concat(formatted_blocks, ignore_index=True)


def create_amino_acid_dataframe(source):
    raw_dataframe = pd.read_excel(source, header=None)

    list_of_blocks = extract_header_blocks(raw_dataframe)
    formated_list = format_header_column(list_of_blocks)
    sub_block_list = extract_subheader_block(formated_list)
    amino_reference_dataframe = format_final(sub_block_list)

    return amino_reference_dataframe


# dataframe = create_amino_acid_dataframe('Input_Files/List of Vibrio genes.xlsx')
# dataframe.to_excel('Output_Files/Reference_Sheet.xlsx', na_rep='N/A', index=True, index_label='Sl_No')