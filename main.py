#!/usr/bin/python3
from time import sleep
#from subprocess import call
from multiprocessing.managers import ValueProxy
from multiprocessing.synchronize import Event as EventHint
from multiprocessing import Process, Event, Manager

try:  # Change process names to something informational when setproctitle is installed.
    from setproctitle import setproctitle
except ImportError:  # setproctitle isn't installed, processes will use their default names.
    setproctitle = None

WIN_NUMBER = 200
SLEEPTIME = 0.05

score = [0, 0]


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


def tug(tug_progress: ValueProxy, change: int, done_flag: EventHint = False, name: str = None):
    try:
        if setproctitle is not None and name:
            setproctitle(name)

        while not done_flag.is_set():
            tug_progress.set(tug_progress.get() + change)
            sleep(SLEEPTIME)
    except KeyboardInterrupt:
        print(f"Stopped: '{name}'")  # Suppress KeyboardInterrupt traceback.


def main():

    progress = Manager().Value('i', WIN_NUMBER // 2)
    done_flag = Event()

    tug_right = Process(target=tug, args=(progress, 1, done_flag, "Python | tug right"))
    tug_left = Process(target=tug, args=(progress, -1, done_flag, "Python | tug left"))

    tug_right.start()
    tug_left.start()

    if setproctitle is not None:
        setproctitle("python | tug print")

    while (current_progress := progress.get()) in range(WIN_NUMBER + 1):
        print(f"{bcolors.FAIL}({score[0]})\t"
              f"{'=' * current_progress}"
              f"{bcolors.OKBLUE}{max(score) - min(score)}"  # 0
              f"{bcolors.OKGREEN}{'=' * (WIN_NUMBER - current_progress)}"
              f"\t({score[1]})")
        sleep(SLEEPTIME)
        #call(['clear'])  # Clears the console on UNIX systems; duh!

    print(bcolors.BOLD)

    if current_progress >= WIN_NUMBER:
        print(bcolors.OKGREEN + "Right side won!")
        score[1] += 1
    else:
        print(bcolors.FAIL + "Left side won!")
        score[0] += 1

    done_flag.set()

    tug_right.join(timeout=SLEEPTIME * 10)
    tug_left.join(timeout=SLEEPTIME * 10)

    tug_right.terminate()
    tug_left.terminate()


if __name__ == '__main__':
    # main()
    # raise SystemExit()
    try:
        while True:
            main()
            sleep(3)
    except KeyboardInterrupt:
        print(bcolors.ENDC, end='')
        pass  # Suppress the traceback.
