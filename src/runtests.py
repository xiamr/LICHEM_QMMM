###################################################
#                                                 #
#   LICHEM: Layered Interacting CHEmical Models   #
#                                                 #
#        Symbiotic Computational Chemistry        #
#                                                 #
###################################################

#LICHEM semi-automated test suite

#Modules
import subprocess
import time
import sys
import os

#Start timer and counters immediately
StartTime = time.time()
passct = 0
failct = 0

#Development settings
#NB: Modified by the Makefile
UpdateResults = 0 #Flag to print energies to update tests
ForceAll = 0 #Flag to force it to do tests even if they will fail

#Classes
class ClrSet:
  #Unicode colors
  Norm = '\033[0m'
  Red = '\033[91m'
  Bold = '\033[1m'
  Green = '\033[92m'
  Blue = '\033[94m'
  Cyan = '\033[36m'
  #Set colors
  TFail = Bold+Red #Highlight failed tests
  TPass = Bold+Green #Highlight passed tests
  Reset = Norm #Reset to defaults

#Functions
def RunLICHEM(xname,rname,cname):
  #Submit LICHEM jobs
  cmd = "lichem -n "
  cmd += `Ncpus`
  cmd += " "
  cmd += "-x "
  cmd += xname
  cmd += " "
  cmd += "-r "
  cmd += rname
  cmd += " "
  cmd += "-c "
  cmd += cname
  cmd += " "
  cmd += "-o trash.xyz "
  cmd += "> tests.out " #Capture stdout
  cmd += "2>&1" #Capture stderr
  subprocess.call(cmd,shell=True) #Run calculations
  return

def CleanFiles():
  #Delete junk files
  cleancmd = "rm -f"
  #Remove LICHEM files
  cleancmd += " BASIS tests.out trash.xyz"
  cleancmd += " BeadStartStruct.xyz BurstStruct.xyz"
  #Remove TINKER files
  cleancmd += " tinker.key"
  #Remove LAMMPS files
  cleancmd += ""
  #Remove AMBER files
  cleancmd += ""
  #Remove Gaussian files
  cleancmd += " *.chk"
  #Remove PSI4 files
  cleancmd += " timer.* psi.* *.32 *.180"
  #Remove NWChem files
  cleancmd += " *.movecs"
  #Delete the files
  subprocess.call(cleancmd,shell=True)
  return

def RecoverEnergy(txtlabel,itemnum):
  #Recover the energy from LICHEM output
  cmd = ""
  cmd += "grep -e "
  cmd += '"'
  cmd += txtlabel
  cmd += ' "'
  cmd += " tests.out"
  savedresult = "Crashed..."
  try:
    #Safely check energy
    finalenergy = subprocess.check_output(cmd,shell=True) #Get results
    finalenergy = finalenergy.split()
    finalenergy = float(finalenergy[itemnum])
    savedresult = "Energy: "+`finalenergy` #Save it for later
    finalenergy = round(finalenergy,5)
  except:
    #Calculation failed
    finalenergy = 0.0
  return finalenergy,savedresult

def AddPass(TestPass,txtln,pct,fct):
  #Add a colored pass or fail message
  if (TestPass == 1):
    txtln += ClrSet.TPass+"Pass"+ClrSet.Reset+","
    pct += 1
  else:
    txtln += ClrSet.TFail+"Fail"+ClrSet.Reset+","
    fct += 1
  return txtln,pct,fct

def AddRunTime(txtln):
  #Collect the LICHEM run time and add it to a string
  cmd = ""
  cmd += "grep -e"
  cmd += ' "Total wall time: " ' #Find run time
  cmd += "tests.out"
  try:
    RunTime = subprocess.check_output(cmd,shell=True) #Get run time
    RunTime = RunTime.split()
    RunTime = " "+('%.4f'%round(float(RunTime[3]),4))+" "+RunTime[4]
  except:
    RunTime = " N/A"
  txtln += RunTime
  return txtln

def AddEnergy(devopt,txtln,enval):
  if (devopt == 1):
    txtln += ", "
    txtln += enval
  return txtln

#Print title
line = '\n'
line += "***************************************************"
line += '\n'
line += "*                                                 *"
line += '\n'
line += "*   LICHEM: Layered Interacting CHEmical Models   *"
line += '\n'
line += "*                                                 *"
line += '\n'
line += "*        Symbiotic Computational Chemistry        *"
line += '\n'
line += "*                                                 *"
line += '\n'
line += "***************************************************"
line += '\n'
print(line)

#Read arguments
DryRun = 0 #Only check packages
AllTests = 0 #Run all tests at once
if (len(sys.argv) == 3):
  if ((sys.argv[2]).lower() == "all"):
    #Automatically run all tests
    AllTests = 1
if (len(sys.argv) < 4):
  line = ""
  if (AllTests == 0):
    #Print help if arguments are missing
    line += "Usage:"
    line += '\n'
    line += " user:$ ./runtests Ncpus All"
    line += '\n'
    line += "  or "
    line += '\n'
    line += " user:$ ./runtests Ncpus QMPackage MMPackage"
    line += '\n'
    line += "  or "
    line += '\n'
    line += " user:$ ./runtests Ncpus QMPackage MMPackage dry"
    line += '\n'
    line += '\n'
  #Find LICHEM
  line += "LICHEM binary: "
  cmd = "which lichem"
  try:
    #Find path
    LICHEMbin = subprocess.check_output(cmd,shell=True)
    LICHEMbin = ClrSet.TPass+LICHEMbin.strip()+ClrSet.Reset
  except:
    LICHEMbin = ClrSet.TFail+"N/A"+ClrSet.Reset
  line += LICHEMbin
  line += '\n'
  line += '\n'
  #Identify QM wrappers
  line += "Available QM wrappers:"
  line += '\n'
  line += " PSI4: "
  cmd = "which psi4"
  try:
    #Find path
    QMbin = subprocess.check_output(cmd,shell=True)
    QMbin = ClrSet.TPass+QMbin.strip()+ClrSet.Reset
  except:
    QMbin = ClrSet.TFail+"N/A"+ClrSet.Reset
  line += QMbin
  line += '\n'
  line += " Gaussian: "
  cmd = "which g09"
  try:
    #Find path
    QMbin = subprocess.check_output(cmd,shell=True)
    QMbin = ClrSet.TPass+QMbin.strip()+ClrSet.Reset
  except:
    QMbin = ClrSet.TFail+"N/A"+ClrSet.Reset
  line += QMbin
  line += '\n'
  line += " NWChem: "
  cmd = "which nwchem"
  try:
    #Find path
    QMbin = subprocess.check_output(cmd,shell=True)
    QMbin = ClrSet.TPass+QMbin.strip()+ClrSet.Reset
  except:
    QMbin = ClrSet.TFail+"N/A"+ClrSet.Reset
  line += QMbin
  line += '\n'
  line += '\n'
  #Identify MM wrappers
  line += "Available MM wrappers:"
  line += '\n'
  line += " TINKER: "
  cmd = "which analyze"
  try:
    #Find path
    MMbin = subprocess.check_output(cmd,shell=True)
    MMbin = ClrSet.TPass+MMbin.strip()+ClrSet.Reset
  except:
    MMbin = ClrSet.TFail+"N/A"+ClrSet.Reset
  line += MMbin
  line += '\n'
  line += " LAMMPS: "
  cmd = "which lammps"
  try:
    #Find path
    MMbin = subprocess.check_output(cmd,shell=True)
    MMbin = ClrSet.TPass+MMbin.strip()+ClrSet.Reset
  except:
    MMbin = ClrSet.TFail+"N/A"+ClrSet.Reset
  line += MMbin
  line += '\n'
  line += " AMBER: "
  cmd = "which pmemd"
  try:
    #Find path
    MMbin = subprocess.check_output(cmd,shell=True)
    MMbin = ClrSet.TPass+MMbin.strip()+ClrSet.Reset
  except:
    MMbin = ClrSet.TFail+"N/A"+ClrSet.Reset
  line += MMbin
  line += '\n'
  print(line)
  if (AllTests == 0):
    #Quit
    exit(0)

Ncpus = int(sys.argv[1]) #Threads
if (AllTests == 0):
  QMPack = sys.argv[2] #QM wrapper for calculations
  QMPack = QMPack.lower()
  MMPack = sys.argv[3] #MM wrapper for calculations
  MMPack = MMPack.lower()
  if (len(sys.argv) > 4):
    if ((sys.argv[4]).lower() == "dry"):
      #Quit early
      DryRun = 1

#Initialize variables
LICHEMbin = ""
QMbin = ""
MMbin = ""

#Check packages and identify missing binaries
BadLICHEM = 0
cmd = "which lichem"
try:
  #Find path
  LICHEMbin = subprocess.check_output(cmd,shell=True)
  LICHEMbin = LICHEMbin.strip()
except:
  LICHEMbin = "N/A"
  BadLICHEM = 1
if (BadLICHEM == 1):
  #Quit with an error
  line = ""
  line += "Error: LICHEM binary not found!"
  line += '\n'
  print(line)
  exit(0)
if (AllTests == 0):
  BadQM = 1
  if ((QMPack == "psi4") or (QMPack == "psi")):
    QMPack = "PSI4"
    cmd = "which psi4"
    try:
      #Find path
      QMbin = subprocess.check_output(cmd,shell=True)
      QMbin = QMbin.strip()
    except:
      QMbin = "N/A"
    BadQM = 0
  if ((QMPack == "gaussian") or (QMPack == "g09")):
    QMPack = "Gaussian"
    cmd = "which g09"
    try:
      #Find path
      QMbin = subprocess.check_output(cmd,shell=True)
      QMbin = QMbin.strip()
    except:
      QMbin = "N/A"
    BadQM = 0
  if (QMPack == "nwchem"):
    QMPack = "NWChem"
    cmd = "which nwchem"
    try:
      #Find path
      QMbin = subprocess.check_output(cmd,shell=True)
      QMbin = QMbin.strip()
    except:
      QMbin = "N/A"
    BadQM = 0
  if (BadQM == 1):
    #Quit with an error
    line = '\n'
    line += "Error: QM package name '"
    line += QMPack
    line += "' not recognized."
    line += '\n'
    print(line)
    exit(0)
  BadMM = 1
  if (MMPack == "tinker"):
    MMPack = "TINKER"
    cmd = "which analyze"
    try:
      #Find path
      MMbin = subprocess.check_output(cmd,shell=True)
      MMbin = MMbin.strip()
    except:
      MMbin = "N/A"
    BadMM = 0
  if (MMPack == "lammps"):
    MMPack = "LAMMPS"
    cmd = "which lammps"
    try:
      #Find path
      MMbin = subprocess.check_output(cmd,shell=True)
      MMbin = MMbin.strip()
    except:
      MMbin = "N/A"
    BadMM = 0
  if (MMPack == "amber"):
    MMPack = "AMBER"
    cmd = "which pmemd" #Check
    try:
      #Find path
      MMbin = subprocess.check_output(cmd,shell=True)
      MMbin = MMbin.strip()
    except:
      MMbin = "N/A"
    BadMM = 0
  if (BadMM == 1):
    #Quit with error
    line = '\n'
    line += "Error: MM package name '"
    line += MMPack
    line += "' not recognized."
    line += '\n'
    print(line)
    exit(0)

#Print settings
line = "Settings:"
line += '\n'
line += " Threads: "
line += `Ncpus`
line += '\n'
if (AllTests == 0):
  line += " LICHEM binary: "
  line += LICHEMbin
  line += '\n'
  line += " QM package: "
  line += QMPack
  line += '\n'
  line += " Binary: "
  line += QMbin
  line += '\n'
  line += " MM package: "
  line += MMPack
  line += '\n'
  line += " Binary: "
  line += MMbin
  line += '\n'
else:
  if (ForceAll == 1):
    line += " Mode: Development"
  else:
    line += " Mode: All tests"
  line += '\n'
if (DryRun == 1):
  line += " Mode: Dry run"
  line += '\n'
print(line)

#Escape for dry runs
if (DryRun == 1):
  #Quit without an error
  line = "Dry run completed."
  line += '\n'
  print(line)
  exit(0)

#Escape if binaries not found
if (((QMbin == "N/A") or (MMbin == "N/A")) and (AllTests == 0)):
  #Quit with an error
  line = "Error: Missing binaries."
  line += '\n'
  print(line)
  exit(0)

line = "***************************************************"
line += '\n'
line += '\n'
line += "Running LICHEM tests..."
line += '\n'
print(line)

#Make a list of tests
QMTests = []
MMTests = []
if (AllTests == 1):
  #Safely add PSI4
  cmd = "which psi4"
  try:
    #Run PSI4 tests
    PackBin = subprocess.check_output(cmd,shell=True)
    QMTests.append("PSI4")
  except:
    #Skip tests that will fail
    if (ForceAll == 1):
      QMTests.append("PSI4")
  #Safely add Gaussian
  cmd = "which g09"
  try:
    #Run Gaussian tests
    PackBin = subprocess.check_output(cmd,shell=True)
    QMTests.append("Gaussian")
  except:
    #Skip tests that will fail
    if (ForceAll == 1):
      QMTests.append("Gaussian")
  #Safely add NWChem
  cmd = "which nwchem"
  try:
    #Run NWChem tests
    PackBin = subprocess.check_output(cmd,shell=True)
    QMTests.append("NWChem")
  except:
    #Skip tests that will fail
    if (ForceAll == 1):
      QMTests.append("NWChem")
  #Safely add TINKER
  cmd = "which analyze"
  try:
    #Run TINKER tests
    PackBin = subprocess.check_output(cmd,shell=True)
    MMTests.append("TINKER")
  except:
    #Skip tests that will fail
    if (ForceAll == 1):
      MMTests.append("TINKER")
  #Safely add lammps
  cmd = "which lammps"
  try:
    #Run LAMMPS tests
    PackBin = subprocess.check_output(cmd,shell=True)
    MMTests.append("LAMMPS")
  except:
    #Skip tests that will fail
    if (ForceAll == 1):
      MMTests.append("LAMMPS")
  #Safely add AMBER
  cmd = "which pmemd"
  try:
    #Run AMBER tests
    PackBin = subprocess.check_output(cmd,shell=True)
    MMTests.append("AMBER")
  except:
    #Skip tests that will fail
    if (ForceAll == 1):
      MMTests.append("AMBER")
else:
  #Add only the specified packages
  QMTests.append(QMPack)
  MMTests.append(MMPack)

#Loop over tests
for qmtest in QMTests:
  for mmtest in MMTests:
    #Set packages
    QMPack = qmtest
    MMPack = mmtest

    #Set path based on packages
    DirPath = ""
    if (QMPack == "PSI4"):
      DirPath += "PSI4_"
    if (QMPack == "Gaussian"):
      DirPath += "Gau_"
    if (QMPack == "NWChem"):
      DirPath += "NWChem_"
    DirPath += MMPack
    DirPath += "/"

    #Change directory
    os.chdir(DirPath)

    #Start printing results
    line = QMPack+"/"+MMPack
    line += " results:"
    print(line)

    #Check HF energy
    if ((QMPack == "PSI4") or (QMPack == "Gaussian")):
      line = ""
      PassEnergy = 0
      RunLICHEM("waterdimer.xyz","hfreg.inp","watercon.inp")
      QMMMEnergy,SavedEnergy = RecoverEnergy("QM energy:",2)
      #Check result
      if (QMPack == "PSI4"):
        #Check against saved energy
        if (QMMMEnergy == round(-4136.9303981392,5)):
          PassEnergy = 1
      if (QMPack == "Gaussian"):
        #Check against saved energy
        if (QMMMEnergy == round(-4136.9317704519,5)):
          PassEnergy = 1
      line += " HF energy:           "
      line,passct,failct = AddPass(PassEnergy,line,passct,failct)
      line = AddRunTime(line)
      line = AddEnergy(UpdateResults,line,SavedEnergy)
      print(line)
      CleanFiles() #Clean up files

    #Check DFT energy
    line = ""
    PassEnergy = 0
    RunLICHEM("waterdimer.xyz","pbereg.inp","watercon.inp")
    QMMMEnergy,SavedEnergy = RecoverEnergy("QM energy:",2)
    #Check result
    if (QMPack == "PSI4"):
      #Check against saved energy
      if (QMMMEnergy == round(-4154.1683659877,5)):
        PassEnergy = 1
    if (QMPack == "Gaussian"):
      #Check against saved energy
      if (QMMMEnergy == round(-4154.1676114324,5)):
        PassEnergy = 1
    if (QMPack == "NWChem"):
      #Check against saved energy
      if (QMMMEnergy == round(-4154.1683939169,5)):
        PassEnergy = 1
    line += " PBE0 energy:         "
    line,passct,failct = AddPass(PassEnergy,line,passct,failct)
    line = AddRunTime(line)
    line = AddEnergy(UpdateResults,line,SavedEnergy)
    print(line)
    CleanFiles() #Clean up files

    #Check CCSD energy
    if (QMPack == "PSI4"):
      line = ""
      PassEnergy = 0
      RunLICHEM("waterdimer.xyz","ccsdreg.inp","watercon.inp")
      QMMMEnergy,SavedEnergy = RecoverEnergy("QM energy:",2)
      #Check result
      if (QMPack == "PSI4"):
        #Check against saved energy
        if (QMMMEnergy == round(-4147.730483706,5)):
          PassEnergy = 1
      line += " CCSD energy:         "
      line,passct,failct = AddPass(PassEnergy,line,passct,failct)
      line = AddRunTime(line)
      line = AddEnergy(UpdateResults,line,SavedEnergy)
      print(line)
      CleanFiles() #Clean up files

    #Check PM6 energy
    if (QMPack == "Gaussian"):
      line = ""
      PassEnergy = 0
      RunLICHEM("waterdimer.xyz","pm6reg.inp","watercon.inp")
      QMMMEnergy,SavedEnergy = RecoverEnergy("QM energy:",2)
      #Check result
      if (QMPack == "Gaussian"):
        #Check against saved energy
        if (QMMMEnergy == round(-4.8623027634995,5)):
          PassEnergy = 1
      line += " PM6 energy:          "
      line,passct,failct = AddPass(PassEnergy,line,passct,failct)
      line = AddRunTime(line)
      line = AddEnergy(UpdateResults,line,SavedEnergy)
      print(line)
      CleanFiles() #Clean up files

    #Check NEB optimization
    line = ""
    PassEnergy = 0
    cmd = "cp methflbeads.xyz BeadStartStruct.xyz"
    subprocess.call(cmd,shell=True) #Copy restart file
    RunLICHEM("methfluor.xyz","nebreg.inp","methflcon.inp")
    QMMMEnergy,SavedEnergy = RecoverEnergy("Opt. step: 2",11)
    #Check result
    if (QMPack == "PSI4"):
      #Check against saved energy
      if (QMMMEnergy == round(-6511.0580192214,5)):
        PassEnergy = 1
    if (QMPack == "Gaussian"):
      #Check against saved energy
      if (QMMMEnergy == round(-6511.0567955964,5)):
        PassEnergy = 1
    if (QMPack == "NWChem"):
      #Check against saved energy
      if (QMMMEnergy == round(-6511.0579547077,5)):
        PassEnergy = 1
    line += " NEB TS energy:       "
    line,passct,failct = AddPass(PassEnergy,line,passct,failct)
    line = AddRunTime(line)
    line = AddEnergy(UpdateResults,line,SavedEnergy)
    print(line)
    CleanFiles() #Clean up files

    #TINKER tests
    if (MMPack == "TINKER"):
      #Check MM energy
      line = ""
      PassEnergy = 0
      cmd = "cp pchrg.key tinker.key"
      subprocess.call(cmd,shell=True) #Copy key file
      RunLICHEM("waterdimer.xyz","mmreg.inp","watercon.inp")
      QMMMEnergy,SavedEnergy = RecoverEnergy("MM energy:",2)
      #Check result
      if (QMMMEnergy == round(-0.2596903536223,5)):
        #Check against saved energy
        PassEnergy = 1
      line += " TIP3P energy:        "
      line,passct,failct = AddPass(PassEnergy,line,passct,failct)
      line = AddRunTime(line)
      line = AddEnergy(UpdateResults,line,SavedEnergy)
      print(line)
      CleanFiles() #Clean up files

      #Check MM energy
      line = ""
      PassEnergy = 0
      cmd = "cp pol.key tinker.key"
      subprocess.call(cmd,shell=True) #Copy key file
      RunLICHEM("waterdimer.xyz","solvreg.inp","watercon.inp")
      QMMMEnergy,SavedEnergy = RecoverEnergy("MM energy:",2)
      #Check result
      if (QMMMEnergy == round(-1.2549403662026,5)):
        #Check against saved energy
        PassEnergy = 1
      line += " AMOEBA/GK energy:    "
      line,passct,failct = AddPass(PassEnergy,line,passct,failct)
      line = AddRunTime(line)
      line = AddEnergy(UpdateResults,line,SavedEnergy)
      print(line)
      CleanFiles() #Clean up files

      #Check QMMM point-charge energy results
      line = ""
      PassEnergy = 0
      cmd = "cp pchrg.key tinker.key"
      subprocess.call(cmd,shell=True) #Copy key file
      RunLICHEM("waterdimer.xyz","pchrgreg.inp","watercon.inp")
      QMMMEnergy,SavedEnergy = RecoverEnergy("QMMM energy:",2)
      #Check result
      if (QMPack == "PSI4"):
        #Check against saved energy
        if (QMMMEnergy == round(-2077.2021947277,5)):
          PassEnergy = 1
      if (QMPack == "Gaussian"):
        #Check against saved energy
        if (QMMMEnergy == round(-2077.2018207808,5)):
          PassEnergy = 1
      if (QMPack == "NWChem"):
        #Check against saved energy
        if (QMMMEnergy == round(-2077.2022117306,5)):
          PassEnergy = 1
      line += " PBE0/TIP3P energy:   "
      line,passct,failct = AddPass(PassEnergy,line,passct,failct)
      line = AddRunTime(line)
      line = AddEnergy(UpdateResults,line,SavedEnergy)
      print(line)
      CleanFiles() #Clean up files

      #Check QMMM polarizable energy results
      line = ""
      PassEnergy = 0
      cmd = "cp pol.key tinker.key"
      subprocess.call(cmd,shell=True) #Copy key file
      RunLICHEM("waterdimer.xyz","polreg.inp","watercon.inp")
      QMMMEnergy,SavedEnergy = RecoverEnergy("QMMM energy:",2)
      #Check result
      if (QMPack == "PSI4"):
        #Check against saved energy
        if (QMMMEnergy == round(-2077.1114201829,5)):
          PassEnergy = 1
      if (QMPack == "Gaussian"):
        #Check against saved energy
        if (QMMMEnergy == round(-2077.1090319595,5)):
          PassEnergy = 1
      if (QMPack == "NWChem"):
        #Check against saved energy
        if (QMMMEnergy == round(-2077.1094168459,5)):
          PassEnergy = 1
      line += " PBE0/AMOEBA energy:  "
      line,passct,failct = AddPass(PassEnergy,line,passct,failct)
      line = AddRunTime(line)
      line = AddEnergy(UpdateResults,line,SavedEnergy)
      print(line)
      CleanFiles() #Clean up files

      #Check pseudobond optimizations
      if ((QMPack == "Gaussian") or (QMPack == "NWChem")):
        line = ""
        PassEnergy = 0
        cmd = "cp pbopt.key tinker.key"
        subprocess.call(cmd,shell=True) #Copy key file
        cmd = "cp pbbasis.txt BASIS"
        subprocess.call(cmd,shell=True) #Copy BASIS set file
        RunLICHEM("alkyl.xyz","pboptreg.inp","alkcon.inp")
        QMMMEnergy,SavedEnergy = RecoverEnergy("Opt. step: 2",6)
        #Check result
        if (QMPack == "Gaussian"):
          #Check against saved energy
          if (QMMMEnergy == round(-3015.0548490566,5)):
            PassEnergy = 1
        if (QMPack == "NWChem"):
          #Check against saved energy
          if (QMMMEnergy == round(-3015.2278310975,5)):
            PassEnergy = 1
        line += " DFP/Pseudobonds:     "
        line,passct,failct = AddPass(PassEnergy,line,passct,failct)
        line = AddRunTime(line)
        line = AddEnergy(UpdateResults,line,SavedEnergy)
        print(line)
        CleanFiles() #Clean up files

    #Print blank line and change directory
    line = ""
    print(line)
    os.chdir("../")

#Start printing the statistics
line = ""
line += "***************************************************"
line += '\n'
line += '\n'
line += "Statistics:"
line += '\n'
line += " Tests passed: "+`passct`+'\n'
line += " Tests failed: "+`failct`+'\n'

#Stop timer
EndTime = time.time()
TotalTime = (EndTime-StartTime)

#Find the correct units
TimeUnits = " seconds"
if (TotalTime > 60):
  TotalTime /= 60.0
  TimeUnits = " minutes"
  if (TotalTime > 60):
    TotalTime /= 60.0
    TimeUnits = " hours"
    if (TotalTime > 24):
      TotalTime /= 24
      TimeUnits = " days"

#Finish printing the statistics
line += " Total run time: "+('%.2f'%round(TotalTime,2))+TimeUnits+'\n'
line += '\n'
line += "***************************************************"
line += '\n'
line += '\n'
line += "Done."
line += '\n'
print(line)

#Quit
exit(0)

