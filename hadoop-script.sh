#!/bin/bash

# 1. perform the preprocessing
#./preprocessing.py

# 2. loop through 25 consecutive hadoop calls
for ((i=0; i<25; i++))
do
	j=$(expr $i + 1)	
	echo "hadoop call number $j..."
	hadoop jar /usr/local/cellar/hadoop/2.7.2/libexec/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -files mapper.py,reducer.py,names -mapper ./mapper.py -reducer ./reducer.py -input data$i/part-00000 -output data$j
done

# 3. perform postprocessing on final data
#./postprocessing.py
