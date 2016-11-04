##### Do plots from reads mapped to precursors
###### Requires:
####### Precursors in fasta
####### BAM files of reads agaisnt precurosrs

library("GenomicAlignments")

workingDir <- "."
setwd(workingDir)


args <- commandArgs(trailingOnly = TRUE)
print(args)
BAMfilesdir<-paste(workingDir, args[1], sep="/")
fastafile<-paste(workingDir, args[2], sep="/")
outdir<-paste(workingDir, args[3], sep="/")

if (length(args)>3){

	mature_coordinates=read.table(paste(workingDir, args[4], sep="/"))
#	mature_coordinates=read.table("/home/guillem/Documents/mirPLOT/Aphid_paper_mirs/matures_on_prec+11.gff3")
	
}


if (length(args)>4){
  star_coordinates=read.table(paste(workingDir, args[5], sep="/"))
}



BAMfiles<-list.files(path=BAMfilesdir, pattern = ".bam$", full.names = TRUE, recursive = TRUE,  ignore.case = FALSE, include.dirs = FALSE)
BAMfiles
#BAMfiles<-list.files(path="/home/guillem/Documents/mirPLOT/Aphid_paper_mirs", pattern = ".bam$", full.names = TRUE, recursive = TRUE,  ignore.case = FALSE, include.dirs = FALSE)


##############  Graphic parameters
## colors for the bars:
colorstouse=c(rainbow(length(BAMfiles)), "grey")  ## by default grey for are of exression and random color for each library

#############



coverage_p<-list()

for(i in 1:length(BAMfiles)){
  alignment<-readGAlignments(BAMfiles[i])
  coverage_p[i]<-coverage(alignment[strand(alignment) == "+"])
}

#fasta <- readDNAStringSet("/home/guillem/Documents/mirPLOT/Aphid_paper_mirs/Aphid_precs+11_oneline_sorted.fa")
#fasta <- readDNAStringSet("/home/guillem/Documents/mirPLOT/Apis/Apis_precursors_sort.fa")

fasta <- readDNAStringSet(fastafile)
fasta



for(mirna in 1 : length(coverage_p[[i]]) ) {  
      seq<-unlist(strsplit(as.character( fasta[names(coverage_p[[1]][mirna]) ] ), split=""  ))

     selectedRange_coverage<- data.frame(as.numeric(unlist(coverage_p[[1]][mirna])))
     
     if(length(coverage_p)>1){
       for(i in 2:length(coverage_p)){
     	 selectedRange_coverage<-cbind(selectedRange_coverage,as.numeric(unlist(coverage_p[[i]][mirna])))
    	}
     }
  greybars<-rowSums(selectedRange_coverage)    
    
      greybars[greybars>0]<-max(selectedRange_coverage,selectedRange_coverage)
      toplot<-rbind(libs=t(selectedRange_coverage), expression=greybars)

  png(filename = paste(outdir,"/",names(coverage_p[[1]][mirna]), ".png",sep=""),   width = 1200, height = 480)

      plot<-barplot(toplot, axes=FALSE, ylab="Number of Reads", main=names(coverage_p[[1]][mirna]), col=colorstouse, border=colorstouse,beside=T)

	#### if we have mature and star coordinates
	if (  length(args) > 4 ) {
		print( names(coverage_p[[1]][mirna]))

#		  star_i=star_coordinates[mirna,4]+1
#		  star_e=star_coordinates[mirna,5]
#	   	matureseq_i=mature_coordinates[mirna,4]+1
#		  matureseq_e=mature_coordinates[mirna,5]
    
		star_i=star_coordinates[star_coordinates$V1==names(coverage_p[[1]][mirna]),4]
		star_e=star_coordinates[star_coordinates$V1==names(coverage_p[[1]][mirna]),5]
		matureseq_i=mature_coordinates[mature_coordinates$V1==names(coverage_p[[1]][mirna]),4]
		matureseq_e=mature_coordinates[mature_coordinates$V1==names(coverage_p[[1]][mirna]),5]

    print(star_coordinates[star_coordinates$V1==names(coverage_p[[1]][mirna]),])


  		  mtext(at = plot[1,c(1:matureseq_i,matureseq_e:length(seq))], text =seq[c(1:matureseq_i,matureseq_e:length(seq))] ,col="black", side = 1,  line = 0, cex=1)
		  mtext(at = plot[1,star_i:star_e], text = seq[star_i:star_e],col="blue", side = 1,  line = 0, cex=1)
		  mtext(at = plot[1,matureseq_i:matureseq_e], text = seq[matureseq_i:matureseq_e],col="red", side = 1,  line = 0, cex=1)
	}
	#### if we have only mature 
	else if (length(args)> 3 ) {

		print( names(coverage_p[[1]][mirna]))
		matureseq_i=mature_coordinates[mature_coordinates$V1==names(coverage_p[[1]][mirna]),4]
		matureseq_e=mature_coordinates[mature_coordinates$V1==names(coverage_p[[1]][mirna]),5]
		  #matureseq_i=mature_coordinates[mirna,4]
		#matureseq_e=mature_coordinates[mirna,5]
		  mtext(at = plot[1,c(1:matureseq_i,matureseq_e:length(seq))], text =seq[c(1:matureseq_i,matureseq_e:length(seq))] ,col="black", side = 1,  line = 0, cex=1)
		  mtext(at = plot[1,matureseq_i:matureseq_e], text = seq[matureseq_i:matureseq_e],col="red", side = 1,  line = 0, cex=1)

		}
	else{
		mtext(at = plot[1,], text = seq, side = 1,  line = 0, cex=1)
		}






      axis(2, at=seq(0,max(toplot[1:2,]), length.out=4 ) )
  	legend("topright",  legend = c(basename(BAMfiles),"Area of expression"), fill = colorstouse)

	dev.off()

      
}

