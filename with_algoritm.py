import matplotlib.pyplot as plt
import time
import pymongo
from sympy import *
from time import gmtime, strftime
import sys
from datetime import datetime, timedelta
from bson.son import SON
import itertools


class time_analyizer_module:

    date = 0
    nextP = 0
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
    rule = 0
    timesArr = []

    def roundByCoefficient(self, n, interval):  # circle numbers by coefficient
        return ((round(n / interval) + 1) * (interval))

    def turnToSec(self, val):
        hours, minutes, seconds = val.split(":")
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

    def fixTime(self, firstH, firstD, currentH, currentD ):
        firstH = self.turnToSec(firstH)
        currentH = self.turnToSec(currentH)

        a = datetime.strptime(firstD, "%d.%m.%y")
        b = datetime.strptime(currentD, "%d.%m.%y")
        if a < b:
            distance = (b-a).days
            currentH = currentH + (distance*24*60*60)
        return currentH - firstH

    def bring_info(self):  ##########################################################################################################

        self.VERSION = self.VERSION + 1
        #try:
        client = pymongo.MongoClient('localhost', 27017)
        db = client.ids
        collection = db.logges
        quesries = []
        start = False
        min = 0

        pipeline = [
            {"$group": {"_id": "$rule", "count": {"$sum": 1}, "arr": {"$push": "$level"}}},
            {"$sort": SON([("count", -1), ("_id", -1)])},
            {"$limit": 1}
        ]

        arr = []
        numRule = ((str(list(collection.aggregate(pipeline))[0]).replace("{", "")).replace("}", "")).split()
        arr.append((numRule[3].replace('[', "")).replace(',', ""))

        for i in range(4, len(numRule) - 3):
            arr.append(numRule[i].replace(',', ""))

        arr.append((numRule[len(numRule) - 3].replace(',', "")).replace("]", ""))
        arr = sorted(arr)

        ar2 = [(g[0], len(list(g[1]))) for g in itertools.groupby(arr)]
        max = 0
        j = 0
        for i in ar2:
            if i[1] > max:
                max = i[1]
                j = i[0]

        j = int(float(j))
        #print j
        numRule = int(float(numRule[-1]))


        for collec in collection.find({"$and": [{"rule": numRule}, {"level": j}]}).sort([("date", pymongo.ASCENDING), ("hour", pymongo.ASCENDING)]) :
            self.timesArr.append(str(collec["hour"]))
            if start == False:
                firstH = collec['hour']
                firstD = collec['date']
                self.rule = collec['rule']
                day, month, year = firstD.split('.')
                hour, minutes, second = firstH.split(':')
                self.date = datetime.strptime('18-05-04 10:12:20', "%y-%m-%d %H:%M:%S")
                self.date = self.date.replace(minute=int(minutes), hour=int(hour), second=int(second), year=int(year), month=int(month), day=int(day))
                print "attack started in " +  str(self.date)
                start = True

            interval = self.fixTime(firstH, firstD, collec['hour'], collec['date'])
            if min > interval:
                min = interval


            quesries.append(interval)

        quesries.sort()
        quesries = list (set (quesries))
        quesries.remove(28817)
        #print max(quesries)
        quesries = [x + (- min) + 1 for x in quesries]

        #except :
         #   print "mongo error, could not connect to the db."
          #  print "Suggestion- have u connected to the db?? \n"


        for itr in range(0, len(quesries)):
            #quesries[itr] = int(self.roundByCoefficient(quesries[itr], 10))
            quesries[itr] = int(quesries[itr])

        #############################


        if len(quesries) == 0:
            print 'have no update, better try next time'
            sys.exit(2)


        return quesries

    def __init__(self):
        array = self.bring_info()
        #array = array[0:100]
        self.__create2Arrays__(array)
        self.VERSION = 1
        self.sum = self.calcmat(self.y_arr[-1])

    def __create2Arrays__(self, arr):
        num = len(arr)-1
        self.x_arr =  arr[0: num]
        self.y_arr = arr[1:]


    def analyze_new(self, new_nums_arr):

        if len(new_nums_arr) > 0: ##if there are updates
            for f in range(0, len(new_nums_arr)):
                print("y point: ", self.y_point)
                self.extendMat(self.x_point, new_nums_arr[f]) #extending

    def repeater(self):


        starttime = time.time()
        while True:
            print "pull request"
            print strftime("%Y-%m-%d %H:%M:%S", gmtime())
            self.bring_info()

            if self.done:  ## no pints are needed
                print "the loop is broken"
                break

            time.sleep(600.0 - ((time.time() - starttime) % 60.0))

    def extendMat(self, x, y):  # arrays without x and y, we look fo the y of y
        # for example: x array: ', [1, 3, 11, 123], ' y_arr: ', [3, 11, 123, 15131], ' x ', 15131, ' y ', 228947163

        self.strform = ""

        #print("y point in extended: ", x, " ", y)

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

        #print "-------after resize-------"

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

        #print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #                 for row in self.MAT]))
        self.x_arr.append(x)
        self.y_arr.append(y)
        self.x_point = y
        self.y_point = sum
        print ("extended f(x) = ", self.simplfomula())
        #print ("new sum ", sum)

        ########################################################################
        # writing to file
        ###############################################################
        #  file_obj = open(INFECTED_MARKER_FILE, "w")
        #  file_obj.write(str(numSerise)+" "+ strform)
        #  file_obj.close()


    def calcmat(self, x_val):
    ###for example  x_val', 15131, ' x_array:  ', [1, 3, 11, 123], ' y_arr: ', [3, 11, 123, 15131]

        w, h = len(self.x_arr), len(self.x_arr)

        self.MAT = [[0 for x in range(w)] for y in range(h)]  # creating matrix of zeros

        for a in range(1, w):
            try:
                self.MAT[a][a - 1] = float(self.y_arr[a] - self.y_arr[a - 1]) / float(self.x_arr[a] - self.x_arr[a - 1])
            except:
                self.MAT[a][a - 1] = self.y_arr[a] - self.y_arr[a - 1] / self.x_arr[a] - self.x_arr[a - 1]


        for i in range(2, w):  # without 8

            for j in range(0, w - i):
                try:
                    self.MAT[j + i][j] = float(self.MAT[j + i][j + 1] - self.MAT[j + i - 1][j]) / float(self.x_arr[i + j] - self.x_arr[j])
                except:
                    self.MAT[j + i][j] = self.MAT[j + i][j + 1] - self.MAT[j + i - 1][j] / self.x_arr[i + j] - self.x_arr[j]

        sum = self.y_arr[0]
        self.strform = str(sum)
        for k in range(1, len(self.x_arr)):
            mul = 1
            self.strform = self.strform + '+'
            for d in range(0, k):
                mul = mul * (x_val - self.x_arr[d])
                self.strform = self.strform + '(X-' + str(self.x_arr[d]) + ')*'
            try:
                sum = sum + self.MAT[k][0] * mul
                self.strform = self.strform + str(self.MAT[k][0])
            except:
                sum = sum + int(self.MAT[k][0]) * mul
                self.strform = self.strform + str(int(self.MAT[k][0]))


        #print "before---------------------------------"
        #print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #                for row in self.MAT]))
        self.x_point = self.y_arr[len(self.y_arr) - 1]
        self.y_point = sum

        # extendMat( x_point,y_point)#expand in new point
        #print ("y of given x", x_val, " is ", sum)
        #print ("f(x) = ", self.simplfomula())
        # extendMat( x_point,y_point)#expand in new point
        #self.analyze_new([228947163, 52416803445000000])
        ########################################################################
        # writing to file
        ###############################################################
        #  file_obj = open(INFECTED_MARKER_FILE, "w")
        #  file_obj.write(str(numSerise)+" "+ strform)
        #  file_obj.close()
        ######################################################################

        return sum

    def simplfomula(self):

        return simplify(self.strform)

    def evaluateForm(self, orderedFormula,xVal):

        f = orderedFormula.replace('X', str(xVal))
        return f


    def writeToFile(self, name):
        f = open(name+".txt", "a")  # opens file with name of "test.txt"
        f.write(" ---------------------------------------------------------------------------------------\n")
        f.write("version from " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) +'\n\n')
        f.write(" ---------------------------------------------------------------------------------------\n")

        f.write(" -----------------------------------parts in the file:----------------------------------------------------\n\n\n\n")
        f.write("\n 1.data acquired\n")
        f.write("\n 2.formula built \n")
        f.write("\n 3.more ordered formula\n")
        f.write("\n 4.future estimated attacks\n")
        f.write("\n\n\n\n -----------------------------------data acquired ----------------------------------------------------\n\n\n\n")
        f.write("intervals (H:M:S): " + str(self.timesArr)+'\n\n')
        f.write("started in: " + str(self.date)+'\n')
        f.write("raised rule "+str(self.rule))
        f.write("\n\n\n\n -----------------------------------got formula:----------------------------------------------------\n\n\n\n")
        f.write(self.strform)
        f.write("\n\n\n -----------------------------------formula in other words----------------------------------------------------\n\n\n\n")
        ordered = str(self.simplfomula())
        f.write(ordered)
        print "calculated a function "
        f.write("\n --------------------------------------\n\n")
        print ordered
        f.write("\n\n\n -----------------------------------future estimated attacks (samples)----------------------------------------------------\n\n\n\n")
        print("\n possible attacks (you are recomended to block according to  the given function)): \n\n ")
        try:

            day = int(int(float(self.sum)) / (60 * 60 * 24))
            if day > 1:
                f.write(str("too far for an attack: "))
            f.write(str( self.date + timedelta(seconds=int(self.sum))))
            f.write(" , \n")
            #print str(self.date + timedelta(seconds=int(self.sum)))


            num = str(self.evaluateForm(self.simplfomula(), self.sum))
            day = int(int(float(num)) / (60 * 60 * 24))
            if day > 1:
                f.write(str("too far for an attack: "))



            f.write( str(self.date + timedelta(seconds=int(float(num)))) + " , \n")
            #print str(self.date + timedelta(seconds=int(float(num))))
            num = str(self.evaluateForm(self.simplfomula(), num))
            day = int(int(float(num)) / (60 * 60 * 24))
            if day > 1:
                f.write(str("too far for an attack: "))


            f.write(str(self.date + timedelta(seconds=int(float(num)))) + '\n')
            #print str(self.date + timedelta(seconds=int(float(num))))

        except:
            f.write("next time is too far then visible. possibly it is not an attack or there wont be any more attack with this function. ")
        f.write('========================================================================================================================\n\n\n')
        f.close()

    def graph(self):
        list = self.y_arr
        plt.plot([self.x_arr[0]]+list, marker='o')
        plt.ylabel('values of intervals')
        plt.title('events acceleration')
        plt.show()

    def repetitions(self, num, name):
        try:
            f = open(name + ".txt", "a")
            f.write("----------------------------you chose " + num + " future suggestions -----------------------------------------\n\n" )
            form = self.simplfomula()
            number = self.sum
            print str(self.date + timedelta(seconds=int(float(self.sum))))
            f.write('0 ' + str(self.date + timedelta(seconds=int(float(self.sum)))) + '\n')
            for i in range(1, int(num)):
                number = self.evaluateForm(self.simplfomula(), number)

                print str(i) + ' ' + str(self.date + timedelta(seconds=int(float(number))))
                f.write(str(i) + ' '+ str(self.date + timedelta(seconds=int(float(number)))) + '\n')
            f.close()
        except:
            print "could not find any close dates"
            f.write("could not complete the action")
            f.close()

def main(argv):

    arguments = argv
    count = len(arguments)
    if (count != 1 and count != 2) or arguments[0] != '-t':
        print " needed   time_analyizer_module.py -t   name of file  (optional) for time inspection"
        sys.exit(2)



#######     we demand that arr creates:
#######         x_arr = [1, 3, 11, 123]
#######         y_arr = [3, 11, 123, 15131]

    if count == 1:
        name = "default"
    else:
        name = arguments[1]

    analyzer = time_analyizer_module()
      # x*x
    # repeater()

    analyzer.writeToFile(name)
    analyzer.graph()
    print "Enter how many future times do u want:",
    numRep = raw_input()
    analyzer.repetitions(numRep, name)

if __name__ == "__main__":

    start_time = time.time()
    main(sys.argv[1:])
   # print("---got answer in %s seconds ---" % (time.time() - start_time))
