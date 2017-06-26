import subprocess as sp
import argparse

#input string and list of strings
#output list of strings of split origional string
def sever(s, l):
    s = [s]
    n = []
    print("Sever:")
    print(s)
    print(l)
    print
    for e in l:
        print(e)
        for i in s:
            print(i)
            n.append(i.split(e))
        s = n
        n = []
        print(s)
    print
    print

#input: string of help result to do an initial pass on
#output: dict of valuable display parts
#Parses the Help text of function
def Parse(str):
    arr = str.split("\r")[1:]#technically from 0 onward in a standard function
    segment = False #segment 0: logic segment 1: help
    logic = ""
    help = []
    helpHelper = {"Name": "","Text": ""}
    for a in arr:
        a = a.strip()
        if (a != ""):
            if "optional arguments:" in a:
                segment = True
            elif (segment==False):
                logic = logic + a
            elif (segment==True):
                #if it is a dashed line:
                if (a[0]=='-'):
                    #add the last bit of helper code to the help array
                    if (helpHelper!={}):
                        help.append(helpHelper)
                        helpHelper = {"Name": "","Text": ""}
                    n = a.split(" ") #n[2:] will return help text, earlier is the informatino on the param
                    helpHelper.update({"Name":n[0].strip("-")})
                    helpText = ""
                    for e in n[2:]:
                        helpText = helpText + e + " "
                    helpHelper.update({"Text": helpHelper["Text"] + helpText.strip()})
                else:
                    helpHelper.update({"Text": helpHelper["Text"] + a})
    print("Endput")
    print(help)
    #parsing logic more heavily
    logic = logic.split(".py ")[1]
    print(logic)

#input: Dictionary to fold
#output: Filename
#Places a dictionary into a .txt file in a reasonable manner
def Fold(dict):
    return

#input: Filename
#output: Dictionary from file
#Does the inverse of Fold
#wont ever be used here but here for documentation purposes
def UnFold(filename):
    return



parser = argparse.ArgumentParser()
parser.add_argument("-pyfile", required=True)
args = parser.parse_args()
print(args.pyfile + "\n")
popen = sp.Popen('python %s --help' %args.pyfile, stdout=sp.PIPE)
print(popen)
str = popen.stdout.read()
Parse(str)
