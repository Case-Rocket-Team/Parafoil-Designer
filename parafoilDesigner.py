import json
import math
import pandas as pd
from CoefficientCalc import CoefficientCalc

parafoil = {
        'Angle of Attack' : 0,              # deg
        'Angle of Zero Lift' : 0,           # deg, obtained from xfoil
        'Angle of Max L/D': 0,              # deg
        'CL of Max L/D' : 0,                # coeff of lift at max l/d, used for slope calc
        'Profile CL alpha' : 0,             # coeff of lift at desired angle of attack
        'Profile CD alpha' : 0,             # obtained from xfoil
        'Span' : 0,                         # m
        'Chord' : 0,                        # m length of parafoil
        'Cells' : 0,                        # number of cells
        'Line' : {
            'Thickness' : 0,                # m
            'Length' : 0,                   # m length of lines, radius payload is from arc of chute, design for length = 0.6 * span
        },
        'Inlet Height' : 0,                 # m, design for 0.14 * chord
        'Vehicle Coefficients' : {
            'CL' : 0,
            'CD' : 0,
        }
    }

def csvFileRead(csvName):
    return pd.read_csv(csvName)

def getAngleZeroLift(parafoil_data):
    cl = parafoil_data['CL']
    # Finds at what angle of attack cl = 0
    for i in range(len(cl) - 1, 0, -1):
        if cl[i] == 0:
            parafoil['Angle of Zero Lift'] = round(parafoil_data['alpha'][i], 3)
        elif cl[i] < 0:
            parafoil['Angle of Zero Lift'] = round(parafoil_data['alpha'][i] - cl[i] * ((parafoil_data['alpha'][i + 1] - parafoil_data['alpha'][i]) / (cl[i + 1] - cl[i])), 3)
            break
        elif i == 0:
            print("!!!Your xfoil data does not contain the angle of zero lift!!!") 

def getMaxLDIndex(parafoil_data):
    ld = parafoil_data['CL'] / parafoil_data['CD']
    max_index = ld.idxmax()
    return max_index

def setMaxLDAngle(parafoil_data):
    max_index = getMaxLDIndex(parafoil_data)
    parafoil['Angle of Max L/D'] = parafoil_data['alpha'][max_index]
    parafoil['CL of Max L/D'] = parafoil_data['CL'][max_index]

def setAlpha(parafoil_data):
    alpha_check = input("Do you want to use alpha of max L/D (m) or custom alpha (c)? ")
    if alpha_check == "m":
        parafoil['Angle of Attack'] = parafoil['Angle of Max L/D']
        parafoil['Profile CL alpha'] = parafoil['CL of Max L/D']
        max_index = getMaxLDIndex(parafoil_data)
        parafoil['Profile CD alpha'] = parafoil_data['CD'][max_index]
    elif alpha_check == "c":
        parafoil['Angle of Attack'] = float(input("Enter desired angle of attack: "))
        alpha = parafoil_data['alpha']
        # Finds cl and cd for desired vehicle angle of attack
        for i in range(0, len(alpha) - 1, 1):
            if alpha[i] == parafoil['Angle of Attack']:
                parafoil['Profile CL alpha'] = parafoil_data['CL'][i]
                parafoil['Profile CD alpha'] = parafoil_data['CD'][i]
            elif alpha[i] > parafoil['Angle of Attack']:
                parafoil['Profile CL alpha'] = round(parafoil_data['CL'][i - 1] + (parafoil['Angle of Attack'] - alpha[i - 1]) * ((parafoil_data['CL'][i] - parafoil_data['CL'][i - 1]) / (alpha[i] - alpha[i - 1])), 3)
                parafoil['Profile CD alpha'] = round(parafoil_data['CD'][i - 1] + (parafoil['Angle of Attack'] - alpha[i - 1]) * ((parafoil_data['CD'][i] - parafoil_data['CD'][i - 1]) / (alpha[i] - alpha[i - 1])), 3)
                break
            elif i == len(alpha) - 1:
                print("!!!Your xfoil data does not contain your desired angle of attack!!!")
    else:
        print("The hell's wrong with you?")

def setAirfoilData(parafoil_data):
    getAngleZeroLift(parafoil_data)
    setMaxLDAngle(parafoil_data)
    setAlpha(parafoil_data)

def getUserData():
    parafoil['Span'] = float(input("Enter span of parafoil (m): "))
    parafoil['Chord'] = float(input("Enter chord of parafoil (m): "))
    if parafoil['Span'] / parafoil['Chord'] != 2:
        print("Aspect Ratio does not equal 2, will need to adjust tau and delta in the coefficient calculator")
    parafoil['Line']['Thickness'] = float(input("Enter thickness of lines (m): "))
    parafoil['Cells'] = float(input("Enter the number of cells the parafoil has: "))

def calcDesignParameters():
    parafoil['Line']['Length'] = round(0.6 * parafoil['Span'], 3)
    parafoil['Inlet Height'] = round(0.14 * parafoil['Chord'], 3)

def jsonFileWrite(jsonName):
    with open(jsonName, 'w') as outfile:
        json.dump(parafoil, outfile)

def jsonFileRead(jsonName):
    with open(jsonName) as f:
        parafoil.update(json.load(f))

def coeffWrite(cc):
    parafoil['Vehicle Coefficients']['CL'] = round(cc.clCalc(parafoil), 3)
    parafoil['Vehicle Coefficients']['CD'] = round(cc.cdCalc(parafoil), 3)

def writeRun(jsonName):
    cc = CoefficientCalc()
    parafoil_data = csvFileRead(input("Enter file name of editted csv from xfoil: "))
    setAirfoilData(parafoil_data)
    getUserData()
    calcDesignParameters()
    coeffWrite(cc)
    jsonFileWrite(jsonName)

def rewriteRun(jsonName):
    jsonFileRead(jsonName)
    cc = CoefficientCalc()
    parafoil_data = csvFileRead(input("Enter file name of editted csv from xfoil: "))
    setAlpha(parafoil_data)
    coeffWrite(cc)
    jsonFileWrite(jsonName)

def main():
    jsonName = input("Enter name of file to dump json data: ")
    rw_check = input("Do you want to write new data to file (w) or rewrite file with new Angle of Attack (r)? ")
    if rw_check == "w":
        writeRun(jsonName)
    elif rw_check == "r":
        rewriteRun(jsonName)
    else:
        print("The hell's wrong with you?")

if __name__ == '__main__':
    main()