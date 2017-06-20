class myStack:
    def __init__(self):
        self.container = []  # You don't want to assign [] to self - when you do that, you're just assigning to a new local variable called `self`.  You want your stack to *have* a list, not *be* a list.

    def isEmpty(self):
        return self.size() == 0  # While there's nothing wrong with self.container == [], there is a builtin function for that purpose, so we may as well use it.  And while we're at it, it's often nice to use your own internal functions, so behavior is more consistent.

    def push(self, item):
        self.container.append(item)  # appending to the *container*, not the instance itself.

    def pop(self):
        return self.container.pop()  # pop from the container, this was fixed from the old version which was wrong

    def size(self):
        return len(self.container)  # length of the container

    def printStack(self):
        print self.container

def main():

    s = myStack()
    s.push('1')
    s.push('2')
    s.printStack()
    print(s.pop())
    s.printStack()
    print(s.pop())
    s.printStack()

if __name__ == "__main__":
    main()
