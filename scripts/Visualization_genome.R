##### Do plots from reads mapped to precursors
###### Requires:
####### Precursors in fasta
####### BAM files of reads agaisnt precurosrs

# reads against miRNAs
library("GenomicAlignments")
#library("rtracklayer")
#library(Rsamtools)
workingDir <- "."
setwd(workingDir)

args <- commandArgs(trailingOnly = TRUE)
print(args)

BAMfilesdir<-paste(workingDir, args[1], sep="/")
fastafile<-paste(workingDir, args[2], sep="/")
outdir<-paste(workingDir, args[3], sep="/")




if (length(args)>3){

	mature_coordinates=read.table(paste(workingDir, args[4], sep="/"))
}


if (length(args)>4){
  star_coordinates=read.table(paste(workingDir, args[5], sep="/"))
}

if (length(args)>5){
  gff=read.table(paste(workingDir, args[6], sep="/"))
}

if (length(args)>6){
  extrabases=as.numeric(args[7])
}



BAMfiles<-list.files(path=BAMfilesdir, pattern = ".bam$", full.names = TRUE, recursive = TRUE,  ignore.case = FALSE, include.dirs = FALSE)
BAMfiles

##############  Graphic parameters
## colors for the bars:
colorstouse=c(rainbow(length(BAMfiles)), "grey")  ## by default grey for are of exression and random color for each library

#############

coverage_p<-list()
coverage_n<-list()

for(i in 1:length(BAMfiles)){
  alignment<-readGAlignments(BAMfiles[i])
  coverage_p[i]<-coverage(alignment[strand(alignment) == "+"])
  coverage_n[i]<-coverage(alignment[strand(alignment) == "-"])
  
}


#genome <- readDNAStringSet("/home/guillem/Documents/Blattella_genome/ftp.hgsc.bcm.edu/I5K-pilot/German_cockroach/genome_assemblies/Bgermanica.scaffolds.fa")
genome <- readDNAStringSet(fastafile)




for(i in 1:dim(gff)[1] ){  
  ##convert in GRanges
  selected_mir<-gff[i,]
  mirname=unlist(strsplit(as.character(gff[i,9]), "ID="))[2]
  selectedRange <- GRanges( selected_mir$V1 ,IRanges(selected_mir$V4-extrabases,selected_mir$V5+extrabases),strand=selected_mir$V7)
  scaffold<-as.character(selected_mir$V1)
  
  if (selected_mir$V7 == "+"){
    
    selectedRange_coverage<- as.numeric(unlist(coverage_p[[1]][scaffold][range(selectedRange)]))
    
    for(j in 2:length(coverage_p)){
      selectedRange_coverage<-cbind(selectedRange_coverage,as.numeric(unlist(coverage_p[[j]][scaffold][range(selectedRange)])))
    }
    
    seqview <- Views(subject=unlist(genome[scaffold]),start=selected_mir$V4-extrabases, end=selected_mir$V5+extrabases)
    
    greybars<-rowSums(selectedRange_coverage)    
    greybars[greybars>0]<-max(selectedRange_coverage,selectedRange_coverage)
    toplot<-rbind(libs=t(selectedRange_coverage), expression=greybars)
    
    
    png(filename = paste(outdir,"/",mirname, ".png",sep=""),   width = 1200, height = 480)
    
    plot<-barplot(toplot, axes=FALSE, ylab="Number of Reads", main=mirname, col=colorstouse, border=colorstouse,beside=T)
    
    
    seq<-toString(seqview)
    seq<-unlist(strsplit(seq, split=""))
    print( gff[i,9])
    
    plot<-barplot(toplot, axes=FALSE, ylab="Number of Reads", main=mirname, col=colorstouse, border=colorstouse,beside=T)
    if (  length(args) > 5 ) {
      print(seq)
      star_i=star_coordinates[i,4]-gff[i,4]+extrabases+1
      star_e=star_coordinates[i,5]-gff[i,4]+extrabases+1
      matureseq_i=mature_coordinates[i,4]-gff[i,4]+extrabases+1
      matureseq_e=mature_coordinates[i,5]-gff[i,4]+extrabases+1
      mtext(at = plot[1,c(1:matureseq_i,matureseq_e:length(seq))], text =seq[c(1:matureseq_i,matureseq_e:length(seq))] ,col="black", side = 1,  line = 0, cex=1)
      mtext(at = plot[1,star_i:star_e], text = seq[star_i:star_e],col="blue", side = 1,  line = 0, cex=1)
      mtext(at = plot[1,matureseq_i:matureseq_e], text = seq[matureseq_i:matureseq_e],col="red", side = 1,  line = 0, cex=1)
      dev.off()
    }
  }
  
  ### If reverse we get revese-comp seq, and we also reverse bars order
  if (selected_mir$V7 == "-"){
    
    selectedRange_coverage<- as.numeric(unlist(coverage_n[[1]][scaffold][range(selectedRange)]))
    
    for(j in 2:length(coverage_n)){
      selectedRange_coverage<-cbind(selectedRange_coverage,as.numeric(unlist(coverage_n[[j]][scaffold][range(selectedRange)])))
    }
    
    seqview <- Views(subject=unlist(genome[scaffold]),start=selected_mir$V4-extrabases, end=selected_mir$V5+extrabases)
    
    greybars<-rowSums(selectedRange_coverage)    
    greybars[greybars>0]<-max(selectedRange_coverage,selectedRange_coverage)
    toplot<-rbind(libs=t(selectedRange_coverage), expression=greybars)
    
    
    png(filename = paste(outdir,"/",mirname, ".png",sep=""),   width = 1200, height = 480)
    
    plot<-barplot(toplot, axes=FALSE, ylab="Number of Reads", main=gff[i,9], col=colorstouse, border=colorstouse,beside=T)
    
    
    seq<-toString(seqview)
    seq<-unlist(strsplit(seq, split=""))
    seq_reverse<-reverseComplement(seqview)
    seq_reverse<-toString(seq_reverse)
    seq_reverse<-unlist(strsplit(seq_reverse, split=""))
    seq<-seq_reverse
    
    revdata <-selectedRange_coverage[dim(selectedRange_coverage)[1]:1,]
    selectedRange_coverage<-revdata
    
    print( gff[i,9])
    
    plot<-barplot(toplot, axes=FALSE, ylab="Number of Reads", main=gff[i,9], col=colorstouse, border=colorstouse,beside=T)
    
    if (  length(args) > 5 ) {
    
      
       
       print(seq)
      star_i=abs(star_coordinates[i,4]-gff[i,5])+extrabases+1
      star_e=abs(star_coordinates[i,5]-gff[i,5])+extrabases+1
      matureseq_i=abs(mature_coordinates[i,4]-gff[i,5])+extrabases+1
      matureseq_e=abs(mature_coordinates[i,5]-gff[i,5])+extrabases+1
     print(star_i)
     print(star_e)
     
      mtext(at = plot[1,c(1:matureseq_i,matureseq_e:length(seq))], text =seq[c(1:matureseq_i,matureseq_e:length(seq))] ,col="black", side = 1,  line = 0, cex=1)
      mtext(at = plot[1,star_i:star_e], text = seq[star_i:star_e],col="blue", side = 1,  line = 0, cex=1)
      mtext(at = plot[1,matureseq_i:matureseq_e], text = seq[matureseq_i:matureseq_e],col="red", side = 1,  line = 0, cex=1)
      dev.off()
 
    }
    
  }
  ### if ature and star coordinates
  
}


