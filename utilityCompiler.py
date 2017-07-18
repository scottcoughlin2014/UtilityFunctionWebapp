import subprocess as sp
import argparse
import re
#from ast import literal_eval as make_tuple #needed for making tuples


# input: string of help result to do an initial pass on
# output: dict of valuable display parts
# Parses the Help text of function
def Parse(inputString):
    # Shape of output:
    # a dict of param fields ex: i, verbose, v
    # that each hold a dict containing: "Field Name" (a string), "Help Text" (a string),
    # "Type" (a string), "Requirement Status" (a tupple with a number and a list), "Base Value" (a "Type")


    resultant = {}
    divOne = re.compile("(?s)usage:\s\w+(?:.py )?(.+)optional arguments:")  # this is the section with the logic
    # might be able to combine the following two
    divTwo = re.compile(
        "(?s)optional arguments:\s(.+)(?:required named arguments)?")  # this is the section with the optional or mutually exclusive arguments
    divThree = re.compile("(?s)required named arguments:\s(.+)")  # this is the section with the not optional arguements
    resultant = ParseLogic(resultant, divOne.findall(inputString)[0])
    docLong = divTwo.findall(inputString)[0]
    if (divThree.findall(inputString) != []):
        docLong = docLong + divThree.findall(inputString)[0]
    resultant = ParseDoc(resultant, docLong)
    return resultant


# inputs: the resultant dict and the logicals input
# outputs: the resultant dict with logical data added in so the entire dict should be defined and the inner dicts should have Mutually Exclusive Links set
def ParseLogic(resultant, input):
    print("Starting up Parsing of Logic")
    print(input)
    divOneParse = re.compile(
        "(?s)(?:\| | |\[|\()-+(.+?(?:(?=(?:\s(?:-|\[-|\(-))|$)))")  # this parses out the logic, group 1 tells you something about the type, group 2 tells you what field is
    divOneField = re.compile(
        "([^\s\]\)]+)(?:\s(([[(])?(?(3)[^])]+?[])]{1}|[^])]+)))?(\])?( \|)?(\))?( )?")  # group 1 is field name group 2 is input name
    # i belive that the next chunk of code here works... but a second pass should be taken before this is finalized
    mutualArr = []
    for a in divOneParse.findall(input):
        print(a)
        e = divOneField.findall(a)[0]
        print(e)
        print(mutualArr)  # ROFL xD
        resultant.update({e[0]: {}})
        # something isn't right here
        if (e[3] != ''):
            val = 0
        elif (e[5] != ''):
            val = 1
        elif (e[4] != ''):
            val = 2
        else:
            val = 3
        if (val == 0 or val == 1 or val == 3):
            mutualArr = [e[1]]
        elif (val == 2):
            mutualArr.append(e[1])
        resultant[e[0]].update({"Requirement Status": (val, mutualArr)})
        # make sure e is what i think it is before proceeding
    print("Ending Parsing of Logic \n\n")
    print(resultant)
    print("\n\n")
    return resultant


# inputs: the resultant dict and the help text input
# outputs: the resultant dict with the Help Text and Field Name added
def ParseDoc(resultant, input):
    print("Starting up Documentation Parsing")
    print(input)
    print("\n")
    # this next one parses out the text
    sectionCapture = re.compile(
        "(?s)(?:\s+-+(.+?))(?:(?=[\n\r]\s+-+)|$)")
    sectionParse = re.compile(
        "(?s)([^\s,]+)(?:\s([^\s,]+))?(?:,\s+-+([^\s]+)(?:\s([^\s]+))?)?\s+(.+)")
    #no longer in use
    #textParse = re.compile(
    #    "(?m)^\s+(-+.+$)(?:\s+([^-]+)$)*")  # group 1: param group 2: text... Doesn't function in every case properly, unsure why
    #paramParse = re.compile(
    #    "(?s)-+([^\s]+)\s(\w+)([\w\s\r\n\t.\(\)]+(?:(?=-)|))")  # this pares out the parameters, group 1 is field, group 2 is field name
    for e in sectionCapture.findall(input):
        print(e)
        a = sectionParse.findall(e)
        print(a)
        if (a != []): #if it actually matches something
            a = a[0]
            resultant[a[0]].update({"Field Name": a[1], "Help Text": a[4].strip()})

    print("Ending Documentation Parsing \n\n")
    print(resultant)
    print("\n\n")
    return resultant


# this is old code that may be used at a later time
def Unused():
    logic = ""
    help = {}  # stores the help text dict (the final result)
    helpHelper = {"Text": "", "Type": (-1, [])}
    groups = []
    counter = 0
    perserve = []
    # The goal in this piece of code is to extract out the individual meaning of each of the lines of the text a being an individual line
    # Then the logics, aka what is needed and what is optional, is placed in a string to be furthur paresed when all the logics end
    # after the logics end then the help text parsing is started and it uses the logics to slowly build the dict that it should output
    for a in arr:
        a = a.strip()
        if (a != ""):
            if "optional arguments:" in a:
                segment = True
                # we also need to deal with this :/
                logic = logic.split(".py ")[1]
                logicexp = re.compile("\[-+(\w+)|\(-+(\w+)|\| -+(\w+)| -+(\w+)")
                # splits the logic part into three groups, group 1 starts with [, group 2 starts with (, and group 3 starts with |
                groups = logicexp.findall(logic)
            elif (segment == False):
                logic = logic + a
            elif (segment == True):
                # if it is a dashed line:
                if (a[0] == '-'):
                    # add the last bit of helper code to the help array
                    if (helpHelper != {"Text": "", "Type": (-1, [])}):
                        help.update({groups[counter]: helpHelper})
                        helpHelper = {"Text": "", "Type": (-1, [])}
                        counter += 1

                    n = a.split(" ")  # n[2:] will return help text, earlier is the informatino on the param
                    helpText = ""
                    for e in n[2:]:  # make my function clearer
                        helpText = helpText + e + " "
                    helpHelper.update({"Text": helpHelper["Text"] + helpText.strip()})
                    # group 1 is not required, while group 2 is mutually required with any group 3's that follow it, but each individual group 2 is required
                    if (groups[counter][0] != ''):
                        helpHelper.update({"Type": (0, [])})
                        groups[counter] = groups[counter][0]
                    elif (groups[counter][1] != ''):
                        perserve = []  # stores the connection between mutually exclusive inputs
                        helpHelper.update({"Type": (1, perserve)})
                        groups[counter] = groups[counter][1]
                        perserve.append(groups[counter])
                    elif (groups[counter][2] != ''):
                        helpHelper.update({"Type": (1, perserve)})
                        groups[counter] = groups[counter][2]
                        perserve.append(groups[counter])
                else:
                    helpHelper.update({"Text": helpHelper["Text"] + a})
    print("Endput")
    print(help)
    return help


# input: Dictionary to fold
# output: Filename
# Places a dictionary into a .txt file in a reasonable manner
def Fold(dict, args):
    #format: dict of fields that each are dicts with {Field Name, Reqiurement Status, Help Text}
    print("Starting Fold: \n\n\n\n")
    text_file = open("manifest_of_%s.txt" % args.pyfile, 'w')
    for e in dict.keys():
        text_file.write(e + "\n")
        print(e + "\n")
        for a in dict[e].keys():
            text_file.write("\t" + a + " : " + str(dict[e][a]) + "\n")
            print("\t" + a + " : " + str(dict[e][a]) + "\n")
    text_file.close()
    return "manifest_of_%s.txt" % args.pyfile


# The file produced by this can be edited by the user, adding links or removing them where wanted
# additional functionality will be added in the UnFold part to support initial values where possible, since this program cannot pick up if there are initial values


# input: Filename
# output: Dictionary from file
# Does the inverse of Fold
# wont ever be used here but here for documentation purposes
def UnFold(filename):
    print("unfolding commencing.....\n\n\n\n\n\n\n\n\n\n\n\n")
    text_file = open(filename, 'r')
    phrase = text_file.read()
    print(phrase)
    arr = phrase.split("\n")
    print("------------------")
    fieldSplitter = re.compile("(?s)\s+(.+)\s:\s?(.+)?") #splits a field into the field name and the entry
    compiled = {}
    savedfield = ""
    last = ""
    # this parses line by line and determines the meaning from the amount of tabs used on that line
    for e in arr:
        print e
        if (e != ""): #this should never fail
            if (e[0] != "\t" and e[0] != " "):
                savedfield = str(e)
                compiled.update({savedfield:{}})
                print("Generating: "+savedfield)
            else:
                a = fieldSplitter.findall(e)
                print a
                if a != []:
                    a = a[0]
                    last = a[0]
                    if a[1] != "":
                        if a[1][0] == "(":
                            compiled[savedfield].update({last : maketuple(a[1])})
                        else:
                            compiled[savedfield].update({last: a[1]})
                        print("Adding "+last+" to: "+savedfield+" with value of: "+str(a[1]))
                else:
                    print compiled
                    compiled[savedfield].update({last: compiled[savedfield][last]+e.strip()})
    return compiled

def maketuple(string):
    print("I will make a tuple")
    formSplitter = re.compile("(?s)\((\d),\s\[(.+)\]\)")#splits into didget and inner part of the requirements
    listExtractor = re.compile("(?s)'([^']+)'")#identifys all the parts of a list
    temp = formSplitter.findall(string)[0]
    print temp
    int_imp = int(temp[0])
    temp = listExtractor.findall(temp[1])
    print temp
    tup = (int_imp, temp)
    print("tuple complete! :)")
    return tup

# this part simply calls the function and sees what its output for help is and then pases the information on to parser
parser = argparse.ArgumentParser()
parser.add_argument("-pyfile")
#these next three should be mutually exclusive
parser.add_argument("-fold")
parser.add_argument("-unfold")
parser.add_argument("-print")
args = parser.parse_args()
args.pyfile = "interface.py"
print(args.pyfile + "\n")
popen = sp.Popen('python %s --help' % args.pyfile, stdout=sp.PIPE, shell=True)
print(popen)
stri = popen.stdout.read()
print(stri)
help = Parse(stri)
# folds the dict up into a text document
filenamef = Fold(help, args)
# this part here (the UnFold) would not be in the final program, it would be moved into the webapp so that the webapp could parse out the dict.
recomped = UnFold(filenamef)
print
print
print help
print recomped
