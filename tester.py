import time_analyizer_module as tm

def main():

    arr = [1, 3, 11, 123, 15131]

    ####    we demand that arr creates:
    ####        x_arr = [1, 3, 11, 123]
    ####        y_arr = [3, 11, 123, 15131]

    analyzer = tm.time_analyizer_module(arr)
    analyzer.calcmat(15131)  # x*x
    # repeater()
    print analyzer.simplfomula()

if __name__ == "__main__":
    main()
