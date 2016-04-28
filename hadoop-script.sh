#!/bin/bash

# 1. perform the preprocessing
./preprocessing.py

# 2. loop through 25 consecutive hadoop calls
for ((i=0; i<25; i++))
do
	j=$(expr $i + 1)	
	echo "hadoop call number $j..."
done

# 3. perform postprocessing on final data
./postprocessing.py
