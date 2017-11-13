import subprocess

# retVal & stdOut in file stream
retVal = subprocess.call(["ls","-al"])
retVal = subprocess.call(["ls","-al", "pippo"])
trash = open("/dev/null","w")
retVal = subprocess.call(["ls","-al"], stdout = trash)
retVal = subprocess.call(["ls","-alz"], stdout = trash, stderr = trash)
trash.close()

# stdOut
retStr = subprocess.check_output(["ls", "-al"])
for line in subprocess.check_output(["ls", "-al"]).splitlines():
    print(line.strip())
