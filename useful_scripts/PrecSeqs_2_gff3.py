import os
import re
## does a grep from a fasata file to a 1 line fasta genome and the output is gff3 file
import sys
str(sys.argv)
filein=sys.argv[1]
genome=sys.argv[2]


#### Function reverese comp
def ReverseComplement1(seq):
    seq_dict = {'A':'T','T':'A','G':'C','C':'G'}
    return "".join([seq_dict[base] for base in reversed(seq)])




counter=0

with open(filein, 'r') as precseqs:
	for line in precseqs:
		if ">" in line: ## not to check headers
			prec=line.strip().split(">")[1]
		else:## for sequnce
			seq=line.strip()		

			cmd=str("grep -B 1 "+str(seq)+" "+genome+" >  outgrep.txt" )
			#print cmd
			os.system(cmd)


			with open("outgrep.txt", 'r') as grepout:
				for linegrep in grepout:
					if (">" in linegrep): ## not to check headers
						scaff=linegrep.strip()
					elif (linegrep == "--"):
						linegrep=linegrep.strip()	
					else:
						match = re.search(str(seq), str(linegrep))
						if match:
							counter=counter+1
							strand="+"
							scaffold=scaff.split(">")[1].split(" Locust")[0]
							print(str(scaffold+"\t"+"."+ "\t"+"miRNA_primary_transcript"+"\t"+str(int(match.start())+1)+"\t"+str(int(match.end()))+"\t"+"."+"\t"+str(strand)+"\t"+"."+"\t"+"ID="+prec+"--"+str(counter)))


			### for negative strand			
			revseq=ReverseComplement1(seq)
			cmd=str("grep -B 1 "+str(revseq)+" "+genome+" >  outgrep.txt" )
			#print cmd
			os.system(cmd)

			with open("outgrep.txt", 'r') as grepout:
				for linegrep in grepout:
					if (">" in linegrep): ## not to check headers
						scaff=linegrep.strip()
					elif (linegrep == "--"):
						linegrep=linegrep.strip()	
					else:
						revmatch = re.search(str(revseq), str(linegrep))
						if revmatch:
							counter=counter+1
							strand="-"
							scaffold=scaff.split(">")[1].split(" Locust")[0]
							print(str(scaffold+"\t"+"."+ "\t"+"miRNA_primary_transcript"+"\t"+str(int(revmatch.start())+1)+"\t"+str(revmatch.end())+"\t"+"."+"\t"+str(strand)+"\t"+"."+"\t"+"ID="+prec+"--"+str(counter)))



