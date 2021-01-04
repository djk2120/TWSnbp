#!/bin/bash

REFSDIR="/Users/djk2120/projects/references/refs/" 
echo "" > all.tmp
while read p; do
  echo "$p"
  cat $REFSDIR$p >> all.tmp
  echo "" >> all.tmp
done <refs.txt
mv all.tmp all.bib
