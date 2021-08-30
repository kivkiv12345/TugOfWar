import os
from time import sleep
from multiprocessing.managers import ValueProxy
from multiprocessing import Queue, Process, Pipe, Event, Value, Manager
from multiprocessing.synchronize import Event as EventHint

clear_console = lambda: os.system('clear')

WIN_NUMBER = 100
SLEEPTIME = 0.05


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def tug(tug_progress: ValueProxy, change: int, not_done_flag: EventHint = False):
    while not_done_flag:
        #print('Gustav was here')
        tug_progress.set(tug_progress.get() + change)
        sleep(SLEEPTIME)


def main():

    progress = Manager().Value('i', WIN_NUMBER // 2)
    not_done_flag = Event()

    tug_right = Process(target=tug, args=(progress, 1, not_done_flag))
    tug_left = Process(target=tug, args=(progress, -1, not_done_flag))

    tug_right.start()
    tug_left.start()

    while abs(current_progress := progress.get()) < WIN_NUMBER:
        #clear_console()
        tug_string = bcolors.FAIL + '=' * current_progress
        tug_string += bcolors.OKBLUE + '0'
        tug_string += bcolors.OKGREEN + '=' * (WIN_NUMBER - current_progress)
        print(tug_string)
        sleep(SLEEPTIME)

    print(bcolors.BOLD)

    if current_progress > 100:
        print("left side won!")
    else:
        print("Right side won!")

    not_done_flag.set()

    tug_right.join()
    tug_left.join()


if __name__ == '__main__':
    main()
