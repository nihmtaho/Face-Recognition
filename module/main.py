from module import dataset, facerecognition, training
import os
import time
import sys


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    print("\t=================== MENU ===================")
    # time.sleep(1)
    choice = input("""
        |      C: Create a new people.
        |      T: Training data.
        |      F: Run Camera.
        |      Q: Quit program.
        |               
        |      [Enter your choice] >> """)

    if choice == "C" or choice == "c":
        cls()
        dataset.run_dataset()
        menu()
    elif choice == "T" or choice == "t":
        cls()
        training.run_training()
        menu()
    elif choice == "F" or choice == "f":
        cls()
        facerecognition.run_face()
        menu()

    elif choice == "Q" or choice == "q":
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