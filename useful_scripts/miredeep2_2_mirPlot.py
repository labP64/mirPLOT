from Bio import SeqIO
import getopt
import sys
import glob
import os
import fileinput
import re
import locale
from docx import Document
from docx.shared import Inches
from docx.shared import Pt 
from docx.shared import RGBColor
from docx.shared import Length
from Bio import SeqIO


version = '1.0'


 
options, remainder = getopt.getopt(sys.argv[1:], 'o:vh', [						         'output=', 
														 'help',
														 'FastqFile=',
														 'Genome=',
														 'Mirdeep_2_result_csv=',
														 'Flanking_bases=',

														 ])



#print 'BamFilesDir :', BamFilesDir


for opt, arg in options:
	if opt in ('-h', '--help'):
		print """ 
		That's the help page (-h / --help)
				python miredeep2_2_mirPlot.py --Flanking_bases --FastqFile  --Genome  --Mirdeep_2_result_csv --output  

$ python miredeep2_2_mirPlot.py --FastqFile  /home/guillem/Downloads/mirdeep2_0_0_7/develoment/22_libs.fastq --Mirdeep_2_result_csv /home/guillem/Documents/mirPLOT/development/result_07_03_2016_t_10_19_30.csv --Flanking_bases 11  --Genome /home/guillem/Documents/Blattella_genome/ftp.hgsc.bcm.edu/I5K-pilot/German_cockroach/genome_assemblies/Bgermanica.scaffolds.fa --output /home/guillem/Documents/mirPLOT/development/


		\n"""
		sys.exit()




	elif opt in ('-o', '--output'):
		output_dir = arg
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)


	elif opt == '--Genome':
		Genome = arg
		if (os.path.isfile(Genome) ==False):
			print "Error ",Genome, "Not found"
			break
		else:
			print "Genome file=", Genome


	elif opt == '--FastqFile':
		FastqFile = arg
		if (os.path.isfile(FastqFile) ==False):
			print "Error ",FastqFile, "Not found"
			break
		else:
			print "FastqFile file=", FastqFile

	
	elif opt == '--Mirdeep_2_result_csv':
		mirdeepcsv = arg
		if (os.path.isfile(mirdeepcsv) ==False):
			print "Error ",mirdeepcsv, "Not found"
			break

	elif opt == '--Flanking_bases':
		flanking_bases=int(arg)

	else:
		print "Args missing"



flag=False
namesdict=dict()

with open(mirdeepcsv, 'r') as inF:
	for line in inF:
		if flag==False:
			if "provisional id" in line :
				flag=True
				#print line
				out_mature= open(output_dir+"matures_mirdeep2.fa", 'w+')
				out_star= open(output_dir+"stars_mirdeep2.fa", 'w+')
				out_prec_gff3= open(output_dir+"precs_mirdeep2+"+str(flanking_bases)+".gff3", 'w+')
			else:
				flag=False	

		else: ## flag= True
			if "Scaffold" in line : ## ALL

				line_splitted=line.split("\t")

				if ("Mir" in line_splitted[9]):### if are descrived
			
					mirname=line_splitted[9].split("_")[0]
					i=1
					while (mirname in namesdict):
						mirname=mirname+"_"+str(i)
						i=i+1
						print mirname
					namesdict[mirname]=1

				else:## if novels
					mirname=line_splitted[0]


				out_mature.write( ">"+mirname+"\n"+line_splitted[13].replace("u", "t").upper()+"\n")
				out_star.write( ">"+mirname+"\n"+line_splitted[14].replace("u", "t").upper()+"\n")
				coordinates=line_splitted[16]

				ini=int(coordinates.split(":")[1].split("..")[0])
				end=int(coordinates.split("..")[1].split(":")[0])

				ini2=ini-flanking_bases+1
				end2=end+flanking_bases
				strand=coordinates.split(":")[2].rstrip('\n')



				out_prec_gff3.write( coordinates.split(":")[0]+"\t"+"mirdeep2"+"\t"+"mirna"+"\t"+str(ini2)+"\t"+str(end2)+"\t"+"."+"\t"+strand+"\t"+"."+"\tID="+mirname+"_prec+"+str(flanking_bases)+"\n")
				

			else:#if empty line
				next=1
				

out_prec_gff3.close()
out_star.close()
out_mature.close()



cmd=str("gffread  -g "+Genome+"  "+output_dir+"precs_mirdeep2+"+str(flanking_bases)+".gff3"+" -w "+ output_dir+"provisional.fa" )
print "\n"+cmd+"\n"
os.system(cmd )

cmd=str("perl useful_scripts/fasta2one.pl  "+output_dir+"provisional.fa  > "+ output_dir+"precs_mirdeep2+"+str(flanking_bases)+"one_line.fa" )
print "\n"+cmd+"\n"
os.system(cmd )

cmd=str("rm -rf "+ output_dir+"provisional.fa" )
print "\n"+cmd+"\n"
os.system(cmd )







###### sort fasta function

def sortfasta( infile ):
	handle = open(infile, "rU")
	records = list(SeqIO.parse(handle, "fasta"))
	handle.close()

	if ("_prec" in records[0].id ):
		sortedList = [f for f in sorted(records, key=lambda x : x.id.split("prec")[0])]
	else:
		sortedList = [f for f in sorted(records, key=lambda x : x.id+"_")]
	out_sort= open(infile+"_sorted", 'w+')
	for s in sortedList:
	   out_sort.write(">"+s.description+"\n")
	   out_sort.write(str(s.seq)+"\n")
	out_sort.close()


##############################

sortfasta(str(output_dir+"precs_mirdeep2+"+str(flanking_bases)+"one_line.fa"))
sortfasta(str(output_dir+"matures_mirdeep2.fa"))
sortfasta(str(output_dir+"stars_mirdeep2.fa"))



########################
## create coordibnates function
def createcoordinates( maturefile, precsfile ):

	with open(maturefile, 'r') as f:
		matures = f.readlines()
	f.closed

	coordinatesfile=open(maturefile.split(".fa")[0]+"_onprec+"+str(flanking_bases)+".gff3", 'w+')

	mir=1

	with open(precsfile, 'r') as inF:
		for line in inF:
			if ">" in line:
				precursorname=line
				name=line.split(">")[1].rstrip()

			else:

				m1=matures[mir].rstrip()#mature
				
		
				maturename=matures[mir-1].split(">")[1].rstrip()


				prec_1=line.split(m1)[0]### precursor until mature
				mature_i=len(line.split(m1)[0])+1
				mature_e=len(line.split(m1)[0])+len(m1)
			
				if("_3p" in maturename): 
					maturename=maturename.replace("_3p", "")

				elif("_5p" in maturename):
					maturename=maturename.replace("_5p", "")
					print "No replace 1", maturename

				
		
				if mature_e > 40: # is 3P

					gffmat=name+"\t"+"."+"\t"+"miRNA"+"\t"+str(mature_i)+"\t"+str(mature_e)+"\t"+"."+"\t"+"+"+"\t"+"."+"\t"+"ID="+maturename+"_3p\n"
					coordinatesfile.write(gffmat)

		
				else: # is 5P

					gffmat=name+"\t"+"."+"\t"+"miRNA"+"\t"+str(mature_i)+"\t"+str(mature_e)+"\t"+"."+"\t"+"+"+"\t"+"."+"\t"+"ID="+maturename+"_5p\n"
					coordinatesfile.write(gffmat)


				mir=mir+2
	coordinatesfile.close()
##############################

createcoordinates( str(output_dir+"matures_mirdeep2.fa_sorted"), str(output_dir+"precs_mirdeep2+"+str(flanking_bases)+"one_line.fa_sorted") )#mature
createcoordinates( str(output_dir+"stars_mirdeep2.fa_sorted"), str(output_dir+"precs_mirdeep2+"+str(flanking_bases)+"one_line.fa_sorted"))#star





cmd=str("bowtie-build -f "+ output_dir+"precs_mirdeep2+"+str(flanking_bases)+"one_line.fa_sorted " + output_dir+"bowtiefiles") 
print "\n"+cmd+"\n"
#os.system(cmd )



cmd=str(" bowtie -a -l 18 -n 0 -p 6 " + output_dir+"bowtiefiles"+" -q "+FastqFile +" --sam "+  output_dir+"Out.sam")
print "\n"+cmd+"\n"
os.system(cmd )


cmd=str("samtools view -bSF4  "+ output_dir+"Out.sam | samtools sort - "+output_dir+"out" )
print cmd+"\n"
os.system(cmd )

cmd=str("samtools index "+ output_dir+"out.bam" )
print cmd+"\n"
os.system(cmd )
	 
cmd=str("rm -rf "+output_dir+"Out.sam" )
print cmd+"\n"
os.system(cmd )






