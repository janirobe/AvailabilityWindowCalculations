# 
import pandas as pd

## running initial data prep/transform script
exec(open("1.IntakeDateScript.py").read())

df = pd.read_csv("../AvailabilityWindowPrepList/1.OUTPUT_intakeDates.csv", sep=',', header=0)
df.drop(df.columns[0],axis=1, inplace=True)

class Availability:
    def __init__(self, type, date, clinicType, monthType,AlexID):
        self.type = type
        self.date = date
        self.clinicType = clinicType
        self.monthType = monthType
        self.AlexID = AlexID
    
    def to_dict(self):
        return {
            'AlexID': self.AlexID,
            'type': self.type,
            'date': self.date,
            'clinicType': self.clinicType,
            'monthType': self.monthType
            }
        

class Clinic(object):
    def __init__(self,intakeDate,num,clinicType, AlexID):
        self.intakeDate = intakeDate
        self.num = num
        self.clinicType = clinicType
        self.timing = self.changeTiming(clinicType)
        self.availabilityList = self.createAvailabilityList(AlexID)
    
    
    ## establishing window timings, custom ones are added at the end    
    def Open3m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(69, unit='D'),"3m","Opening")
    def Closed3m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(111, unit='D'),"3m","Closing")
    def Open6m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(159, unit='D'),"6m","Opening")
    def Closed6m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(201, unit='D'),"6m","Closing")
    def Open9m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(249, unit='D'),"9m","Opening")
    def Closed9m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(291, unit='D'),"9m","Closing")
    def Open12m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(339, unit='D'),"12m","Opening")
    def Closed12m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(381, unit='D'),"12m","Closing")
    def Open15m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(429, unit='D'),"15m","Opening")
    def Closed15m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(471, unit='D'),"15m","Closing")
    def Open18m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(519, unit='D'),"18m","Opening")
    def Closed18m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(561, unit='D'),"18m","Closing")
    def Open21m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(609, unit='D'),"21m","Opening")
    def Closed21m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(651, unit='D'),"21m","Closing")
    def Open24m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(699, unit='D'),"24m","Opening")
    def Closed24m(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(741, unit='D'),"24m","Closing")
    
    #visionHealthBusSpecific
    def vhbOpen(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(70, unit='D'),"VHB_2m","Opening")
    def vhbClose(self):
        return (pd.to_datetime(self.intakeDate) + pd.Timedelta(98, unit='D'),"VHB_2m","Closing")
    
    def changeTiming(self, clinicType):
        if clinicType == "Homebase" or clinicType == "Rapid Access Addiction Medicine" or clinicType == "Prelude" or clinicType == "Abbeydale" :
            return 3
        elif clinicType == "Vision Health Bus":
            return "VHB"
        else:
            return 6
    
    def createAvailabilityList(self, AlexID):
        functions3m = [self.Open3m, self.Closed3m,self.Open6m, self.Closed6m,self.Open9m, self.Closed9m,self.Open12m, self.Closed12m,self.Open15m, self.Closed15m,self.Open18m, self.Closed18m,self.Open21m, self.Closed21m,self.Open24m, self.Closed24m]
        functions6m = [self.Open6m,self.Closed6m,self.Open12m,self.Closed12m,self.Open18m,self.Closed18m,self.Open24m,self.Closed24m]
        functionsVHB = [self.vhbOpen, self.vhbClose]
        availabilityObjectList = []
        if self.timing == 6:
            for fn in functions6m:
                availabilityObjectList.append(Availability(fn()[2], fn()[0], self.clinicType, fn()[1],AlexID))
                
            return availabilityObjectList
        elif self.timing == 3:
            availabilityObjectList = []
            for fn in functions3m:
                availabilityObjectList.append(Availability(fn()[2], fn()[0], self.clinicType, fn()[1],AlexID))
                
            return availabilityObjectList
        elif self.timing == "VHB":
            availabilityObjectList = []
            for fn in functionsVHB:
                availabilityObjectList.append(Availability(fn()[2], fn()[0], self.clinicType, fn()[1],AlexID))
                
            return availabilityObjectList
      

class Client:
    def __init__(self, id):
        self.id = id
        self.clinicList = []
    
    def addClinic(self, clinic):
        self.clinicList.append(clinic)
        
# In[ ]:
    
clientDict = dict()

counter = 0

#this is iterating through all clients and creating their clinic list
for rowIndex, row in df.iterrows():
    for columnIndex, value in row.items():
        print(columnIndex)
        if columnIndex == "AlexID":
            print(columnIndex)
        
        elif columnIndex == "Contact ID":
            client = Client(value)
            clientDict[client.id] = client
        
        elif pd.isna(value) == False:
            string = str(columnIndex).split(".")
            string[1] = string[1].strip()
            clientDict[client.id].addClinic(Clinic(value,string[2],string[1],client.id))
            print(client.id, client.clinicList)


# In[ ]:
    
totalAvailabilityList = []

for client in clientDict.values():
    for clinic in client.clinicList:
        totalAvailabilityList += clinic.availabilityList
        
#print(clientDict["ROBAST11092004"].clinicList[0].Open3m())
#print(clientDict["ROBAST11092004"].clinicList[0].availabilityList[0].type)
#print(clientDict["ROBAST11092004"].clinicList[0].availabilityList[0].date)
#print(clientDict["ROBAST11092004"].clinicList[0].availabilityList[0].clinicType)
#print(clientDict["ROBAST11092004"].clinicList[0].availabilityList[0].monthType)
#print(len(clientDict["ROBAST11092004"].clinicList[0].availabilityList))

#putting each element in list into a dictionary (deconstructs object to be it's parameters)
df3 = pd.DataFrame.from_records([a.to_dict() for a in totalAvailabilityList])
df3 = df3.rename(columns={'AlexID':'ContactID'})
df3.to_csv('2.OUTPUT_calculated_availability.csv', index=False)


