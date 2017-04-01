Our algorithem is as the following:

Our algorithem has two modes:
A. Accurate and heavier
B. Less acurrate and less heavier. 

We get as an input text files of logs of the hids-s into some certain folder.  Those logs carry the number of queries in it as file names. Those files arrive after some parsing  and optimization.

We take the first file and put the source ip+size+type into a data structure called bloom filter.  For every other file , for every packet, we check if it is contained in the bloom filter. we Put those packets inside a hash map and later search for it in the first file by aho corasick algorithem.
We will save those packets time inside a dictionary and later use machine learning in order to make new rules. 


We configured a Virtual  system in order to test our algorithem.  It wont work outside Our system because it demands the existence of hids,  parser and more. 

A youtube link as poc will be updated soon!
