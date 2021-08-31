from time import sleep
from subprocess import call
from multiprocessing.managers import ValueProxy
from multiprocessing.synchronize import Event as EventHint
from multiprocessing import Process, Event, Manager

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


def tug(tug_progress: ValueProxy, change: int, done_flag: EventHint = False):
    while not done_flag.is_set():
        tug_progress.set(tug_progress.get() + change)
        sleep(SLEEPTIME)


def main():

    progress = Manager().Value('i', WIN_NUMBER // 2)
    done_flag = Event()

    tug_right = Process(target=tug, args=(progress, 1, done_flag))
    tug_left = Process(target=tug, args=(progress, -1, done_flag))

    tug_right.start()
    tug_left.start()

    while (current_progress := progress.get()) in range(WIN_NUMBER):
        tug_string = bcolors.FAIL + '=' * current_progress
        tug_string += bcolors.OKBLUE + '0'
        tug_string += bcolors.OKGREEN + '=' * (WIN_NUMBER - current_progress)
        print(tug_string)
        sleep(SLEEPTIME)
        #call(['clear'])  # Clears the console on UNIX systems; duh!

    print(bcolors.BOLD)

    if current_progress >= WIN_NUMBER:
        print(bcolors.OKGREEN + "Right side won!")
    else:
        print(bcolors.FAIL + "Left side won!")

    done_flag.set()

    tug_right.join()
    tug_left.join()


if __name__ == '__main__':
    main()
