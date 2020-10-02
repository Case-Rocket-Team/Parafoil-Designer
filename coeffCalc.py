import math
import matplotlib.pyplot as plt
import json

def clCalc(parafoil):
    epsilon = parafoil['Span'] / (4 * parafoil['Line']['Length'])
    AR = parafoil['Span'] / parafoil['Chord']                   # aspect ratio of span to chord
    if AR != 2:
        print("Aspect Ratio is not 2, tau value needs to be altered in code from paper")
        return 0
    if 1 < AR and AR < 2.5:
        k1 = 3.33 - AR * 1.33
    elif AR >= 2.5:
        k1 = 0
    else:
        print("That's not a good parafoil")
        return 0
    cl_slope = parafoil['Profile CL alpha'] / math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"])
    # k is a corrective term for the lift-curve slope for small aspect ratio wings
    k = (2 * math.pi * AR) / cl_slope * math.tanh(cl_slope / (2 * math.pi * AR))
    cl_slope_prime = cl_slope * k
    # tau is a corrective term for elliptic loading
    tau = 0.07
    cl_alpha = math.pi * AR * cl_slope_prime / (math.pi * AR + cl_slope_prime * (1 + tau))
    return cl_alpha, cl_alpha * math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"]) * math.cos(math.radians(epsilon)) ** 2 + k1 * math.sin(math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"])) ** 2 * math.cos(math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"]))
def calcPercentage(value, total):
    return value / total * 100
def cdCalc(parafoil, cl_alpha):
    # Drag due to 
    inlet_drag = 0.5 * parafoil['Inlet Height'] / parafoil['Chord']
    AR = parafoil['Span'] / parafoil['Chord']                   # aspect ratio of span to chord
    if AR != 2:
        print("Aspect Ratio is not 2, delta value needs to be altered in code from paper")
        return 0
    if 1 < AR and AR < 2.5:
        k1 = 3.33 - AR * 1.33
    elif AR >= 2.5:
        k1 = 0
    else:
        print("That's not a good parafoil")
        return 0
    # Add a small amount of drag due to surface roughness and imperfections to the profile drag
    surf_drag =  0.004
    # Drag due to lines from wing to payload
    line_drag = (parafoil['Cells'] + 1) * parafoil['Line']['Length'] * parafoil['Line']['Thickness'] * math.cos(math.radians(parafoil['Angle of Attack'])) ** 3 / (parafoil['Span'] * parafoil['Chord'])
    # Store drag is the drag from the payload, front drag area of payload / canopy area
    store_drag = 0.016877386 / (parafoil['Span'] * parafoil['Chord'])
    # delta is a nonelliptic loading factor based on aspect ratio
    delta = 0.01
    # Drag induced on the wing due to lift
    induced_drag = cl_alpha ** 2 * math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"]) ** 2 / (math.pi * AR) * (1 + delta) + k1 * math.sin(math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"])) ** 3
    tot_cd = parafoil['Profile CD alpha'] + inlet_drag + line_drag + induced_drag + store_drag
    prof_percent = calcPercentage(parafoil['Profile CD alpha'], tot_cd)
    inlet_percent = calcPercentage(inlet_drag, tot_cd)
    line_percent = calcPercentage(line_drag, tot_cd)
    induced_percent = calcPercentage(induced_drag, tot_cd)
    surf_percent = calcPercentage(surf_drag, tot_cd)
    store_percent = calcPercentage(store_drag, tot_cd)
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Profile Drag', 'Inlet Drag', 'Line Drag', 'Store Drag (From Payload)', 'Induced Drag', 'Roughness Drag'
    sizes = [prof_percent, inlet_percent, line_percent, store_percent, induced_percent, surf_percent]
    explode = (0.1, 0, 0, 0.1, 0, 0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title("Drag Components on Vehicle")
    plt.show()
    return tot_cd

def main():
    # load your prepped json file from parafoil Designer
    with open(input("Enter name of parafoil json file: ")) as f:
        parafoil = json.load(f)
    cl_alpha, cl = clCalc(parafoil)
    cd = cdCalc(parafoil, cl_alpha)
    print("Coefficient of Lift: ", cl, "\n Coefficient of Drag: ", cd)

if __name__ == '__main__':
    main()