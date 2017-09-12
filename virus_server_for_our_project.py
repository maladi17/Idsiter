import socket  # Import socket module


def Main():
    host = ''
    port = 5001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    s.listen(1)
    print "listening"
    c, addr = s.accept()
    message = 'n'
    print "connection from: " + str(addr)
    ##data = c.recv(1024)  # get the list of files as string
    ##print data

    ##while True:

        ##message = raw_input("->")  # get as input wanted  file
        ##c.send(message)  # send name of wanted file
        ##data = c.recv(1024)  # get answer whether it is valid name
        ##if data == "done":
         ##   print "done"
         ##   break
        ##else:
        ##    print "try again"
    size = int(c.recv(1024))

    f = open('new_' + str(message), 'wb')
    data = c.recv(1024)
    totalRec = int(len(data))
    f.write(data)
    while totalRec < size:
        data = c.recv(1024)
        print str(totalRec) + " " + str(size)
        totalRec += len(data)
        f.write(data)

    print "download Complete"

    c.close()


if __name__ == '__main__':
    Main()
