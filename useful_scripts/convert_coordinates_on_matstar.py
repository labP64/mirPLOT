import fileinput
import os
import sys

#guillem ylla september 2014
##python2.7 in.gff3 > out_gff3_+11_on_precursor

str(sys.argv)
seq_cord=sys.argv[1]
prec_cord=sys.argv[2]



diccin=dict()
diccend=dict()

with open(prec_cord, 'r') as inF:
	#inF.readline() # skip first line
	for line2 in inF:
		clean_line_2=line2.strip()
		splitted= clean_line_2.split("\t") 
		precend=splitted[4]
		precin=splitted[3]
		nameprec=clean_line_2.split("ID=")[1].split("+11")[0]
		diccin[nameprec]=precin
		diccend[nameprec]=precend
#print diccin


with open(seq_cord, 'r') as inF:
	#inF.readline() # skip first line
	for line2 in inF:
		clean_line_2=line2.strip()
		splitted= clean_line_2.split("\t") 
		scaffold=splitted[2]
		strand=splitted[6]
		pr_i=splitted[3]
		pr_e=splitted[4]
		
		mirid=splitted[8]
		name=clean_line_2.split("ID=")[1].split("_")[0] +"_"+clean_line_2.split("ID=")[1].split("_")[1]
		name=name+"_prec"
		#print name

		if("5p" in splitted[8] and strand=="+"):

			pr_i_new=diccin[name]
			pr_e_new=int(pr_i_new)+int(pr_e)-int(pr_i)

		
		if("3p" in splitted[8] and strand=="+"):
			#print "bbbb", strand
			pr_e_new=int(diccend[name])
			pr_i_new=int(pr_e_new)-(int(pr_e)-int(pr_i))



		if("3p" in splitted[8] and strand=="-"):
			#print "aaaa", strand
			pr_e_new=int(diccend[name])
			pr_i_new=int(pr_e_new)-(int(pr_e)-int(pr_i))


		if("5p" in splitted[8] and strand=="-"):
			pr_i_new=diccin[name]
			pr_e_new=int(pr_i_new)+int(pr_e)-int(pr_i)


		print name+"\t"+splitted[1]+"\t"+splitted[2]+"\t"+str(pr_i_new)+"\t"+str(pr_e_new)+"\t"+splitted[5]+"\t"+"+"+"\t"+splitted[7]+"\t"+splitted[8]


