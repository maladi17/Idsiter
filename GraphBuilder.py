import collections

class GraphBuilder:
    __data = {}
    __vertexes = 0
    __graph =[]

    def __init__(self,data, vertexes):
        self.__data = collections.OrderedDict(sorted(data.items()))
        self.__vertexes = vertexes
        self.__builder__()


    def __builder__(self):

        self.__graph = [[] for i in range(0,self.__vertexes)]
        keys = self.__data.keys()
        values = self.__data.values()
        for i in range(0, len(self.__data)):

           index =  values[i][0]
           price = keys[i]
           dest = values[i][1]
           tempL = [dest, price]
           self.__graph[index].append((dest,price))


    def printGraph(self):
        print self.__graph

    def printData(self):
        print self.__data

    def getsmallestEdge(self, index):   # I did not put a for here because it should be already ordered by prices
        min = self.__graph[index] ##min price
        if len(min) == 0:
            print "nothing here to find as small"
            return
        else:
            min = self.__graph[index][0][1]
            minEdge = self.__graph[index][0]
     #   for j in range(1,len(self.__graph[index])):
      #      if self.__graph[index][j][1]< min:
       #         min = self.__graph[index][j][1]
        #        minEdge = self.__graph[index][j]

            print(minEdge," ", min)

    def removeEdge(self, StartVertex):
        if len(self.__graph[StartVertex]) == 0:
            print "could not remove anything "
            return
        else:
            del self.__graph[StartVertex][0]

    def HowMuchEdges(self, index):
        ### return how much edges are there from cerain vertex
        return len(self.__graph[index])

    def IsMultiEdge(self, origin, dest):
        ##return num of edges between 2 vertex
        if len(self.__graph[origin]) == 0:
            print "there is no any edges"
            return 0
        else:
            count = 0
            for i in range(0, len(self.__graph[origin])):
                if self.__graph[origin][i][0] == dest:
                    count = count + 1
            print "there are " + str(count) + " edges between "+ str(origin)+" to " +str(dest)
            return count

#######################################################################################
###                                                                                 ###
###         error-does not works when there are packets on the same time            ###
###                                                                                 ###
#######################################################################################


def main():
    data = {10:[0,2], 12:[3,1], 14:[1,3], 15:[2,3],18:[0,2], 20:[2,1]}
    gr = GraphBuilder(data,4)
    gr.printGraph()
    gr.IsMultiEdge(0,2)
    gr.getsmallestEdge(1)
    gr.getsmallestEdge(0)
    gr.removeEdge(1)
    gr.printGraph()
    gr.removeEdge(1)
    gr.printGraph()
    gr.getsmallestEdge(1)
    gr.printGraph()
    gr.removeEdge(0)
    gr.printGraph()
    gr.removeEdge(0)
    gr.printGraph()
    print ("how much edges from 0",gr.HowMuchEdges(0))
    print ("how much edges from 2", gr.HowMuchEdges(2))
    gr.IsMultiEdge(0, 2)
    gr.IsMultiEdge(3, 1)


if __name__ == "__main__":
    main()
