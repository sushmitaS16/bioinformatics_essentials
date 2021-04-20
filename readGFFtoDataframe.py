#!/usr/bin/python
''' 
Usage : python3 gffReader.py [-h] [-i INFILE] [-o OUTFILE] 
@sushmitaS16
'''

import sys
import re
import argparse
import pandas as pd


class _GFFModifier(object):
	''' this class takes a gff/gff3 file as input, 
	transforms it into a pandas dataframe for more accessibility, 
	and then modifies it based on user preference '''

	def __init__(self):
		super(_GFFModifier, self).__init__()


	def modify_gff3(self, infile):
		''' this will remove comment lines (if any) from the gff file '''
		with open(infile, 'r+') as f:
			line = f.readlines()
			f.seek(0)
			for i in line:
				if not re.findall("^#", i):
					f.write(i)

			f.truncate()

		return self.read_gff3_to_dataframe(infile)



	def read_gff3_to_dataframe(self, infile):
		''' this function will read the gff3 and convert it into dataframe '''
		file = open(infile, "r+")
		df = pd.read_csv(file, header=None, sep='\t', names=["chrom","origin","type","start","end","score","strand","phase","attributes"])

		file.close()

		return df


	def extract_by_type(self, df):
		''' based on which 'type' of sequence one needs extract the necessary dataframe '''
		print(df.type.unique())
		#["gene","CDS","mRNA","exon","five_prime_UTR","three_prime_UTR","rRNA","tRNA","ncRNA","tmRNA","transcript","mobile_genetic_element","origin_of_replication","promoter","repeat_region"]
		chosen_type = input("Type of sequences required: ")

		# extract out rows with the chosen type
		new_df = df[df.type == chosen_type]

		return new_df



	def extract_by_strand(self, df):
		''' based on which 'stranded' sequences one needs extract the necessary dataframe '''
		print(df.strand.unique())
		chosen_str = input("+/- sequences required: ")

		# extract out rows with the chosen strand
		new_df = df[df.strand == chosen_str]

		return new_df



def main():

	msg = "Script to modify a given gff file and extract specific features"

	# initialize parser
	parser = argparse.ArgumentParser(description=msg)
	parser.add_argument("-i", "--infile", help="Input annotation file to be processed (.gff/.gff3)")
	parser.add_argument("-o", "--outfile", help="Output tab-delimited file with feature data (.csv)")


	# read arguments from command line
	args = parser.parse_args()

	# processing the input
	annotation = args.infile

	gff_modifier = _GFFModifier()
	df = gff_modifier.modify_gff3(annotation)

	#print(df)


	# extract user-specific feature data
	_user_input_feat = input("'type' / 'strand' of sequence based extraction (t/s): ")

	if _user_input_feat == 'type' or _user_input_feat == 't':
		user_df = gff_modifier.extract_by_type(df)
	elif _user_input_feat == 'strand' or _user_input_feat == 's':
		user_df = gff_modifier.extract_by_strand(df)
	else:
		print("Nothing specified!")
		pass

	user_df.to_csv(args.outfile, sep='\t', index=False)
	print("***** Extraction successful! *****")

	return None

if __name__ == "__main__":
	main()