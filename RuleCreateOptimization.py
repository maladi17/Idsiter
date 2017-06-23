import sys, getopt, operator
#import paramiko
import requests, json
import time
from sympy import *
from time import gmtime, strftime


class time_analyizer_module:

    numSerise = 0
    EPSILON = 20
    VERSION = 0  # rules version
    INFECTED_MARKER_FILE = "/tmp/infected.txt"
    strform = ""
    x_arr = []
    y_arr = []
    x_point = 0
    y_point = 0
    MAT = []
    firstime = True
    done = False


    def __init__(self, x_array, y_array):
        self.x_arr = x_array
        self.y_arr = y_array

    # how to get new points
    ##check if new point is expected in range
    ##make x_arr and y_arr global and add to them new points
    # only ssh when new series or law update

    # def ssh_connection(self): # should get as parameters the rules
    #   global VERSION
    #   ssh = paramiko.SSHClient()
    #   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #   ssh.connect(SENDIP, username='ubuntu',
    #               password='123456')  # in my opinion it is pretty idiotic to put here mine username and password
    # SENDIP is the other component ip (should be global var)
    #    sftpClient = ssh.open_sftp()
    #   sftpClient.put("/etc/passwd", "sshpasses/passwd" + str(VERSION) + ".txt") # second variable is dest computer

    def roundByCoefficient(self, n, interval):  # circle numbers by coefficient
        return ((round(n / interval) + 1) * (interval))

    def bring_info(self):  ##########################################################################################################

        resp = requests.get('https://todolist.example.com/tasks/')
        if resp.status_code != 200:
            # This means something went wrong.
            print 'could not get the info'
            # for todo_item in resp.json():
            #     print('{} {}'.format(todo_item['id'], todo_item['summary']))
        data = json.loads(resp.json())  # {'version':num,'arr' : arr}
        print data['arr']  # should print the array
        #############################
        array = data['arr']
        for itr in range(0, len(array)):
            array[itr] = self.roundByCoefficient(array[itr], 10)
        #############################
        if len(data['arr']) == 0:
            print 'have no update, better try next time'
        else:  # create x_array, y_array
            if self.firstime:
                self.calcmat(array)
                self.firstime = False
            else:
                # analyze_new(json.loads(data['arr']))
                self.analyze_new(array)

    def analyze_new(self, new_nums_arr):

        if len(new_nums_arr) > 0: ##if there are updates
            for f in range(0, len(new_nums_arr)):
                print("y point: ", self.y_point)
                self.extendMat(self.x_point, new_nums_arr[f]) #extending

    def repeater(self):

        ##
        ## tells to do an action every x time
        ##

        starttime = time.time()
        while True:
            print "pull request"
            print strftime("%Y-%m-%d %H:%M:%S", gmtime())
            self.bring_info()  #######################
            #################################################################################
            ################################################################################
            if self.done:  ## no pints are needed
                print "the loop is broken"
                break

            time.sleep(600.0 - ((time.time() - starttime) % 60.0))

    def extendMat(self, x, y):  # arrays without x and y, we look fo the y of y
        # for example: x array: ', [1, 3, 11, 123], ' y_arr: ', [3, 11, 123, 15131], ' x ', 15131, ' y ', 228947163

        self.strform = ""

        print("y point in extended: ", x, " ", y)

        ##################################################
        ##################################################
        ##################################################
        ##################################################
        #################optimization#####################
        ##################################################
        ##################################################
        # if MAT[len(MAT) - 1][0] == 0:
        #   done = True
        #    print "no more dots needed, we have got the right function!!!!"
        #    return
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        #################optimization#####################
        ##################################################
        ##################################################

        print "-------after resize-------"

        self.MAT.append([0 for b in range(len(self.MAT[0]))])
        for l in range(0, len(self.MAT)):
            self.MAT[l].append(0)
        self.MAT[len(self.MAT) - 1][len(self.MAT) - 2] = (y - x) / (x - self.x_arr[len(self.x_arr) - 1])  # may be changed
        for pointer in range(len(self.MAT) - 3, -1, -1):
            self.MAT[len(self.MAT) - 1][pointer] = (self.MAT[len(self.MAT) - 1][pointer + 1] - self.MAT[len(self.MAT) - 1 - 1][pointer]) / (
            x - self.x_arr[len(self.x_arr) - 1])
        sum = self.y_arr[0]
        self.strform = str(sum)
        for r in range(1, len(self.MAT)):
            mul = 1
            self.strform = self.strform + '+'
            for d in range(0, r):
                mul = mul * (y - self.x_arr[d])  # we would like to find the y of the given y
                self.strform = self.strform + '(X-' + str(self.x_arr[d]) + ')*'

            self.strform = self.strform + str(self.MAT[r][0])
            sum = sum + self.MAT[r][0] * mul

        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in self.MAT]))
        self.x_arr.append(x)
        self.y_arr.append(y)
        self.x_point = y
        self.y_point = sum
        print ("extended f(x) = ", self.simplfomula())
        print ("new sum ", sum)

        ########################################################################
        # writing to file
        ###############################################################
        #  file_obj = open(INFECTED_MARKER_FILE, "w")
        #  file_obj.write(str(numSerise)+" "+ strform)
        #  file_obj.close()

    ######################################################################

    def calcmat(self, x_val):
    ###for example  x_val', 15131, ' x_array:  ', [1, 3, 11, 123], ' y_arr: ', [3, 11, 123, 15131]
        w, h = len(self.x_arr), len(self.x_arr)

        self.MAT = [[0 for x in range(w)] for y in range(h)]  # creating matrix of zeros

        for a in range(1, w):
            self.MAT[a][a - 1] = (self.y_arr[a] - self.y_arr[a - 1]) / (self.x_arr[a] - self.x_arr[a - 1])

        for i in range(2, w):  # without 8

            for j in range(0, w - i):
                self.MAT[j + i][j] = (self.MAT[j + i][j + 1] - self.MAT[j + i - 1][j]) / (self.x_arr[i + j] - self.x_arr[j])

        sum = self.y_arr[0]
        self.strform = str(sum)
        for k in range(1, len(self.x_arr)):
            mul = 1
            self.strform = self.strform + '+'
            for d in range(0, k):
                mul = mul * (x_val - self.x_arr[d])
                self.strform = self.strform + '(X-' + str(self.x_arr[d]) + ')*'

            sum = sum + self.MAT[k][0] * mul
            self.strform = self.strform + str(self.MAT[k][0])

        print "before---------------------------------"
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in self.MAT]))
        self.x_point = self.y_arr[len(self.y_arr) - 1]
        self.y_point = sum

        # extendMat( x_point,y_point)#expand in new point
        print ("y of given x", x_val, " is ", sum)
        print ("f(x) = ", self.simplfomula())
        # extendMat( x_point,y_point)#expand in new point
        self.analyze_new([228947163, 52416803445000000])
        ########################################################################
        # writing to file
        ###############################################################
        #  file_obj = open(INFECTED_MARKER_FILE, "w")
        #  file_obj.write(str(numSerise)+" "+ strform)
        #  file_obj.close()
        ######################################################################

        return sum

    def simplfomula(self):
        print self.strform
        return simplify(self.strform)

def main():


    x_arr = [1, 3, 11, 123]
    y_arr = [3, 11, 123, 15131]
    analyzer = time_analyizer_module(x_arr, y_arr)
    analyzer.calcmat(15131)  # x*x
    # repeater()
    print analyzer.simplfomula()

if __name__ == "__main__":
    main()
