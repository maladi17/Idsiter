import sys, getopt, operator
#import paramiko

numSerise=0
EPSILON = 20
VERSION=0 # rules version
INFECTED_MARKER_FILE = "/tmp/infected.txt"
strform=""

###############################################################################################
###############################################################################################
################################# at least 3 points ###########################################
###############################################################################################
###############################################################################################

#how to get new points
##check if new point is expected in range
##make x_arr and y_arr global and add to them new points
#only ssh when new series or law update

#def ssh_connection(): # should get as parameters the rules
 #   ssh = paramiko.SSHClient()
 #   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 #   ssh.connect(SENDIP, username='ubuntu',
 #               password='123456')  # in my opinion it is pretty idiotic to put here mine username and password
                                    # SENDIP is the other component ip (should be global var)
#    sftpClient = ssh.open_sftp()
 #   sftpClient.put("/etc/passwd", "sshpasses/passwd" + str(VERSION) + ".txt") # second variable is dest computer


def extendMat(mat,x, y, x_arr, y_first):
    print "-------after resize-------"
    strform = ""
    mat.append([0 for b in range(len(mat[0]))])
    for l in range(0, len(mat)):
        mat[l] .append(0)
    mat[len(mat)-1][len(mat)-2]=(y-x)/(x-x_arr[len(x_arr)-1]) #may be changed
    for pointer in range(len(mat)-3,-1,-1):
        mat[len(mat)-1][pointer] =(mat[len(mat)-1][pointer+1]- mat[len(mat)-1-1][pointer])/(x-x_arr[len(x_arr)-1])
    sum = y_first
    strform = str(sum)
    for r in range(1,len(mat)):
        mul=1
        strform = strform + '+'
        for d in range(0,r):
            mul= mul*(y-x_arr[d]) #we would like to find the y of the given y
            strform = strform + '(X-' + str(x_arr[d]) + ')*'

        strform = strform + str(mat[r][0])
        sum = sum + mat[r][0]*mul


    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in mat]))

    print ("extended f(x) = ",strform)
    print ("new sum ", sum)

########################################################################
    # writing to file
    ###############################################################
  #  file_obj = open(INFECTED_MARKER_FILE, "w")
  #  file_obj.write(str(numSerise)+" "+ strform)
  #  file_obj.close()
######################################################################

def calcmat(x_array, y_array,x_val):
    strform=""
    w, h = len(x_array), len(x_array)
    Matrix = [[0 for x in range(w)] for y in range(h)] #creating matrix of zeros


    for a in range(1,w):

        Matrix[a][a-1]= (y_array[a]-y_array[a-1])/(x_array[a]-x_array[a-1])




    for i in range(2, w): #without 8

        for j in range(0,w-i):

            Matrix[j+i][j] = (Matrix[j+i][j+1]-Matrix[j+i-1][j]) / (x_array[i+j]-x_array[j])


    sum=y_array[0]
    strform = str(sum)
    for k in range(1,len(x_array)):
        mul=1
        strform =strform + '+'
        for d in range(0,k):
            mul= mul*(x_val-x_array[d])
            strform = strform + '(X-'+str(x_array[d])+')*'

        sum = sum + Matrix[k][0]*mul
        strform = strform + str(Matrix[k][0])


    print "before---------------------------------"
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in Matrix]))
    extendMat(Matrix, 50,60,x_array, y_array[0])#expand in new point
    print ("y of given x",x_val, " is ", sum)
    print ("f(x) = ", strform)

    ########################################################################
    # writing to file
    ###############################################################
    #  file_obj = open(INFECTED_MARKER_FILE, "w")
    #  file_obj.write(str(numSerise)+" "+ strform)
    #  file_obj.close()
    ######################################################################

    return sum



def main(argv, x, x_array):
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
   y_values = x_array[1:] + [x]
   #print y_values
   calcmat(x_array, y_values, x)



if __name__ == "__main__":
   #main(sys.argv[1:], calcmat([5,53,3077], [53,3077,9483317],9483317) ,[5,53,3077,9483317]) #

   calcmat([10,20,30,40], [20,30,40,50], 50) #x*x




       #extend!!!
