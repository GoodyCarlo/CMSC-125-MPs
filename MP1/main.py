import customtkinter
import random
import logic

SEED = 123451234
MAX = 5
TIME = 5

class variableFrame(customtkinter.CTkFrame):
    def __init__(self, master, variable, **kwargs):
        super().__init__(master, **kwargs)
        #store an instance of the variable
        self.variable = variable
        
        #add widgets onto the frame
        self.variableNumber = customtkinter.CTkLabel(self)
        self.variableNumber.grid(row=0, column = 0, padx = 20, sticky = "nsew")
        
        self.variableBeingUsed = customtkinter.CTkLabel(self)
        self.variableBeingUsed.grid(row=0, column = 1, padx = 20)
        
        self.timeEstimate = customtkinter.CTkLabel(self)
        self.timeEstimate.grid(row=0, column = 2, padx = 20)
        
        self.variableState = customtkinter.CTkLabel(self)
        self.variableState.grid(row=0, column = 3, padx = 20)
        
        self.queue = customtkinter.CTkLabel(self)
        self.queue.grid(row=1, column = 0, padx = 20, columnspan = 4, sticky = "w")
        
        self.runTimeEstimate = customtkinter.CTkLabel(self)
        self.runTimeEstimate.grid(row=1, column = 3)

class sidebarFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame
        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)
        
    def updateLabel(self,label:str):
        self.label.configure(text = label)

class app(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #for future handling of variables
        self.handler = None
        self.resourceFrames = []
        self.userFrames = []    
        #window confguration
        self.title("Ypanto MP1 GUI")
        self.geometry("1920x1080")
        
        #grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        #sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
        #label
        self.sidebarlabel = customtkinter.CTkLabel(self.sidebar_frame, text="Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sidebarlabel.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        #set seed of random number generator
        self.seedtextbox = sidebarFrame(self.sidebar_frame, width=200, height= 30, corner_radius=0)
        self.seedtextbox.updateLabel(SEED)
        self.seedtextbox.grid(row=1, column=0, padx=20, pady=10)
        self.seedtextbox.grid_propagate(False)
        # self.seedtextbox.insert("0.0",str(SEED))
        self.seedbutton = customtkinter.CTkButton(self.sidebar_frame, command=self.seed_button_event, text="Set Seed")
        self.seedbutton.grid(row=2, column=0, padx=20, pady=10)
        
        #set max amount of resources and users
        self.maxtextbox = sidebarFrame(self.sidebar_frame, width=200, height= 30, corner_radius=0)
        self.maxtextbox.updateLabel(MAX)
        self.maxtextbox.grid(row=3, column=0, padx=20, pady=10)
        self.maxtextbox.grid_propagate(False)
        self.maxbutton = customtkinter.CTkButton(self.sidebar_frame, command=self.max_button_event, text="Set max")
        self.maxbutton.grid(row=4, column=0, padx=20, pady=10)
        
        #set max amount of time
        self.timetextbox = sidebarFrame(self.sidebar_frame, width=200, height= 30, corner_radius=0)
        self.timetextbox.updateLabel(TIME)
        self.timetextbox.grid(row=5, column=0, padx=20, pady=10)
        self.timetextbox.grid_propagate(False)
        self.timebutton = customtkinter.CTkButton(self.sidebar_frame, command=self.time_button_event, text="Set time")
        self.timebutton.grid(row=6, column=0, padx=20, pady=10)
        
        self.startbutton = customtkinter.CTkButton(self.sidebar_frame, command=self.startLoop, text="Start")
        self.startbutton.grid(row=7, column=0, padx=20, pady=10)
        
        #dashboard area
        self.dashboard_frame = customtkinter.CTkFrame(self, corner_radius=0, height= 100)
        self.dashboard_frame.grid(row=0, column=1, columnspan = 2, sticky = "nsew")
        self.dashboard_frame.grid_propagate(False)
        self.titlelabel = customtkinter.CTkLabel(self.dashboard_frame, text="Ypanto MP1", font=customtkinter.CTkFont(size=40, weight="bold"))
        self.titlelabel.grid(row=0, column=0, padx=500, sticky = "ns")
        self.timelabel = customtkinter.CTkLabel(self.dashboard_frame, text="Time Elapsed: 0", font=customtkinter.CTkFont(size=20))
        self.timelabel.grid(row=1, column=0, padx=300)
        
        #resource area
        self.resource_frame = customtkinter.CTkScrollableFrame(self, width=100, corner_radius=0, fg_color="#8f8f8f")
        self.resource_frame.grid(row=1, column=1, sticky = "nsew")
        self.resourcelabel = customtkinter.CTkLabel(self.resource_frame, text="Resources", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.resourcelabel.grid(row=0, column=0, padx=260)
        
        
        #user area
        self.user_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="#8f8f8f")
        self.user_frame.grid(row=1, column=2, sticky = "nsew")
        self.userlabel = customtkinter.CTkLabel(self.user_frame, text="Users", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.userlabel.grid(row=0, column=0, padx=300)
        
    def seed_button_event(self):
        global SEED
        while True:
            seeddialog = customtkinter.CTkInputDialog(text="Type in a number for the seed:", title="Set seed dialog")
            seed = seeddialog.get_input()
            if seed.isnumeric():
                SEED = int(seed)
                break
        self.seedtextbox.updateLabel(seed)
        
    def max_button_event(self):
        global MAX
        while True:
            maxdialog = customtkinter.CTkInputDialog(text="Type in a number for the max: (max amount is 30)", title="Set max dialog")
            max = maxdialog.get_input()
            if not max.isnumeric():
                max = MAX
                break
            
            if int(max) <= 30:
                break
        MAX = int(max)
        self.maxtextbox.updateLabel(MAX)
        
    def time_button_event(self):
        global TIME
        while True:
            timedialog = customtkinter.CTkInputDialog(text="Type in a number for the time: (max amount is 30)", title="Set time dialog")
            time = timedialog.get_input()
            if not time.isnumeric():
                time = TIME
                break
            
            if int(time) <= 30:
                break
        TIME = int(time)
        self.timetextbox.updateLabel(time)

    def createResourceText(self,resource:logic.resource) -> variableFrame:
        temp = variableFrame(self.resource_frame, resource, width=500, height= 60, corner_radius=0)
        temp.variableNumber.configure(text = f"R{resource.resourceNumber}")
        temp.timeEstimate.configure(text = "Time Remaining: 0")
        temp.variableBeingUsed.configure(text = "User using resource: None")
        temp.queue.configure(text = f"Queue: None")
        temp.grid(row = resource.resourceNumber+1,column = 0)
        temp.grid_propagate(False)
        temp.variableState.configure(text = f"State: {resource.state}")
        temp.runTimeEstimate.configure(text = "ETC: 0")
        
        return temp
    
    def createUserText(self,user:logic.user) -> variableFrame:
        temp = variableFrame(self.user_frame, user, width=500, height= 60, corner_radius=0)
        temp.variableNumber.configure(text = f"U{user.userNumber}")
        temp.timeEstimate.configure(text = "Time Estimate: 0")
        temp.variableBeingUsed.configure(text = "Resource being used: None")
        tempQueueVar = ""
        x:tuple[logic.resource,int]
        
        for x in user.resourcesNeeded:
            tempQueueVar += f"R{x[0].resourceNumber} [{x[1]}s], "
            
        tempQueueVar = tempQueueVar[0:-2]
        
        temp.queue.configure(text = f"Resource List: {tempQueueVar}")
        temp.grid(row = user.userNumber+1,column = 0)
        temp.grid_propagate(False)
        temp.variableState.configure(text = f"State: {user.state}")
        temp.runTimeEstimate.configure(text = "ETA: 0")
        return temp

    def clearContent(self):
        for x in self.userFrames:
                x.destroy()
        for x in self.resourceFrames:
            x.destroy()
            
        self.seedbutton.configure(state= "enabled", fg_color= self.origColor)
        self.maxbutton.configure(state= "enabled", fg_color= self.origColor)
        self.timebutton.configure(state= "enabled", fg_color= self.origColor)
        self.startbutton.configure(state= "enabled", fg_color= self.origColor)
    
    def updateText(self):
        ele:variableFrame
        
        for ele in self.resourceFrames:
            tempResourceText = ""
            if len(ele.variable.queue) == 0:
                tempResourceText += "None"
            else:
                for x in ele.variable.queue:
                    tempResourceText += f" U{x[0].userNumber} [{x[1]}s],"
                tempResourceText = tempResourceText[:-1]
            ele.queue.configure(text = f"Queue:{tempResourceText}")
            
            if ele.variable.activeUser == None:
                ele.variableBeingUsed.configure(text = f"User using resource: None")
            else:
                if ele.variable.state == "Active":
                    ele.variableBeingUsed.configure(text = f"User using resource: U{ele.variable.activeUser.userNumber}")
            ele.timeEstimate.configure(text = f"Time Remaining: {str(ele.variable.remainingUserTime)}")
            ele.variableState.configure(text = f"State: {ele.variable.state}")
            ele.runTimeEstimate.configure(text = f"ETC: {str(ele.variable.computeTime())}")
                
        for ele in self.userFrames:
            tempUserText = ""
            # print(ele.variable.resourcesNeeded)   
            if len(ele.variable.resourcesNeeded) == 0:
                tempUserText += "None"
            else:
                for x in ele.variable.resourcesNeeded:
                    tempUserText += f" R{x[0].resourceNumber} [{x[1]}s],"
                tempUserText = tempUserText[:-1]
            ele.queue.configure(text = f"Resource List:{tempUserText}")
            if ele.variable.state == "Active":
                ele.variableBeingUsed.configure(text = f"Resource being used: R{ele.variable.resourceBeingUsed.resourceNumber}")
            else:
                ele.variableBeingUsed.configure(text = f"Resource being used: None")
            ele.timeEstimate.configure(text = f"Time Remaining: {ele.variable.remainingTime}")
            ele.variableState.configure(text = f"State: {ele.variable.state}")
            
            if ele.variable.state == "Waiting":
                ele.runTimeEstimate.configure(text = f"ETA: {str(ele.variable.computeTime())}")
                ele.variableBeingUsed.configure(text = f"Waiting on resource: R{ele.variable.resourceBeingUsed.resourceNumber}")
            else:
                ele.runTimeEstimate.configure(text = f"ETA: 0")
    def update(self):
        self.handler.iterate()
        self.updateText()
        self.timeElapsed += 1
        self.timelabel.configure(text = f"Time Elapsed: {self.timeElapsed}")
        if self.handler.isDone():
            self.after(1000,self.clearContent)
            return 
        else:  
            self.after(1000,self.update)
    
    def startLoop(self):
        # print(MAX)
        print(self.resourceFrames)
        self.resourceFrames = []
        print(self.resourceFrames)
        self.userFrames = []
        self.timeElapsed = 0
        self.origColor = self.seedbutton.cget("fg_color")
        self.seedbutton.configure(state= "disabled", fg_color= "GRAY")
        self.maxbutton.configure(state= "disabled", fg_color= "GRAY")
        self.timebutton.configure(state= "disabled", fg_color= "GRAY")
        self.startbutton.configure(state= "disabled", fg_color= "GRAY")
        
        
        random.seed(SEED)
        self.handler = logic.handler(MAX,TIME)

        
        for x in self.handler.resourceList:
            self.resourceFrames.append(self.createResourceText(x))

        for x in self.handler.userList:
            self.userFrames.append(self.createUserText(x))
            
        self.after(1000,self.update)
        
if __name__ == "__main__":
    app = app()
    app.mainloop()