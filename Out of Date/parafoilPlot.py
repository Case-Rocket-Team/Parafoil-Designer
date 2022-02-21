# !!! Standalone airfoil data plotter for demo purposes !!!
import pandas as pd
import matplotlib.pyplot as plt
parafoil_data = pd.read_csv("naca4418_orig.csv")

plt.plot(parafoil_data['alpha'], parafoil_data['CL'])
plt.xlabel("Angle of Attack (deg)")
plt.ylabel("Coefficient of Lift")
plt.title("CL vs Angle of Attack")

plt.figure()
plt.plot(parafoil_data['alpha'], parafoil_data['CD'])
plt.xlabel("Angle of Attack (deg)")
plt.ylabel("Coefficient of Drag")
plt.title("CD vs Angle of Attack")

ld = parafoil_data['CL'] / parafoil_data['CD']
print("Max L/D is: ", max(ld))
max_index = ld.idxmax()
print("Highest L/D occurs at: ", parafoil_data['alpha'][max_index])

plt.figure()
plt.plot(parafoil_data['alpha'], ld)
plt.xlabel("Angle of Attack (deg)")
plt.ylabel("L/D")
plt.title("L/D vs Angle of Attack")
plt.show()