#!/bin/bash

# 1. perform the preprocessing
# This was performed manually to produce the necessary input for the program
./preprocessing.py part-0000

hdfs dfs -mkdir data0
hdfs dfs -put data0/part-00000 data0/ # copy the data from local directory to hdfs


# 2. loop through 25 consecutive hadoop calls
for ((i=0; i<25; i++))
do
	j=$(expr $i + 1)	
	echo "hadoop call number $j..."
	hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -files mapper.py,reducer.py,names -mapper ./mapper.py -reducer ./reducer.py -input data$i/part-00000 -output data$j 
done

# 3. perform postprocessing on final data
hdfs dfs -get data25/part-0000 ./
./postprocessing.py | sort -g > pageRank.txt
