#! /bin/bash
#
#PBS -l walltime=00:02:00:00
#PBS -l nodes=1:ppn=32
#PBS -W group_list=cascades
#PBS -q open_q

cd $PBS_O_WORKDIR

module purge
module load gcc/5.2.0
module load Anaconda/4.2.0
#
python -m 
