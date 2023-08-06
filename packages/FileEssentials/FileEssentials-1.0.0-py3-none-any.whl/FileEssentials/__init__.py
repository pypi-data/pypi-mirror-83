import os

os.system("")

def CreateFile(name, ifexists = False):
    f = None
    if ifexists:
        if not os.path.exists(name):
            f = open(name, 'w+')
    else:
        f = open(name, 'w+')
    return f

def DeleteFile(name):
    if os.path.exists(name):
        os.remove(name)
    else:
        print("\033[91m", "The file does not exist", "\033[0m")
    
def ReadFile(name):
    f = open(name, 'r')
    contents = f.read()
    return contents

def ReadFileLines(name):
    f = open(name, 'r')
    contents = f.readlines()
    return contents

def ReadFileLine(name, line):
    f = open(name, 'r')
    lines = f.readlines()
    line = lines[line - 1]
    return line

def WriteFile(name, text):
    f = open(name, 'w')
    f.write(text)
    return f
    
def AppendFile(name, text):
    f = open(name, 'a')
    f.write(text)
    return f
    
def CheckFileExists(name):
    exists = os.path.exists(name)
    return exists