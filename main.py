import dataset
import facerecognition
import tranning
import os
import time
import sys


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    print("\t=================== MENU ===================")
    time.sleep(1)
    choise = input("""
        |      C: Create a new people.
        |      T: Trainng data.
        |      F: Run Camera.
        |      Q: Quit program.
        |               
        |      [Enter your choise] >> """)

    if choise == "C" or choise == "c":
        cls()
        dataset.run_dataset()
        menu()
    elif choise == "T" or choise == "t":
        cls()
        tranning.run_traning()
        menu()
    elif choise == "F" or choise == "f":
        cls()
        facerecognition.run_face()
        menu()

    elif choise == "Q" or choise == "q":
        cls()
        print("\n[INFO] Exit now...")
        time.sleep(1)
        sys.exit(0)
    else:
        cls()
        print("\n\t[INFO] You must only select either C, T, F or Q.")
        print("\t[INFO] Please try again...\n")
        menu()


# main program here
# menu()
if __name__ == "__main__":
    menu()
