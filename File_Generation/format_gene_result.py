"""
Extracts the data from the gene result text file into a dataframe
"""
import pandas as pd
import re


# Creating a function to extract and manipulate data from source file
def format_gene_result(source_path):
    # Opening the source text file
    with open(source_path, 'r', encoding='utf-8') as src:
        """
        After reading each line, extracts a block as soon as it gets a blank new line.
        Using split to extract the block and create lists of blocks.
        """
        content = src.read()
        blocks = content.strip().split('\n\n')
        records = []

        # Iterating though each block from blocks list
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                raw_gene_name = lines[0].strip()
                r"""
                Replace with nothing, where the pattern matches using re.sub.
                The pattern, ^ matches the starting of the string, meaning the pattern should be at the start, if it is
                anywhere else, that is not matched.
                '\d+' matches if there is one or more digits.
                '\.' matches actual dot character in string
                '\s*' matches if any whitespace character.
                It will check any of the patters are matching from the starting of the string and if yes, then replaces
                with ''.
                """
                gene_name = re.sub(r'^\d+\.\s*', '', raw_gene_name)

                # Replace used to remove the term Other Aliases from the string
                other_aliases = lines[2].strip().replace('Other Aliases: ', '')
                final_aliases = [alias.strip() for alias in other_aliases.split(',')]

                while len(final_aliases) < 3:
                    final_aliases.append('')

                # Creating a list of tuples
                records.append((gene_name, final_aliases[0], final_aliases[1], final_aliases[2]))

    # Create DataFrame
    gene_primary_result = pd.DataFrame(records, columns=['Gene_Name', 'Alias1', 'Alias2', 'Alias3'])
    gene_primary_result.index.name = 'Sl.No'

    return gene_primary_result

    # Write to Excel
    # df.index = range(1, len(df)+1)
    # df.to_excel(r'Output_Files\Gene_Primary_Result.xlsx', index=True, index_label='Sl_No')
    # print("Excel file write completed.....")

# gene_results = format_gene_result('Input_Files/gene_result.txt')
# print(gene_results.to_string())
