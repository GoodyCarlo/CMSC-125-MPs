import random

class resource():
    def __init__(self,resourceNumber) -> None:
        self.resourceNumber = resourceNumber
        #resource has 2 states: idle and active
        self.state = "Idle"
        self.queue = []
        self.activeUser = None
        #Remaining time of the active user
        self.remainingUserTime = 0
        #Remaining time for all the users in the queue
        self.timeEstimate = 0
    
    def enqueue(self,userTime:tuple['user',int]):
        self.queue.append(userTime)
    
    def computeTime(self) -> int:
        runTime = self.remainingUserTime
        if len(self.queue) > 0:
            for x in self.queue:
                runTime += x[1]
        return runTime
    
    def __repr__(self) -> str:
        return f"Resource: {self.resourceNumber}"

class user():
    def __init__(self,userNumber) -> None:
        self.userNumber = userNumber
        #User has 3 states
        #Idle = No resources left
        #Active = Currently using a resource
        #Waiting = Waiting for a resource to be available
        self.state = "Idle"
        
        self.resourceBeingUsed = None
        self.remainingTime = 0
        
        #create resources used and time required per resource
        self.resourcesNeeded:list[tuple[user,int]]

    def assignResources(self, resourcesNeeded) -> None:
        self.resourcesNeeded = resourcesNeeded
        
    def isDone(self) -> bool:
        if self.state == "Idle" and len(self.resourcesNeeded) == 0:
             return True
        return False
                
    def computeTime(self) -> int:
        total = self.resourceBeingUsed.remainingUserTime
        for x in self.resourceBeingUsed.queue:
            if x[0].userNumber < self.userNumber:
                total += x[1]
                
        return total
    
    def __repr__(self) -> str:
        return str(f"{self.userNumber}: {self.resourcesNeeded}")
    
    
        
class handler():
    def __init__(self,max,time) -> None:
        self.userList = []
        self.resourceList = []
        
        #generate the users
        self.totalUsers = random.randint(1,max)
        
        for i in range(self.totalUsers):
            self.userList.append(user(i+1))
        
        #generate the resources
        self.totalResources = random.randint(1,max)
        
        for i in range(self.totalResources):
            self.resourceList.append(resource(i+1))

        #generate the resources that the user will need to use and the time it will use each resource
        i:user
        for i in self.userList:
            resources = []
            for j in random.sample(self.resourceList, k  = random.randint(1,self.totalResources)):
                resources.append((j,random.randint(1,time)))
            i.assignResources(resources)
    
    def isDone(self) -> bool:
        for ele in self.resourceList:
            if ele.state == "Active":
                return False
        for ele in self.userList:
            if not ele.isDone():
                return False
        return True
    
    def iterate(self) -> None:
        ele:user
        for ele in self.userList:
            #if user is idle and if user still has resources it needs to use
            if ele.state == "Idle" and not ele.isDone():
                #flag to tell if the user has queued or not
                queuedFlag = False
                res:tuple[resource,int]
                #iterating over the resource list to find a resource that is not being used
                #if no such item is found then it will queue for the first resource in its list 
                for indx,res in enumerate(ele.resourcesNeeded):
                    if res[0].state == "Idle" and len(res[0].queue) == 0:
                        queuedFlag = True
                        temp = ele.resourcesNeeded.pop(indx)
                        #queues the current user with the time it needs for that resource
                        res[0].enqueue((ele,temp[1]))
                        break
                if queuedFlag == False:
                    temp:tuple[resource,int]
                    temp = ele.resourcesNeeded.pop(0)
                    temp[0].enqueue((ele,temp[1]))
                    ele.state = "Waiting"
                    ele.resourceBeingUsed = temp[0]
            
            if ele.state == "Active":
                ele.remainingTime -= 1
                ele.resourceBeingUsed.remainingUserTime -= 1
            
        resourceIter:resource
        for resourceIter in self.resourceList:
            if resourceIter.state == "Idle":
                if len(resourceIter.queue) != 0:
                    temp = resourceIter.queue.pop(resourceIter.queue.index(min(resourceIter.queue,key = lambda test:test[0].userNumber)))
                    # print(min(resourceIter.queue,key = lambda test:test[0].userNumber))
                    resourceIter.activeUser = temp[0]
                    resourceIter.remainingUserTime = temp[1]
                    resourceIter.state = "Active"
                    resourceIter.activeUser.state = "Active"
                    resourceIter.activeUser.remainingTime = resourceIter.remainingUserTime
                    resourceIter.activeUser.resourceBeingUsed = resourceIter
            
            if resourceIter.state == "Active":
                if resourceIter.remainingUserTime == 0 and len(resourceIter.queue) != 0:
                    #Set the finished user to inactive and set the resource reference to none
                    resourceIter.activeUser.state = "Idle"
                    resourceIter.activeUser.resourceBeingUsed = None
                    
                    temp = resourceIter.queue.pop(resourceIter.queue.index(min(resourceIter.queue,key = lambda test:test[0].userNumber)))
                    resourceIter.activeUser = temp[0]
                    resourceIter.remainingUserTime = temp[1]
                    resourceIter.activeUser.state = "Active"
                    resourceIter.activeUser.remainingTime = resourceIter.remainingUserTime
                    resourceIter.activeUser.resourceBeingUsed = resourceIter
                
                if resourceIter.remainingUserTime == 0:
                    resourceIter.activeUser.state = "Idle"
                    resourceIter.state = "Idle"
                    resourceIter.activeUser.resourceBeingUsed = None
                    resourceIter.activeUser = None
                    
# if __name__ == "__main__":
#     test = 

