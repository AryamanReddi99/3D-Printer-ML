#%% import 
import math
import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#%% data
# some 3-dim points
data = np.empty([20,3])
E_fixed_F =     [16,11,20,29,26,12,10,15,27,22]
Score_fixed_F = [5,4,3.5,0,5.5,6,2,7,2,9]
fixed_F =       [1000]*10

fixed_E = [18.75]*10
Score_fixed_E = [7,7,4,7,7,7,8,4,8,9]
F_fixed_E = [1570,746,500,1570,1570,1570,1009,1800,987,1000]

Score_fixed_E = [7,8,9,10,10,10,8,7,3,2]
F_fixed_E = [700,800,900,1000,1000,1000,1100,1200,1300,1400]

E_fixed_F.extend(fixed_E)
E = E_fixed_F
fixed_F.extend(F_fixed_E)
F = fixed_F
Score_fixed_F.extend(Score_fixed_E)
Z = Score_fixed_F

for i in range(20):
    data[i] = [E[i],F[i],Z[i]]

# regular grid covering the domain of the data
X,Y = np.meshgrid(np.arange(0, 50, 1), np.arange(400, 4000, 10))
XX = X.flatten()
YY = Y.flatten()

order = 2    # 1: linear, 2: quadratic
if order == 1:
    # best-fit linear plane
    A = np.c_[data[:,0], data[:,1], np.ones(data.shape[0])]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])    # coefficients
    
    # evaluate it on grid
    Z = C[0]*X + C[1]*Y + C[2]
    
    # or expressed using matrix/vector product
    #Z = np.dot(np.c_[XX, YY, np.ones(XX.shape)], C).reshape(X.shape)

elif order == 2:
    # best-fit quadratic curve
    A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])
    
    # evaluate it on a grid
    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
ax.scatter(data[:10,0], data[:10,1], data[:10,2], c='r', s=50)    # changing E
ax.scatter(data[10:,0], data[10:,1], data[10:,2], c='orange', s=50)   # changing F
plt.xlabel('E')
plt.ylabel('F')
ax.set_zlabel('Z')
ax.axis('equal')
ax.axis('tight')
ax.view_init(0,90)
plt.show()

#%% print
print(C)


#%% print surface again

def create_data(E,F,Z):
    data = np.empty([len(E),3])
    for i in range(len(E)):
        data[i] = [E[i],F[i],Z[i]]
    return(data)

def plot_surface(E,F,Z,C,new_e,new_f):
    data = create_data(E,F,Z)
    new_z = return_z(C,new_e,new_f)
    print("predicted z:", new_z)
    X,Y = np.meshgrid(np.arange(0, 50, 1), np.arange(400, 4000, 10))
    XX = X.flatten()
    YY = Y.flatten()
    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
    ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
    ax.scatter(new_e,new_f,new_z, c='g',s=300)
    plt.xlabel('X')
    plt.ylabel('Y')
    ax.set_zlabel('Z')
    ax.axis('equal')
    ax.axis('tight')
    #ax.view_init(0,90)
    plt.show()

def create_surface(E,F,Z):
    data = create_data(E,F,Z)
    A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]  # best-fit quadratic
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])        # curve params
    return C
    
def return_z(C,x,y):
    z = x*x*C[4]+y*y*C[5]+x*y*C[3]+x*C[1]+y*C[2]+C[0]    # output of best-fit graph
    return z

def E_learning_rate(i):
    #rate = -2*math.log(i+0.5) + 50
    rate = -10*i+100
    return rate

def optimise_E(C,e,f,delta,i):
    grad = (return_z(C,e+delta,f) - return_z(C,e-delta,f))/(2*delta)
    print(grad)
    new_e = E_learning_rate(i)*grad + e
    return(new_e)
    
def F_learning_rate(i):
    #rate = -10000*math.log(i+200) + 600000
    rate = -40000*i+500000
    return rate

def optimise_F(C,e,f,delta,i):
    grad = (return_z(C,e,f+delta) - return_z(C,e,f-delta))/(2*delta)
    print(grad)
    new_f = F_learning_rate(i)*grad + f
    return(new_f)
    
# %% main

# 3 initial data points
E = [30,30,5,20]
F = [400,4000,2200,1000]
Z = [1.5,0,2.5,3.25]
    
for i in range(6):
    C = create_surface(E,F,Z)
    new_e = optimise_E(C,E[-1],F[-1],0.1,i)
    new_f = optimise_F(C,E[-1],F[-1],1,i)
    plot_surface(E,F,Z,C,new_e,new_f)
    print("New E:", new_e)
    print("New F:", new_f)
    new_z = input("Enter new z")

    E.append(new_e)
    F.append(new_f)
    Z.append(new_z)

print(E,Z,F)

# %%

# 3 initial data points
#E = [30,30,5,20,21.7,5.2]
#F = [400,4000,2200,1000,2171,2308]
#Z = [1.5,0,2.5,2,2,2]

E = [0,40,0,40,15,11,15,10.2,23,21,20,20]
F = [100,100,3000,3000,1321,2452,1324,1361,1374,1271,1071,1200]
Z = [0,0,0,0,6,4,8,5.5,8,8,7,10]

#E = [0,40,0,40,15,11,15,10.2,23,21,20,20]
#F = [100,100,3000,3000,1321,2452,1324,1361,1374,1271,1071,637]
#Z = [0,0,0,0,6,4,8,5.5,8,8,7,9]

C = create_surface(E,F,Z)
new_e = optimise_E(C,E[-1],F[-1],0.1,6)
new_f = optimise_F(C,E[-1],F[-1],1,6)
plot_surface(E,F,Z,C,new_e,new_f)
print("New E:", new_e)
print("New F:", new_f)