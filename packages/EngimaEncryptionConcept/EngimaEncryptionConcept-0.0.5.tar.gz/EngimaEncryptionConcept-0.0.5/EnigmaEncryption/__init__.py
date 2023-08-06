import random
class EnigmaAssembly:
    def __init__(self,c1ports=[],c2ports=[],c3ports=[],autogenerate=False,cylinderRotation=False):
        if autogenerate:
            self.cylinder1 = Cylinder(autogenerate=True)
            self.cylinder2 = Cylinder(autogenerate=True)
            self.cylinder3 = Cylinder(autogenerate=True)
        else:
            if len(c1ports)!=26 or len(c2ports)!=26 or len(c3ports)!=26:
                raise(Exception("Not enough ports!"))
            else:
                self.cylinder1 = Cylinder(c1ports)
                self.cylinder2 = Cylinder(c2ports)
                self.cylinder3 = Cylinder(c3ports)
        self.cylinderRotation = cylinderRotation
        self.alphabet = Alphabet()
    def getRotations(self):
        return {'Rotor1':self.cylinder1.getRotation(),'Rotor2':self.cylinder2.getRotation(),'Rotor3':self.cylinder3.getRotation()}
    def getKeys(self):
        return {'Rotor1':self.cylinder1.generated,'Rotor2':self.cylinder2.generated,'Rotor3':self.cylinder3.generated}
    def cylinderRotationCheck(self):
        if self.cylinder1.rotations == 26:
            self.cylinder1.rotations = 0
            self.cylinder2.turnCylinder()
        if self.cylinder2.rotations == 26:
            self.cylinder2.rotations = 0
            self.cylinder3.turnCylinder()
        if self.cylinder3.rotations == 26:
            self.cylinder3.rotations=0
    def Encrypt(self, inputmessage):
        if not isinstance(inputmessage, str):
            raise(Exception("Input is not a string"))
        words = inputmessage.split()
        encrypted = ""
        # print(f"{self.cylinder1.ports}\n{self.cylinder2.ports}\n|{self.cylinder3.ports}")
        for word in words:
            for i in word:
                if i not in self.alphabet.alphabetUpper and i not in self.alphabet.alphabetLower:
                    encrypted = encrypted + i
                    continue
                # print(f"{self.cylinder1.ports}\n{self.cylinder2.ports}\n|{self.cylinder3.ports}")
                if i in self.alphabet.alphabetLower:
                    position = self.alphabet.alphabetLower.index(i)
                    # print(f"Position: {position}")
                    firslayerposition = self.cylinder1.ports[position]
                    # print(f"firslayerposition: {firslayerposition}")
                    secondlayerposition = self.cylinder2.ports[firslayerposition]
                    # print(f"secondlayerposition: {secondlayerposition}")
                    thirdlayerposition = self.cylinder3.ports[secondlayerposition]
                    # print(f"thirdlayerposition {thirdlayerposition}")
                    encryptedletter = self.alphabet.alphabetLower[thirdlayerposition]
                elif i in self.alphabet.alphabetUpper:
                    position = self.alphabet.alphabetUpper.index(i)
                    # print(f"Position: {position}")
                    firslayerposition = self.cylinder1.ports[position]
                    # print(f"firslayerposition: {firslayerposition}")
                    secondlayerposition = self.cylinder2.ports[firslayerposition]
                    # print(f"secondlayerposition: {secondlayerposition}")
                    thirdlayerposition = self.cylinder3.ports[secondlayerposition]
                    # print(f"thirdlayerposition {thirdlayerposition}")
                    encryptedletter = self.alphabet.alphabetUpper[thirdlayerposition]
                else:
                    continue #Keep the symbols, change to make it work later
                encrypted = encrypted + encryptedletter
                self.cylinder1.turnCylinder()
                if self.cylinderRotation:
                    print(f"F1 {self.cylinder1.rotations} | F2 {self.cylinder2.rotations} | F3 {self.cylinder3.rotations}")
                self.cylinderRotationCheck()
            encrypted = encrypted + " "
        return encrypted
    def Decrypt(self, inputmessage, code1,code2,code3,rotation1,rotation2,rotation3):
        if not isinstance(inputmessage, str):
            raise(Exception("Input is not a string"))
        self.cylinder1.ports = self.cylinder1.putInDict(code1)
        self.cylinder2.ports = self.cylinder2.putInDict(code2)
        self.cylinder3.ports = self.cylinder3.putInDict(code3)
        self.cylinder1.setRotation(rotation1)
        self.cylinder2.setRotation(rotation2)
        self.cylinder3.setRotation(rotation3)
        # print(f"{self.cylinder1.ports}\n{self.cylinder2.ports}\n|{self.cylinder3.ports}")
        words = inputmessage.split()
        decrypted = ""
        for word in words:
            for i in word:
                if i not in self.alphabet.alphabetUpper and i not in self.alphabet.alphabetLower:
                    decrypted = decrypted + i
                    continue
                # print(f"{self.cylinder1.ports}\n{self.cylinder2.ports}\n|{self.cylinder3.ports}")
                if i in self.alphabet.alphabetLower:
                    position = self.alphabet.alphabetLower.index(i)
                    # print(f"Position: {position}")
                    thirdlayerposition = self.findFromValue(position,self.cylinder3.ports)
                    # print(f"thirdlayerposition {thirdlayerposition}")
                    secondlayerposition = self.findFromValue(thirdlayerposition,self.cylinder2.ports)
                    # print(f"secondlayerposition: {secondlayerposition}")
                    firslayerposition = self.findFromValue(secondlayerposition,self.cylinder1.ports)
                    # print(f"firslayerposition: {firslayerposition}")
                    decryptedletter = self.alphabet.alphabetLower[firslayerposition]
                elif i in self.alphabet.alphabetUpper:
                    position = self.alphabet.alphabetUpper.index(i)
                    # print(f"Position: {position}")
                    thirdlayerposition = self.findFromValue(position,self.cylinder3.ports)
                    # print(f"thirdlayerposition {thirdlayerposition}")
                    secondlayerposition = self.findFromValue(thirdlayerposition,self.cylinder2.ports)
                    # print(f"secondlayerposition: {secondlayerposition}")
                    firslayerposition = self.findFromValue(secondlayerposition,self.cylinder1.ports)
                    # print(f"firslayerposition: {firslayerposition}")
                    decryptedletter = self.alphabet.alphabetUpper[firslayerposition]
                else:
                    continue #Keep the symbols, change to make it work later
                decrypted = decrypted + decryptedletter
                self.cylinder1.turnCylinder()
                if self.cylinderRotation:
                    print(f"F1 {self.cylinder1.rotations} | F2 {self.cylinder2.rotations} | F3 {self.cylinder3.rotations}")
                self.cylinderRotationCheck()
            decrypted = decrypted + " "
        return decrypted
    def findFromValue(self,value,dictionary):
        for x in dictionary:
            if dictionary[x]==value:
                # print(x)
                return x

class Alphabet: #ASCII for losers jk
    def __init__(self):
        self.alphabetLower = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        self.alphabetUpper = []
        for x in self.alphabetLower:
            self.alphabetUpper.append(x.upper())
class Cylinder:
    def __init__(self,outputport=[],autogenerate=False,rotationPosition=0):
        if autogenerate:
            self.generated = self.AutoGenerateCylinder()
            self.ports = self.putInDict(self.generated)
            self.setRotation(random.choice(range(0,26)))
        else:
            if len(outputport)!=26:
                raise(Exception("Not enought outputports"))
            else:
                self.ports = {}
                for i in range(0,26):
                    self.ports[i]=outputport[i]
            self.setRotation(rotationPosition)

            # print(self.ports)
    def getRotation(self):
        return self.rotations
    def setRotation(self,rotationPosition):
        if rotationPosition!=0:
            self.rotations=0
            while self.rotations!=rotationPosition:
                self.turnCylinder()
        else:
            self.rotations=0;
    def AutoGenerateCylinder(self):
        x=[]
        y=[]
        for i in range(0,26):
            x.append(i)

        while len(x)!=0:
            z = random.choice(x)
            y.append(z)
            x.remove(z)

        return y
    def turnCylinder(self):
        portslist = []
        for i in range(0,26):
            portslist.append(self.ports[i]) #get ports from dict
        for i in range(0,26):
            if i == 25:
                self.ports[i]=portslist[0]
            else:
                self.ports[i]=portslist[i+1] #put data in dict and turn it
        self.rotations += 1
        # print(self.ports)

    def putInDict(self,ports):
        tempdict = {}
        for i in range(0,26):
            tempdict[i]=ports[i]
        return tempdict
    def putInList(self, dictionary):
        ports = []
        for i in range(0,26):
            ports.append(dictionary[i])
        return ports
