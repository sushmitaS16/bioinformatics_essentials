#!/usr/bin/python
'''
Script to identify set of genes/transcripts from a countmatrix in the annotation file
@sushmitaS16
'''
import sys
import re
import argparse
import pandas as pd
import numpy as np 


def getFeatureNames(annotation_data):
	''' function to add an additional column in the annotation table with the feature name (obtained from the 'attribute' column) '''

	# from the annotation df take the 'attribute' col as a list
	attr = annotation_data['attribute']
	attr_len = len(attr)
	feature_names = []

	for i in range(0, attr_len):
		attr_info = attr[i].split(";") # split on semicolon to form a new list
		# obtain the 'gene_name' from this newly formed list (name is usually the 2nd or 3rd element in this list; check to make sure)
		for ele in attr_info:
			val = re.findall('Name', ele) #select the element with 'Name' in it ('Name' may vary from one gff file to other)
			if len(val) != 0:
				n = attr_info.index(ele)
				gene_with_name = attr_info[n]	# or attr_info[2]; attr_info[0] is almost always the 'ID'
				gene = gene_with_name.split("=")	# or gene_with_name.split(" ")
				feature_names.append(gene[1])
			else:
				pass

	annotation_data['feature_names'] = feature_names

	return annotation_data


def savefile(annotation_data, fwd_annotation_data, rev_annotation_data, outfile):
	''' function to save relevant files '''
	files_toSave = input("Whether forward/reverse strand based seperation required (y/n)? :  ")

	if files_toSave == 'y' or files_toSave == 'Y':
		annotation_data.to_csv(outfile + '.csv', sep='\t', index=False)
		fwd_annotation_data.to_csv(outfile + '.forward_strand' + '.csv', sep='\t', index=False)
		rev_annotation_data.to_csv(outfile + '.reverse_strand' + '.csv', sep='\t', index=False)
		print("**** 3 files successfully extracted! ****")

	elif files_toSave == 'n' or files_toSave == 'N':
		annotation_data.to_csv(outfile + '.csv', sep='\t', index=False)
		print("**** 1 file successfully extracted! ****")


def main():

	desc = "Script to identify set of genes/transcripts from a list in the annotation file"

	#initialize parser
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument("-a", "--annotation", help="Input gene/transcript annotation file (in dataframe format) (.csv)", type=argparse.FileType('r+'))
	parser.add_argument("-f", "--features", help="Input countmatrix of genes/transcripts to be identified (.txt/.csv)", type=argparse.FileType('r+'))
	parser.add_argument("-o", "--outfile", help="Output file with genes/transcripts of interest")

	# read arguments from command line
	args = parser.parse_args()

	# defining the inputs
	anno = args.annotation
	feats = args.features
	out_df = args.outfile

	anno_df = pd.read_csv(anno, sep='\t')
	feats_df = pd.read_csv(feats, sep='\t')

	anno.close()
	feats.close()

	modified_anno_df = getFeatureNames(anno_df)
	feats_list = feats_df.iloc[:,0]
	#print("modified annotation dataframe : \n", modified_anno_df.head())
	print("\nlist of feature names : \n", feats_list.head())

	# extract out rows specific rows
	new_anno_df = modified_anno_df[modified_anno_df.feature_names.isin(feats_list)]
	#print("\nnew annotation dataframe : \n", new_anno_df.head())


	# separate the new dataframe based on sequence strandedness
	forward_df = new_anno_df[new_anno_df.strand == '+']
	reverse_df = new_anno_df[new_anno_df.strand == '-']

	savefile(new_anno_df, forward_df, reverse_df, out_df)

	return 0


if __name__ == "__main__":
	main()
