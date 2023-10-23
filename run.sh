#!/bin/bash

#SBATCH --export=ALL # export all environment variables to the batch job.
#SBATCH -p mrcq # submit to the MRC queue
#SBATCH --time=90:00:00 # Maximum wall time for the job.
#SBATCH -A Research_Project-MRC190311 # research project to submit under.
#SBATCH --nodes=1 # specify number of nodes.
#SBATCH --ntasks-per-node=16 # specify number of processors per node
#SBATCH --mail-type=END # send email at job completion
#SBATCH --mail-user=s.w.wang@exeter.ac.uk # email me at job completion
#SBATCH --error=/gpfs/mrc0/projects/Research_Project-MRC190311/DNAm/Fetal/hackathon_team2/Pancreas/run.err # error file
#SBATCH --output=/gpfs/mrc0/projects/Research_Project-MRC190311/DNAm/Fetal/hackathon_team2/Pancreas/run.log # output file
#SBATCH --mem=20G
#SBATCH --job-name=database

# specify the working dir and input files 
work_path='/gpfs/mrc0/projects/Research_Project-MRC190311/DNAm/Fetal/hackathon_team2'
db_path='Pancreas'
pheno_file='fetalPancreas_pheno.csv'
epic_file='epicManifest.csv'
betas='fetalPancreas_betas.csv'

# Preparing the data based on R
cd ${db_path}
mkdir -p ${db_path}
module load R/4.2.1-foss-2022a
Rscript Parse_db_data.R  \
        ${work_path} \
        ${db_path} \
        ${pheno_file} \
        ${epic_file} \
        ${betas}

# Building the database based on Python
python Hackathod_Siyi.py

# Fetch gene list and probe list
python Fetch_Siyi.py