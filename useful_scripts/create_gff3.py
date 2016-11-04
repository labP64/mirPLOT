

from docx import Document
from docx.shared import Inches
import fileinput
import os
import sys
import re
from docx.shared import Pt 
from docx.shared import RGBColor
from docx.shared import Length
import locale
str(sys.argv)


refname=sys.argv[1]
seqsname=sys.argv[2]
outfilnamee=sys.argv[3]
### read matures


with open(seqsname, 'r') as f:
	matures = f.readlines()
f.closed







creat_coordinates_mature=open(outfilnamee, 'w+')

mir=1



with open(refname, 'r') as inF:
	for line in inF:
		if ">" in line:
			precursorname=line


			#prename=line.split("_pre")[0]
			name=line.split(">")[1].rstrip()

		else:

			m1=matures[mir].rstrip()#mature
			maturename=matures[mir-1].split(">")[1].rstrip()
			print  m1
			print line
			prec_1=line.split(m1)[0]### precursor until mature
			mature_i=len(line.split(m1)[0])+1
			mature_e=len(line.split(m1)[0])+len(m1)

		
			if mature_e > 50: # is 3P

				gffmat=name+"\t"+"."+"\t"+"miRNA"+"\t"+str(mature_i)+"\t"+str(mature_e)+"\t"+"."+"\t"+"+"+"\t"+"."+"\t"+"ID="+maturename+"_3p\n"
				creat_coordinates_mature.write(gffmat)
				#print aaa
		
			else: # is 5P

				gffmat=name+"\t"+"."+"\t"+"miRNA"+"\t"+str(mature_i)+"\t"+str(mature_e)+"\t"+"."+"\t"+"+"+"\t"+"."+"\t"+"ID="+maturename+"_5p\n"
				creat_coordinates_mature.write(gffmat)
				#print aaa

			mir=mir+2
