import math

class VoidedShaftMock:

    def __init__(self):
        self.D = 20.0
        self.Di = 12.0
        self.a = 9.0
        self.c = self.a/0.75
        


    # Methods for outer gross area 
    def theta_0(self):
        "Angle of outer circle chord"
        D = self.D 
        a = self.a
        return math.acos((D/2.0 - a)/(D/2.0))
        
        
    def Ac_0(self):
        "Area in compression, gross"
        D = self.D 
        a = self.a
        theta = self.theta_0() 
        return D**2*((theta - math.sin(theta)*math.cos(theta))/4.0)
       

    def ybar_0(self):
        "Location of centroid of gross area in compression"
        D = self.D 
        theta = self.theta_0()
        Acybar = D**3*((math.sin(theta)**3)/12.0) 
        return Acybar/self.Ac_0()
        

        
    # Methods for inner hollow circle - deducted from gross to form net
    def theta_i(self):
        "Angle of outer circle chord"
        D = self.D
        Di = self.Di
        ai = max(self.a - (D/2.0 - Di/2.0), 0.0) # arccos(1) = 0
        return math.acos((Di/2.0 - ai)/(Di/2.0))
        
        
    def Ac_i(self):
        "Area in compression, gross"
        Di = self.Di 
        theta_i = self.theta_i()
        return Di**2*((theta_i - math.sin(theta_i)*math.cos(theta_i))/4.0)
       

    def ybar_i(self):
        "Location of centroid of gross area in compression"
        Di = self.Di
        theta_i = self.theta_i()
        Acybar_i = Di**3*((math.sin(theta_i)**3)/12.0) 
        return Acybar_i/self.Ac_i()   
        
        
    def Ac(self):
        return self.Ac_0() - self.Ac_i()
        
    def ybar(self):
        Ac0 = self.Ac_0()
        Aci = self.Ac_i()
        y0 = self.ybar_0()
        yi = self.ybar_i()
        return (Ac0*y0 - Aci*yi)/(Ac0 - Aci)

if __name__ == "__main__":
    shaft = VoidedShaftMock()
    print(shaft.theta_0())
    print(shaft.Ac_0())
    print(shaft.ybar_0())

    print("======================")
    print(shaft.theta_i())
    print(shaft.Ac_i())
    print(shaft.ybar_i())
    
    print("======================")
    print(shaft.Ac())
    print(shaft.ybar())
    