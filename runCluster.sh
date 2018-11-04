#!/bin/env bash

hadoop fs -rm -r -f -skipTrash *.json
hadoop fs -rm -r -f -skipTrash wordCount
hadoop fs -rm -r -f -skipTrash namedEntity
export JAVA_HOME=/usr/java/jdk1.8.0_171/
hadoop fs -put ../3_Hurricane_Matthew_big_CleanedData/*.json
spark2-submit --archives external_pkgs.zip#pyspark clustercode.py
rm -rf wordCount
rm -rf namedEntity
hadoop fs -get wordCount
hadoop fs -get namedEntity 
