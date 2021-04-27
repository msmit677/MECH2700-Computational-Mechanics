"""
Author: Matthew Smith
Date: 28/08/2019
Title: MECH2700 Trajectory Assignment
"""

from math import sin,cos,pi,radians,atan,sqrt,degrees
import pylab

#Define all global parameters that have been given
m = 0.7 # kg
rho = 1.2 # kg/m^3
d = 0.15 # m
g = 9.81 # m/s^2
Cd = 0
theta_0 = radians(45) # angles must be in radians
delta_t = 0.000001 # s
V_0 = 30 # m/s
A_front = pi*(d/2)**2 # m^2

print("Zero Drag Numerical Solution:")
#Define the drag force
def FDrag(V):
    return 1/2*rho*V**2*A_front*Cd

#Define positions in the x and y directions which depends on the drag force
def xPos(V,Vx,x,theta):
    Fx = FDrag(V)*cos(theta)
    Ax = -Fx/m
    x += Vx*delta_t + 1/2*Ax*(delta_t)**2
    Vx += Ax*delta_t
    return Ax,Vx,x

def yPos(V,Vy,y,theta):
    Fy = FDrag(V)*sin(theta)
    Ay = -g-Fy/m
    y += Vy*delta_t + 1/2*Ay*(delta_t)**2
    Vy += Ay*delta_t
    return Ay,Vy,y

#Create empty lists that store the values of x and y at each time-step 
xs = []
ys = []
#Construct a function which computes the trajectory of the bread roll
def Trajectory():
    #Define the initial launch conditions
    t = 0
    Vx = V_0*cos(theta_0)
    Vy = V_0*sin(theta_0)
    x = 0            
    y = 1.8          
    xs.append(x)
    ys.append(y)
    while y > 0: #The function will run until the bread roll hits the ground
        t += delta_t
        theta = atan(Vy/Vx)
        V = sqrt(Vx**2+Vy**2)
        Ax,Vx,x = xPos(V,Vx,x,theta)
        Ay,Vy,y = yPos(V,Vy,y,theta)
        xs.append(x) #Adds the computed x value to the xs list
        ys.append(y) #Adds the computed y value to the ys list
    print("Time-Step = {0:0.6f}s, Flight Time = {1:0.6f}s, Range = {2:0.6f}m"
          .format(delta_t,t,x))
    return t,x

Trajectory() #Run the Trajectory function

print("Analytic Solution:")
#Define a function which computes the range and time of flight analytically
def Analytic():
    y_0 = 1.8
    Vx = V_0*cos(theta_0)
    Vy = V_0*sin(theta_0)
    t = (-Vy-sqrt(((Vy)**2)-(4*-g/2*y_0)))/-g
    x = Vx*t
    print("Flight Time = {0:0.6f}s, Range = {1:0.6f}m".format(t,x))

Analytic() #Run the Analytic function

print("Find an Accurate Time-Step for Non-zero Drag:")
#Calculate an accurate time-step for non-zero drag
Cd = 0.5
for delta_t in [1/(10**i) for i in range(1,7)]:
    Trajectory()

print("Find the optimum launch conditions:")
#Create a function which checks if roll hits the house using an angle of 45
#Reset the x and y data lists to store new data
xs = []
ys = []
V_0 = 40.08 #Change the velocity manually until a result is achieved
theta_0 = radians(42.70) #Change angle manually until optimised
print("Optimal Angle = {0:0.2f} degrees".format(degrees(theta_0)))
print("Optimal Velocity =",V_0,"m/s")

def OptimumVelocity():
    #Define initial launch conditions
    t = 0
    Vx = V_0*cos(theta_0)
    Vy = V_0*sin(theta_0)
    x = 0
    y = 1.8  
    xs.append(x)
    ys.append(y)
    while y > 0: #The function will run until the bread roll hits the ground
        t += delta_t
        theta = atan(Vy/Vx)
        V = sqrt(Vx**2+Vy**2)
        Ax,Vx,x = xPos(V,Vx,x,theta)
        Ay,Vy,y = yPos(V,Vy,y,theta)
        if 75 <= x <= 84 and y <= 9:
            print("The bread roll hits the house at x = {0:0.6f}".format(x))
            break  #Stops the while loop if the bread roll hits the house
        else:
            xs.append(x) #Adds the computed x value to the xs list
            ys.append(y) #Adds the computed y value to the ys list

#Plot the trajectory for the optimum conditions
OptimumVelocity()
pylab.plot(xs,ys, label="Trajectory")
pylab.plot([74,74,84,84],[0,9,9,0],"-", label="House")
pylab.xlim(0,max(xs)+2)
pylab.ylim(0,max(ys)+2)
pylab.xlabel("x(m)")
pylab.ylabel("y(m)")
pylab.title("Trajectory of the Bread Roll (Optimum Conditions)")
pylab.legend()
pylab.show()
    
