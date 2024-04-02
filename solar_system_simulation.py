import tkinter as tk
import random
import math
import threading
import time
import winsound

WIDTH = 1905    # Window Width
HEIGHT = 1000   # Window Height
EARTHDIS = 60
EARTHRADIUS = 4
PlanetRadiusRatio = 2    # Make this 1 to see the real ratio of planet sizes
numberofAstreoids = 150  
astreoidRandomMove = 0.05 # make it between 0 - 0.1 for good results

#IMPORTANT CONSTANTS - Don't change below unless you know what you are doing
EARTHMASS = 20  
SPEEDF = 6
G = 6.6743e-7 # Gravitational constant
DT = 8


class CelestialBody:
  def __init__(self, canvas, x, y, radius, mass, adx,ady,color,name="astreoid"):
    self.canvas = canvas
    self.id = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)
    self.x = x
    self.y = y
    self.radius = radius
    self.mass = mass
    self.dx = adx
    self.dy = ady
    self.color = color
    self.destroyed= 0
    self.alive = True
    self.name = name

def bleep():
  freq=1000
  dur=30
  winsound.Beep(freq,dur)

def DestroyAstreoid(Killer,killed):
    canvas.delete (killed.id)
    Killer.destroyed +=1
    canvas.delete(Killer.name)
    canvas.create_text(100, 50+Killer.id*20, text=Killer.name + " - Number Killed: " + str(Killer.destroyed), fill=Killer.color, font=("Arial", 10),tags=Killer.name)
    killed.alive = False
    bleep()


def calculatemovement(theobj):
    if theobj.alive==True:
        ax,ay=0,0
        for obj2 in objects:
            if theobj != obj2 and obj2.mass>5 :
                dx = theobj.x - obj2.x  # horizontal distance
                dy = theobj.y - obj2.y  # vertical distance
                distance = (dx**2 + dy**2)**0.5  
                if distance <6 and theobj.mass<=2:
                    DestroyAstreoid(obj2,theobj)
                elif distance > 10:
                    force = G  * obj2.mass / distance**2
                    ax += force * (dx / distance)
                    ay += force * (dy / distance)
        theobj.dx -= ax * DT
        theobj.dy -= ay * DT 


def updatepositions(objects):
    for obj in objects:
        # canvas.create_line(obj.x,obj.y,obj.x+1,obj.y+1,fill=obj.color)
        movementx, movementy = obj.dx , obj.dy
        obj.x += movementx
        obj.y += movementy
        obj.canvas.move(obj.id, movementx, movementy)
        if obj.name=="Earth" or obj.name=="Jupiter":
            pass
            #canvas.create_line(obj.x,obj.y,obj.x+1,obj.y+1,fill=obj.color)


class MovementThread(threading.Thread):
  def __init__(self, obj):
    super().__init__()
    self.obj = obj

  def run(self):
    calculatemovement(self.obj)

def printFPS(tm):
    canvas.delete("thetext")
    canvas.create_text(WIDTH-100, 50, text=f"FPS  {tm:.2f} ", fill="white", font=("Arial", 10),tags="thetext")

def makeplanet(distance,size,mass,color,name="astreoid"):
    angle = random.random()*6.28
    posx = WIDTH/2+(math.sin(angle))*distance
    posy = HEIGHT/2+(math.cos(angle))*distance
    if distance>1:
        catchspeed =  SPEEDF / (distance**0.5)
    else:
       catchspeed= 0
    randomness=astreoidRandomMove if name == "astreoid" else 0
    xmov= catchspeed*math.cos(angle)+random.random()*randomness*2-randomness
    ymov= -catchspeed*math.sin(angle)+random.random()*randomness*2-randomness
    if name=="Mercury":
        xmov = catchspeed*math.cos(angle)*1.04
        ymov= -catchspeed*math.sin(angle)*1.04
    objects.append(CelestialBody(canvas,posx,posy ,size, mass, xmov,ymov,color,name))

def CreateSolarSystem():
    makeplanet (0,7,EARTHMASS*330000,"red", "The SUN") #SUN
    makeplanet(0.4*EARTHDIS,EARTHRADIUS * (0.38**(1/PlanetRadiusRatio)),EARTHMASS*0.33,"#ababab","Mercury")  # Mercury
    makeplanet(0.725*EARTHDIS,EARTHRADIUS * (0.95**(1/PlanetRadiusRatio)),EARTHMASS*0.95,"#907010","Venus")  # Venus
    makeplanet(EARTHDIS,EARTHRADIUS,EARTHMASS,"blue", "Earth") # Earth
    makeplanet(1.52*EARTHDIS,EARTHRADIUS * (0.53**(1/PlanetRadiusRatio)),EARTHMASS*.4,"yellow","Mars")  # Mars
    makeplanet(5.2*EARTHDIS,EARTHRADIUS * (7**(1/PlanetRadiusRatio)),EARTHMASS*318,"#605020","Jupiter") # Jupiter
    makeplanet(9.54*EARTHDIS,EARTHRADIUS * (6**(1/PlanetRadiusRatio)),EARTHMASS*14.54,"#aaaa00","Saturn") # Saturn
    makeplanet(19.19*EARTHDIS,EARTHRADIUS * (2.54**(1/PlanetRadiusRatio)),EARTHMASS*95,"#ccccff","Uranus") # Uranus
    makeplanet(30*EARTHDIS,EARTHRADIUS * (2.46**(1/PlanetRadiusRatio)),EARTHMASS*17,"#2020ff","Neptune") # Neptune


def CreateAstroids(numberofasts,distance,randomness,color):
    for i in range (1,numberofasts):
        makeplanet(distance+random.randint(1,randomness),2,1,color)


def update():
    start_time = time.time()  
    for obj in objects:
        calculatemovement(obj)
    updatepositions(objects=objects)
    end_time = time.time()  
    diff = end_time-start_time
    if diff !=0:         
        printFPS(0.033/diff)
    #canvas.update()
    root.after(1,update)



if __name__ == '__main__':
    # Create main window
    root = tk.Tk()
    root.title("CPU xtra")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()
    totalscreenw = root.winfo_screenwidth()
    totalscreenh = root.winfo_screenheight()
    xx= totalscreenw/2 - WIDTH/2
    yy = (totalscreenh-80)/2 - HEIGHT/2
    # Set the window size
    root.geometry(f"{WIDTH}x{HEIGHT}+{int(xx)}+{int(yy)}")  # Adjusted for spacing

    objects =[]
    CreateSolarSystem()
    CreateAstroids(numberofAstreoids,EARTHDIS*10,200,"grey")


    update()
    root.mainloop()




'''
    def updateMulti():
    threads = []
    # Create threads for each object
    for obj in objects:
        thread = MovementThread(obj)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Update positions after all calculations are done
    updatepositions(objects=objects)
    #canvas.delete("thetext")
    canvas.create_text(WIDTH/2, 150, text="Last Eater ", fill="white", font=("Arial", 10),tags="thetext")

    root.after(1, updateMulti)
'''