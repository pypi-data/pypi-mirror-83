import os


refresh = lambda: os.system("cls")

class console:

    def log(log):
        print(log)

    def error(err):
        print("[error]: " + err)

    def warn(warn):
        print("[warn]: " + warn)

    def count(count):
        print(count, 1)

    def clear():
        refresh()



def prompt(prompt):
    str(input(prompt))

