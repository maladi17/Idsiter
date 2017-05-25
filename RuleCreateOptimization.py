import sys, getopt, operator
#import paramiko
import requests, json
import time
from time import gmtime, strftime
from py_expression_eval import Parser

numSerise=0
EPSILON = 20
VERSION=0 # rules version
INFECTED_MARKER_FILE = "/tmp/infected.txt"
STRFORM = ""
x_arr=[]
y_arr=[]
x_point=0
y_point=0
firstime=True
done=False
list1=[]
list2=[]
list3=[]

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


def formulaCalc(x_val):
    global STRFORM, x_point, y_point, x_arr, y_arr
    parser = Parser()
    ans = parser.evaluate(STRFORM, {'X': x_val})
    x_point = x_val

    y_point = ans
   
    return ans

def bring_info():##########################################################################################################
    global firstime
    resp = requests.get('https://todolist.example.com/tasks/')
    if resp.status_code != 200:
        # This means something went wrong.
        print 'could not get the info'
   #for todo_item in resp.json():
   #     print('{} {}'.format(todo_item['id'], todo_item['summary']))
    data = json.loads(resp.json()) # {'version':num,'arr' : arr}
    print data['arr'] #should print the array
    if len(data['arr'])==0:
        print 'have no update, better try next time'
    else:
        if firstime:
            otherCalc(data['arr'])
            firstime = False
        else:
            analyze_new(json.loads(data['arr']))


def analyze_new(new_nums_arr):
    global x_point
    if len(new_nums_arr)>0:
        for f in range(0, len(new_nums_arr)):
            extendArr(x_point, new_nums_arr[f])


def extendArr(x_p, y_p):
    global list1,list2,list3, done, x_point, y_point,x_arr,y_arr
    if list1[len(list1)-1]=='A':
        if list2[0] == 0:
            done = True
            print "no more dots needed, we have got the right function!!!!"
            return
        else:
            list2.append('A')

            list1.append(y_p)

            for j in range(len(list1)-1, 0, -1):
                list1[j-1] = ((list1[j ] - list2[j-1]) / (x_p - x_arr[j-1]))

            list3.append(list1[0])

    else: #A in list2
        if list1[0] == 0:
            done = True
            print "no more dots needed, we have got the right function!!!!"
            return
        else:
            list1.append('A')

            list2.append(y_p)

            for j in range(len(list2) - 1, 0, -1):
                list2[j-1] = ((list2[j] - list1[j-1]) / (x_p - x_arr[j-1]))

            list3.append(list2[0])
    x_point = y_p
    y_point = formulaCalc(y_p)
    x_arr.append(x_p)
    y_arr.append(y_p)

########################################################################
    # writing to file
    ###############################################################
  #  file_obj = open(INFECTED_MARKER_FILE, "w")
  #  file_obj.write(str(numSerise)+" "+ strform)
  #  file_obj.close()
######################################################################



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




def otherCalc(y_last_point_known):
    global x_point, y_point, x_arr, y_arr, MAT, STRFORM
    global list1,list2,list3   #keeps mekadmim
    list1.append(y_arr[0])
    list1.append('A')
    list3.append(y_arr[0])
    list2.append(y_arr[1])
    list2.insert(0,(y_arr[1]-y_arr[0])/(x_arr[1]-x_arr[0]))
    list3.append(list2[0])

    for a in range(2, len(x_arr)):
        if a%2==0:
            list2.append('A')
            list1.append(y_arr[a])
            for j in range(len(list1)-2, -1, -1):
                list1[j]=((list1[j+1] - list2[j]) / (x_arr[j+1] - x_arr[j]))

            list3.append(list1[0])

        else:

            list1.append('A')
            list2.append(y_arr[a])
            for j in range(len(list2)-2, -1, -1):
                list2[j]=((list2[j+1] - list1[j]) / (x_arr[j+1] - x_arr[j]))

            list3.append(list2[0])


    STRFORM = str(list3[0])

    for i in range(1, len(list3)):
        STRFORM = STRFORM + "+" + str(list3[i])
        for k in range(0, i): # we dont wat the first one to do this
            STRFORM = STRFORM +"*(X-" + str(x_arr[k])+")"
    formulaCalc(y_last_point_known)
    analyze_new([150,310,630,1270])

    ########################################################################
    # writing to file
    ###############################################################
    #  file_obj = open(INFECTED_MARKER_FILE, "w")
    #  file_obj.write(str(numSerise)+" "+ STRFORM)
    #  file_obj.close()
    ######################################################################





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
   otherCalc()



if __name__ == "__main__":
   #main(sys.argv[1:], calcmat([5,53,3077], [53,3077,9483317],9483317) ,[5,53,3077,9483317]) #

    x_arr=[10,30]
    y_arr=[30,70]
    otherCalc(70)
    print formulaCalc(1270)
    print STRFORM
    #calcmat( 50) #x*x
    #repeater()
    #formulaCalc()


       #extend!!!
