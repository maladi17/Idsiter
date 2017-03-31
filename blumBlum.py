try:

    

    from os import listdir, getcwd, chdir

    from os.path import isfile, join

    from pybloomfilter import BloomFilter                    

except ImportError:

    try:

        print 'System does not have pybloomfilter library. Trying to fix the problem'

        import pip

        pip.main(['install', 'pybloomfiltermmap'])

    except ImportError:

        

        print 'umm...you do not have pip either. you really make thinks hard :('

        exit(1)



print "your current location is: "

print os.getcwd()		

path=input("enter the path to the logs folder: ") # if "" then stay on current directory, else if "../" go back else name directory

if path is "" or " ":

	print "you chose to stay here"

	path=os.getcwd()

else:

	os.chdir(path)

	path=os.getcwd()

	print path



### instead of taking the first file and comparing it with every file as bloom file, the first is bloom always and the rest checked

print firstFileName = os.listdir(path)[0]

print "test file: "+ firstFileName+"   .. openning"





bf = BloomFilter(100000000, 0.00000001, 'filter.bloom')



with open(firstFileName) as f:

    for word in f:

	#we better split each line to ip address, type, payload

        bf.add(word.rstrip())



dict={}

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

#remove first file from list

for log_file in only files:

	with open(log_file) as f:

        	for line in f:

    	    		if /ip+type+payload/ in bf:

				with open(firstFileName) as f: #other file name

			        	for word in f:

						if ip_first is ip_second and type_first is type_second and payload_first is payload_second:

							

							dict[address+""+payload+""+type].append(time_first) # should  we initialize the list?

							break 





	 

#print 'apple' in bf