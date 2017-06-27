import subprocess as sp
import argparse
import re

#input: string of help result to do an initial pass on
#output: dict of valuable display parts
#Parses the Help text of function
def Parse(str):
    arr = str.split("\r")[1:]#technically from 0 onward in a standard function
    segment = False #segment 0: logic segment 1: help
    logic = ""
    help = {}
    helpHelper = {"Text": "","Type": (-1, [])}
    groups = []
    counter = 0
    perserve = []
    #The goal in this piece of code is to extract out the individual meaning of each of the lines of the text a being an individual line
    #Then the logics, aka what is needed and what is optional, is placed in a string to be furthur paresed when all the logics end
    #after the logics end then the help text parsing is started and it uses the logics to slowly build the dict that it should output
    for a in arr:
        a = a.strip()
        if (a != ""):
            if "optional arguments:" in a:
                segment = True
                logic = logic.split(".py ")[1]
                logicexp = re.compile("\[-+(\w+)|\(-+(\w+)|\| ?-+(\w+)")
                #splits the logic part into three groups, group 1 starts with [, group 2 starts with (, and group 3 starts with |
                groups = logicexp.findall(logic)
            elif (segment==False):
                logic = logic + a
            elif (segment==True):
                #if it is a dashed line:
                if (a[0]=='-'):
                    #add the last bit of helper code to the help array
                    if (helpHelper!={"Text": "","Type": (-1, [])}):
                        help.update({groups[counter]: helpHelper})
                        helpHelper = {"Text": "","Type": (-1, [])}
                        counter += 1

                    n = a.split(" ") #n[2:] will return help text, earlier is the informatino on the param
                    helpText = ""
                    for e in n[2:]: #make my function clearer
                        helpText = helpText + e + " "
                    helpHelper.update({"Text": helpHelper["Text"] + helpText.strip()})
                    #group 1 is not required, while group 2 is mutually required with any group 3's that follow it, but each individual group 2 is required
                    if (groups[counter][0]!=''):
                        helpHelper.update({"Type": (0, [])})
                        groups[counter] = groups[counter][0]
                    elif (groups[counter][1]!=''):
                        perserve = [] #stores the connection between mutually exclusive inputs
                        helpHelper.update({"Type": (1, perserve)})
                        groups[counter] = groups[counter][1]
                        perserve.append(groups[counter])
                    elif (groups[counter][2]!=''):
                        helpHelper.update({"Type": (1, perserve)})
                        groups[counter] = groups[counter][2]
                        perserve.append(groups[counter])
                else:
                    helpHelper.update({"Text": helpHelper["Text"] + a})
    print("Endput")
    print(help)
    return help




#input: Dictionary to fold
#output: Filename
#Places a dictionary into a .txt file in a reasonable manner
def Fold(dict, args):
    text_file = open("manifest_of_%s.txt" %args.pyfile, 'w')
    for e in dict.keys():
        text_file.write(str(e) + " " + dict[e]["Text"] + "\n\t" + str(dict[e]["Type"][0]) + "\n")
        for key in dict[e]["Type"][1]:
            text_file.write("\t\t" + str(key) + "\n")
    text_file.close()
    return "manifest_of_%s.txt" %args.pyfile
#The file produced by this can be edited by the user, adding links or removing them where wanted
#additional functionality will be added in the UnFold part to support initial values where possible, since this program cannot pick up if there are initial values


#input: Filename
#output: Dictionary from file
#Does the inverse of Fold
#wont ever be used here but here for documentation purposes
def UnFold(filename):
    text_file = open(filename, 'r')
    phrase = text_file.read()
    print phrase
    arr = phrase.split("\n")
    fieldsave = ""
    compiled = {}
    linksave= []
    #this parses line by line and determines the meaning from the amount of tabs used on that line
    for e in arr:
        if (e!=""):
            if (e[1]=="\t"):
                linksave.append(e.strip("\t"))
            elif (e[0]=="\t"):
                linksave= []
                compiled[fieldsave].update({"Type": (int(e),linksave)})
            else:
                p = e.split(" ",1)
                compiled.update({p[0]:{"Text": p[1]}})
                fieldsave = p[0]
    return compiled


#this part simply calls the function and sees what its output for help is and then pases the information on to parser
parser = argparse.ArgumentParser()
parser.add_argument("-pyfile", required=True)
args = parser.parse_args()
print(args.pyfile + "\n")
popen = sp.Popen('python %s --help' %args.pyfile, stdout=sp.PIPE)
print(popen)
stri = popen.stdout.read()
help = Parse(stri)
#folds the dict up into a text document
filenamef = Fold(help, args)
#this part here (the UnFold) would not be in the final program, it would be moved into the webapp so that the webapp could parse out the dict.
recomped = UnFold(filenamef)
print
print
print recomped
