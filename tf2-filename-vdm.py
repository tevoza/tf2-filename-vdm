# Loop through directories and attempt to generate vdm files for each demo
import os

#DIR = ""

def GetClipStr(action, ref, start, end):
    #build skip cmd string
    action +=1
    ClipStr = '\t"'+str(action)+'"\n\t{'
    ClipStr += '\tfactory "SkipAhead"\n\t\tname "skip"\n\t\t'
    ClipStr += 'starttick "'+str(ref)+'"\n\t\t'
    ClipStr += 'skiptotick "'+str(start-500)+'"\n\t}\n'

    #startRecordingStr
    action +=1
    ClipStr += '\t"'+str(action)+'"\n\t{\n'
    ClipStr += '\t\tfactory "PlayCommands"\n'
    ClipStr += '\t\tname "startrec"\n'
    ClipStr += '\t\tstarttick "'+str(start)+'"\n'
    ClipStr += '\t\tcommands "startrecording"\n\t}\n'

    #stopRecordingStr
    action += 1
    ClipStr += '\t"'+str(action)+'"\n\t{\n'
    ClipStr += '\t\tfactory "PlayCommands"\n'
    ClipStr += '\t\tname "stoprec"\n'
    ClipStr += '\t\tstarttick "'+str(end)+'"\n'
    ClipStr += '\t\tcommands "stoprecording"\n\t}\n'

    return ClipStr, action

def GetStopStr(action, refTick):
    action +=1
    StopStr = '\t"'+str(action)+'"\n\t{'
    StopStr += '\tfactory "PlayCommands"\n\t\tname "stopdem"\n\t\t'
    StopStr += 'starttick "'+str(refTick)+'"\n\t\t'
    StopStr += 'commands "stopdemo"\n\t}\n'

    return StopStr

def GetNextStr(action, refTick, nextDemo):
    global DIR
    action +=1
    NextStr = '\t"'+str(action)+'"\n\t{'
    NextStr += '\tfactory "PlayCommands"\n\t\tname "nextdem"\n\t\t'
    NextStr += 'starttick "'+str(refTick)+'"\n\t\t'
    NextStr += 'commands "playdemo '+ DIR + nextDemo +'"\n\t}\n'

    return NextStr

def MakeVDM(demo, nextDemo = None):
    demo = demo[:-4]
    filename = demo + ".vdm"
    NumFrags = demo.count("-")

    print("#Generating VDM for " + demo + " (" + str(NumFrags) + " clips)")

    processed = 0
    refTick = 1
    action = 0;

    #Cut off header
    print(demo)
    idx = demo.index("_")
    procStr = demo[idx+1:];
    print("Processing: " + procStr)
    command = ''

    while (processed < NumFrags):
        processed += 1

        #Find clip
        sep = procStr.find("_")
        if sep < 0:
            clipStr = procStr
        else:
            clipStr = procStr[:sep]

        print('#' + str(processed) + ": " + clipStr)

        #ID ticks for clip
        tickSep = clipStr.find("-")
        startTick = int(clipStr[:tickSep])
        endTick = int(clipStr[tickSep+1:])

        clipCommand, action = GetClipStr(action, refTick, startTick, endTick)
        command += clipCommand
        refTick = endTick+100

        procStr = procStr[sep+1:]

    if nextDemo == None:
        stopCommand = GetStopStr(action, refTick)
        command+= stopCommand
    else:
        nextCommand = GetNextStr(action, refTick, nextDemo)
        command+= nextCommand

    command = "demoactions\n{\n" + command + "}"

    return filename, command

if __name__ == "__main__":
    DIR = os.getcwd()

    AllFiles = os.listdir(DIR)
    files = [];
    #delete nondemo files from list
    for filename in AllFiles:
        print(filename)
        if filename.endswith(".dem"):
            files.append(filename)

    files = sorted(files)

    #get directory relative to tf/
    idx = DIR.find("tf/")
    DIR = DIR[idx+3:]+"/"

    #Generate vdms
    for idx, filename in enumerate(files):
        if idx < len(files) - 1:
            filename, VDM = MakeVDM(files[idx], files[idx+1])
        else:
            filename, VDM = MakeVDM(files[idx])

        f = open(filename, "w")
        f.write(VDM)
        f.close()

    print("VDMs created! Start at " + files[0])
