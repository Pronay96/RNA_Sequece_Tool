from sys import argv
import pandas as pd
import re
import os

def copy_file_content_to_excel(source_path, destination_path):
    with open(source_path, 'r', encoding='utf-8') as src:
        content = src.read()
        blocks = content.strip().split('\n\n')
        records = []

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                raw_gene_name = lines[0].strip()
                gene_name = re.sub(r'^\d+\.\s*', '', raw_gene_name)

                other_aliases = lines[2].strip().replace('Other Aliases: ', '')
                final_aliases = [alias.strip() for alias in other_aliases.split(',')]

                while len(final_aliases) < 3:
                    final_aliases.append('')

                records.append((gene_name, final_aliases[0], final_aliases[1], final_aliases[2]))

    # Create DataFrame
    df = pd.DataFrame(records, columns=['Gene Name', 'Alias1', 'Alias2', 'Alias3'])

    # Write to Excel
    df.to_excel(destination_path, index=False)
    print("Excel file write completed.....")


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python script_name.py <source_file> <destination_file>")
    source_path = os.path.abspath(argv[1])
    destination_path = os.path.abspath(argv[2])
    copy_file_content_to_excel(source_path, destination_path)
