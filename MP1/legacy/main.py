from random import randint, seed

seed(1212312341234199912143121411233)

MAX = 5

resourceHolder = []
userHolder = []

def generateResources():
#Generates the resources and the time alloted for each resource 
    numberOfResourcesRequired = randint(1, MAX)
    resources = []
    resourcesTemp = []
    while numberOfResourcesRequired != 0:
        resourceGenerated = randint(1,MAX)
        timeNeeded = randint(1,MAX)
        
        if resourceGenerated in resourcesTemp:
            pass
        else:
            resources.append([resourceGenerated,timeNeeded])
            resourcesTemp.append(resourceGenerated)
            numberOfResourcesRequired -= 1
    
    return resources

class Resource:
    def __init__(self,resourceNumber) -> None:
        self.resourceNumber = resourceNumber
        #False status indicates an available resource
        self.status = False
        self.userCurrentlyAssigned = 0
        
    def __str__(self) -> str:
        return str(self.resourceNumber)
        
class User:
    def __init__(self,userNumber) -> None:
        self.userNumber = userNumber
        self.resourcesRequired = generateResources
        self.resourceBeingUsed = 0
        
    def __str__(self) -> str:
        return f"{self.resourceNumberRequired} {self.resourceTimeRequired}"
        
if __name__ == "__main__":
    resourceTotal = randint(1,MAX)
    userTotal = randint(1,MAX)
    
    for x in range(resourceTotal):
        resourceHolder.append(Resource(x+1))
        
    for x in range(userTotal):
        userHolder.append(User(x+1))
        
