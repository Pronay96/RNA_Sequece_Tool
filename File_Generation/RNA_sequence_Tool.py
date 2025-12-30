import os
from sys import argv
import compare_genes_amino as cga

import format_gene_result

if __name__ == "__main__":
    if len(argv) != 5:
        print("Usage: python script_name.py <source_file_path1> <source_file_path2> <source_file_path3> <destination_file_path>")
    source_path_gene = os.path.abspath(argv[1])
    source_path_amino = os.path.abspath(argv[2])
    source_path_reference = os.path.abspath(argv[3])
    destination_path = os.path.abspath(argv[4])

    final_dataset = cga.compare(source_path_gene, source_path_amino, source_path_reference)

    # Writing to excel
    final_dataset.index = range(1, len(final_dataset) + 1)
    final_dataset.to_excel(destination_path, na_rep='N/A', index=True, index_label='Sl_No')
    print("Excel file write completed.....")
