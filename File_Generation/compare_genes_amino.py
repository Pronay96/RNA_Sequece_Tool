"""
Compares the data from the Amino_acid_biosynthesis_with_bold_headings xlsx file and gene_result.txt
Reference it with the final sample for complete result
"""
import pandas as pd
import format_gene_result as gr
import format_amino_reference as ar


def compare(source1, source2, source3):
    gene_dataframe = gr.format_gene_result(source1)
    amino_dataframe = ar.create_amino_acid_dataframe(source2)

    combined = gene_dataframe.merge(
        amino_dataframe,
        left_on='Alias2',
        right_on='GeneId',
        how='left'
    )

    final_reference_dataframe = pd.read_excel(source3, header=1)
    formated_reference_dataframe = final_reference_dataframe.loc[:,['ID', 'log2FoldChange', 'pvalue', 'padj']]
    # print(formated_reference_dataframe.to_string())

    # Adding a temporary order column
    combined['_order'] = range(len(combined))

    # Merge on Alias1
    m1 = combined.merge(
        formated_reference_dataframe,
        left_on='Alias1',
        right_on='ID',
        how='left'
    )

    # Merge on Alias2
    m2 = combined.merge(
        formated_reference_dataframe,
        left_on='Alias2',
        right_on='ID',
        how='left'
    )

    # Combine columns (Alias1 → Alias2 fallback)
    final_combined = combined.copy()

    for col in ['log2FoldChange', 'pvalue', 'padj']:
        final_combined[col] = (
            m1[col].combine_first(m2[col])
        )

    # Restore original order & cleanup
    final_combined = (
        final_combined.sort_values('_order').drop(columns=['_order']).reset_index(drop=True)
    )

    final_combined = final_combined.dropna(subset=['log2FoldChange', 'pvalue', 'padj'],how='all')

    return final_combined


# combined_dataset = (
# final_combined_df = compare('Input_Files/gene_result.txt',
#                        'Input_Files/List_of_Vibrio_genes.xlsx',
#                        'Input_Files/Sample_Gene_Reference.xlsx')
#
# final_combined_df.to_excel('Output_Files/test.xlsx', na_rep='N/A', index=True, index_label='Sl_No')
# print("Excel file write completed.....")
