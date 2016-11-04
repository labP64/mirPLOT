import fileinput
import os
import sys

#guillem ylla september 2014
##python2.7 in.gff3 > out_gff3_+11_on_precursor

str(sys.argv)
prec_cord=sys.argv[1]
#mat_cord=sys.argv[2]
#star_cord=sys.argv[3]
extrabases=sys.argv[2]





with open(prec_cord, 'r') as inF:
	#inF.readline() # skip first line
	for line2 in inF:
		clean_line_2=line2.strip()
		splitted= clean_line_2.split("\t") 
		scaffold=splitted[2]
		strand=splitted[6]
		pr_i=splitted[3]
		pr_e=splitted[4]
		
		pr_i_new=int(extrabases)+1
		pr_e_new=int(extrabases)+int(pr_e)-int(pr_i)+1

		name=clean_line_2.split("ID=")[1] 

		print name+"_prec"+"\t"+splitted[1]+"\t"+splitted[2]+"\t"+str(pr_i_new)+"\t"+str(pr_e_new)+"\t"+splitted[5]+"\t"+"+"+"\t"+splitted[7]+"\tID="+name+"_prec+"+str(extrabases)


