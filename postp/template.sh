#!/bin/bash
#PBS -N lens2_postp_num
#PBS -q casper
#PBS -l walltime=12:00:00
#PBS -A P93300641
#PBS -j oe
#PBS -k eod
#PBS -l select=1:ncpus=1

source ~/.bashrc
conda activate lens-py

#python postp_cesm1.py file
#python postp_cesm2.py file
python postp_cesm1_amean1976.py file
#python postp_mpi12.py file




