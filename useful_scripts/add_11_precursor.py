import fileinput
import os
import sys

#guillem ylla september 2014
##python2.7 in.gff3 > out_gff3_+11_on_precursor

str(sys.argv)
filenames=sys.argv[1]







with open(filenames, 'r') as inF:
	#inF.readline() # skip first line
	for line2 in inF:
		if "miRNA" in line2:
			clean_line_2=line2.strip()
			splitted= clean_line_2.split("\t") 
			scaffold=splitted[2]
			strand=splitted[6]
			pr_i=splitted[3]
			pr_e=splitted[4]
			pr_i_new=int(pr_i)-11
			pr_e_new=int(pr_e)+11

			#print splitted[0]+"\t"+splitted[1]+"\t"+splitted[2]+"\t"+str(pr_i_new)+"\t"+str(pr_e_new)+"\t"+splitted[5]+"\t"+splitted[6]+"\t"+splitted[7]+"\t"+splitted[8].split("--")[0]+"-prec+_11"
			print splitted[0]+"\t"+splitted[1]+"\t"+splitted[2]+"\t"+str(pr_i_new)+"\t"+str(pr_e_new)+"\t"+splitted[5]+"\t"+splitted[6]+"\t"+splitted[7]+"\t"+splitted[8]+"-prec+_11"

		else:
			print line2

