"""
Compares the data from the Amino_acid_biosynthesis_with_bold_headings xlsx file and gene_result.txt
"""
import format_gene_result as gr
import format_amino_reference as ar


def compare(source1, source2):
    gene_dataframe = gr.format_gene_result(source1)
    amino_dataframe = ar.amino_acid_dataframe(source2)

    combined = gene_dataframe.merge(
        amino_dataframe,
        left_on='Alias2',
        right_on='GeneId',
        how='left'
    )

    return combined


# combined_dataset = compare('Input_Files/gene_result.txt')
# print(combined_dataset.to_string())
