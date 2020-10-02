import math
class CoefficientCalc:
    def clCalc(self, parafoil):
        epsilon = parafoil['Span'] / (4 * parafoil['Line']['Length'])
        ar = self.calcAR(parafoil)                  
        if ar != 2:
            print("Aspect Ratio is not 2, tau value needs to be altered in code from paper")
            return 0
        if 1 < ar and ar < 2.5:
            k1 = 3.33 - ar * 1.33
        elif ar >= 2.5:
            k1 = 0
        else:
            print("That's not a good parafoil")
            return 0
        cl_alpha = self.calcCLalpha(parafoil)
        return cl_alpha * math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"]) * math.cos(math.radians(epsilon)) ** 2 + k1 * math.sin(math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"])) ** 2 * math.cos(math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"]))
    # Calculates CL alpha value used in CL and CD calculation
    
    def calcCLalpha(self, parafoil):
        # tau is a corrective term for elliptic loading
        tau = 0.07
        ar = self.calcAR(parafoil)
        cl_slope = parafoil['Profile CL alpha'] / math.radians(parafoil['Angle of Max L/D'] - parafoil["Angle of Zero Lift"])
        k = (2 * math.pi *  ar) / cl_slope * math.tanh(cl_slope / (2 * math.pi *  ar))
        cl_slope_prime = cl_slope * k
        cl_alpha = math.pi * ar * cl_slope_prime / (math.pi * ar + cl_slope_prime * (1 + tau))
        return cl_alpha
    
    # Calculates aspect ratio of span to chord
    def calcAR(self, parafoil):
        return parafoil['Span'] / parafoil['Chord']
    
    def cdCalc(self, parafoil):
        # Drag due to 
        inlet_drag = 0.5 * parafoil['Inlet Height'] / parafoil['Chord']
        ar = self.calcAR(parafoil)                   # aspect ratio of span to chord
        if ar != 2:
            print("Aspect Ratio is not 2, delta value needs to be altered in code from paper")
            return 0
        if 1 < ar and ar < 2.5:
            k1 = 3.33 - ar * 1.33
        elif ar >= 2.5:
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
        cl_alpha = self.calcCLalpha(parafoil)
        # Drag induced on the wing due to lift
        induced_drag = cl_alpha ** 2 * math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"]) ** 2 / (math.pi *   ar) * (1 + delta) + k1 * math.sin(math.radians(parafoil['Angle of Attack'] - parafoil["Angle of Zero Lift"])) ** 3
        tot_cd = parafoil['Profile CD alpha'] + inlet_drag + line_drag + induced_drag + store_drag
        return tot_cd