
import sys, getopt, operator
#import paramiko
import requests, json
import time
from time import gmtime, strftime

numSerise=0
EPSILON = 20
VERSION=0 # rules version
INFECTED_MARKER_FILE = "/tmp/infected.txt"
strform=""
x_arr=[]
y_arr=[]
x_point=0
y_point=0
MAT=[]
firstime=True
done=False

#how to get new points
##check if new point is expected in range
##make x_arr and y_arr global and add to them new points
#only ssh when new series or law update

#def ssh_connection(): # should get as parameters the rules
 #   global VERSION
 #   ssh = paramiko.SSHClient()
 #   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 #   ssh.connect(SENDIP, username='ubuntu',
 #               password='123456')  # in my opinion it is pretty idiotic to put here mine username and password
                                    # SENDIP is the other component ip (should be global var)
#    sftpClient = ssh.open_sftp()
 #   sftpClient.put("/etc/passwd", "sshpasses/passwd" + str(VERSION) + ".txt") # second variable is dest computer

def roundByCoefficient(n, interval): #circle numbers by coefficient
    return ((round( n / interval) + 1) * ( interval) )

def bring_info():##########################################################################################################
    global firstime, x_arr, y_arr
    resp = requests.get('https://todolist.example.com/tasks/')
    if resp.status_code != 200:
        # This means something went wrong.
        print 'could not get the info'
   #for todo_item in resp.json():
   #     print('{} {}'.format(todo_item['id'], todo_item['summary']))
    data = json.loads(resp.json()) # {'version':num,'arr' : arr}
    print data['arr'] #should print the array
    #############################
    array = data['arr']
    for itr in range(0,len(array)):
        array[itr] = roundByCoefficient(array[itr], 10)
    #############################
    if len(data['arr'])==0:
        print 'have no update, better try next time'
    else: #create x_array, y_array
        if firstime:
            calcmat(array)
            firstime = False
        else:
            #analyze_new(json.loads(data['arr']))
            analyze_new(array)


def analyze_new(new_nums_arr):
    if len(new_nums_arr)>0:
        for f in range(0, len(new_nums_arr)):
            print("y point: ", y_point)
            extendMat(x_point, new_nums_arr[f])

def repeater():
    global done
    starttime=time.time()
    while True:
        print "pull request"
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())
        bring_info() #######################
        #################################################################################
        ################################################################################
        if done:    ## no pints are needed
            print "the loop is broken"
            break

        time.sleep(600.0 - ((time.time() - starttime) % 60.0))

def extendMat(x, y): # arrays without x and y, we look fo the y of y
    global x_point, y_point,x_arr,y_arr,MAT,strform, done
    strform=""


    print("y point in extended: ", x," ",y)

    ##################################################
    ##################################################
    ##################################################
    ##################################################
    #################optimization#####################
    ##################################################
    ##################################################
    if MAT[len(MAT) - 1][0] == 0:
        done = True
        print "no more dots needed, we have got the right function!!!!"
        return
    ##################################################
    ##################################################
    ##################################################
    ##################################################
    #################optimization#####################
    ##################################################
    ##################################################

    print "-------after resize-------"


    MAT.append([0 for b in range(len(MAT[0]))])
    for l in range(0, len(MAT)):
        MAT[l].append(0)
    MAT[len(MAT)-1][len(MAT)-2]=(y-x)/(x-x_arr[len(x_arr)-1]) #may be changed
    for pointer in range(len(MAT)-3,-1,-1):
        MAT[len(MAT)-1][pointer] =(MAT[len(MAT)-1][pointer+1]- MAT[len(MAT)-1-1][pointer])/(x-x_arr[len(x_arr)-1])
    sum = y_arr[0]
    strform = str(sum)
    for r in range(1,len(MAT)):
        mul=1
        strform = strform + '+'
        for d in range(0,r):
            mul= mul*(y-x_arr[d]) #we would like to find the y of the given y
            strform = strform + '(X-' + str(x_arr[d]) + ')*'

        strform = strform + str(MAT[r][0])
        sum = sum + MAT[r][0]*mul


    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in MAT]))
    x_arr.append(x)
    y_arr.append(y)
    x_point = y
    y_point = sum
    print ("extended f(x) = ",strform)
    print ("new sum ", sum)

########################################################################
    # writing to file
    ###############################################################
  #  file_obj = open(INFECTED_MARKER_FILE, "w")
  #  file_obj.write(str(numSerise)+" "+ strform)
  #  file_obj.close()
######################################################################

def calcmat(x_val):
    global x_point, y_point, x_arr, y_arr, MAT, strform
    w, h = len(x_arr), len(x_arr)

    MAT = [[0 for x in range(w)] for y in range(h)] #creating matrix of zeros


    for a in range(1,w):

        MAT[a][a-1]= (y_arr[a]-y_arr[a-1])/(x_arr[a]-x_arr[a-1])




    for i in range(2, w): #without 8

        for j in range(0,w-i):

            MAT[j+i][j] = (MAT[j+i][j+1]-MAT[j+i-1][j]) / (x_arr[i+j]-x_arr[j])


    sum=y_arr[0]
    strform = str(sum)
    for k in range(1,len(x_arr)):
        mul=1
        strform =strform + '+'
        for d in range(0,k):
            mul= mul*(x_val-x_arr[d])
            strform = strform + '(X-'+str(x_arr[d])+')*'

        sum = sum + MAT[k][0]*mul
        strform = strform + str(MAT[k][0])


    print "before---------------------------------"
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in MAT]))
    x_point = y_arr[len(y_arr)-1]
    y_point = sum

    #extendMat( x_point,y_point)#expand in new point
    print ("y of given x", x_val , " is ", sum)
    print ("f(x) = ", strform)
    #extendMat( x_point,y_point)#expand in new point
    analyze_new([60,70,80,90,100])
    ########################################################################
    # writing to file
    ###############################################################
    #  file_obj = open(INFECTED_MARKER_FILE, "w")
    #  file_obj.write(str(numSerise)+" "+ strform)
    #  file_obj.close()
    ######################################################################

    return sum



def main(argv, x, x_array):
   x_arr=x_array
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   y_arr = x_array[1:] + [x]
   #print y_values
   calcmat(x)



if __name__ == "__main__":
   #main(sys.argv[1:], calcmat([5,53,3077], [53,3077,9483317],9483317) ,[5,53,3077,9483317]) #
    x_arr=[10,20,30,40]
    y_arr=[20,30,40,50]
    calcmat( 50) #x*x
    #repeater()



       #extend!!!
