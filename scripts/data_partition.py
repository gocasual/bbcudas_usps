'''
this script reads the original csv data set and partitions the data frame. 
writes data chunks to individual files for easier computing. 
'''
import os
import pandas as pd


chunk_size = 100000
input_file_path = os.path.join('raw-data', 'gmu_dom_firstscan_20240501.csv')
output_file_path = os.path.join('data','usps_set')
total_rows = sum(1 for line in open(input_file_path))

print(total_rows)
