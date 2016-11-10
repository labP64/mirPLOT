# mirPLOT


Here you can download the scripts used for generating the miRNA reports for "The microRNA toolkit of insects". mirPLOT calls different scripts from "/scripts" in order to produce different plots depending on input data. However the scripts from that directory can also be used independently. The results are in "docx" format, however it is recomended to open them with "LibreOffice Write" for better visualization.



The "useful_scripts" directory, contains some scripts that might be useful for pre-processing miRNA data.
 
 
 

The data for running the examples is available at;
https://drive.google.com/open?id=0B1HX-0ECt0DgQkh5VEg4REE1dDA


For mirPLOT help;
    $ python mirPLOT_current.py --help

			You have differnt modes to run mirPLOT.py

			 1- With Bam files of shortRNA reads mapped against miRNA precursors+some flanking nucleotides:

			   1.1 - Providing precursors fasta file and bam files directory

				 $ python mirPLOT_current.py --BamFilesDir Example_Files/ --PrecsFasta Example_Files/conserved+30.fa --output Figures_2  --Flanking_bases 11

			   1.2 - Providing precursors fasta file, bam files directory and gff3 file with mature miRNA annotations

				 $ python mirPLOT_current.py --BamFilesDir Example_Files/ --PrecsFasta Example_Files/conserved+30.fa --output Figures_2  --gff3Matures Example_Files/Coordinates_matures_30.gff3 --Flanking_bases 11

			   1.3 - Providing precursors fasta file, bam files directory and gff3 file with mature and star miRNA annotations
				 
				 $ python mirPLOT_current_dev.py --BamFilesDir Example_Files/ --PrecsFasta Example_Files/conserved+30.fa --output Example_Files/  --gff3Matures Example_Files/Coordinates_matures_30.gff3  --gff3Stars Example_Files/Coordinates_stars_30.gff3 --Flanking_bases 11


			 2- With Bam files of shortRNA reads mapped against genome and  gff3 files
				 $ python mirPLOT_current.py --BamFilesDir  --Genome --output Figures_2  --gff3Matures  --gff3Stars --gff3Precs --Flanking_bases 11

			--BamFilesDir
			--PrecsFasta
			--output / -o
			--help / -h
			--gff3Matures
			--gff3Stars
			--OnlyPngPlot
			--Flanking_bases	Number of flanking bases






For any questions write me at guillem.ylla [-a-t-] ibe.upf-csic.com
Please refer to (Ylla et al. 2016)

