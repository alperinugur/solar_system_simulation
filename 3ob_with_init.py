import tkinter as tk
import winsound
import json

import time

WIDTH = 1900  # Window Width
HEIGHT = 1000  # Window Height

G = 6.6743e-7 # Gravitational constant
DT = 50000
MOVDIVIDER = 1500

def bleep():
  freq=2000
  dur=3
  winsound.Beep(freq,dur)



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


class CelBody:
    def __init__(self, canvas, x, y, radius, mass, dx,dy,color,name="astreoid"):
        #self.canvas = canvas
        #self.id = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.dx = dx
        self.dy = dy
        self.color = color
        self.destroyed= 0
        self.alive = True
        self.name = name

    def to_dict(self):
        return {
        'x': self.x,
        'y': self.y,
        'radius': self.radius,
        'mass': self.mass,
        'dx': self.dx,
        'dy': self.dy,
        'color': self.color,
        'name': self.name
        }

    @classmethod
    def from_dict(cls, canvas, data):
        return cls(canvas, **data)


ox, oy,lastx,lasty = 0,0,0,0
mx,my,lastmx,lastmy = 0,0,0,0


def save_celestial_bodies(cel_bodies, filename):
    data = [body.to_dict() for body in cel_bodies]
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_celestial_bodies(canvas, filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return [CelBody.from_dict(canvas, body_data) for body_data in data]


def addobject(mx,my,lastmx,lastmy,ox, oy,lastx,lasty):
    print(mx,my,lastmx,lastmy,ox, oy,lastx,lasty)
    sz = ((mx-lastmx)**2 + (my-lastmy)**2)**0.5/4
    xmov = (lastx-ox)/MOVDIVIDER
    ymov = (lasty-oy)/MOVDIVIDER
    objects.append(CelBody(canvas,ox,oy ,sz**0.5, sz*10, xmov,ymov,"#ff0000"))
    pass


def mousemotionGetMass(event):
    global mx,my,lastmx,lastmy,ox, oy,lastx,lasty
    if mx == 0 and my == 0:
        mx, my = event.x, event.y
        lastmx,lastmy = mx,my
    else:
        canvas.delete("temp")
        sz = ((mx-lastmx)**2 + (my-lastmy)**2)**0.5/4
        canvas.create_oval(ox-sz, oy-sz, ox+sz, oy+sz, fill="#ff0000",tags="temp")
        canvas.update()
        lastmx, lastmy = event.x, event.y  # Update starting point for next line

def bReleaseGetMass(event):
    global mx,my,lastmx,lastmy,ox, oy,lastx,lasty
    sz = ((mx-lastmx)**2 + (my-lastmy)**2)**0.5/4
    canvas.create_oval(ox-sz, oy-sz, ox+sz, oy+sz, fill="#ff0000")
    addobject (mx,my,lastmx,lastmy,ox, oy,lastx,lasty )
    mx,my,lastmx,lastmy,ox, oy,lastx,lasty = 0,0,0,0,0,0,0,0
    canvas.bind("<B1-Motion>", mousemotion)
    canvas.bind("<ButtonRelease>", bRelease)

def getMass():
    global ox, oy,lastx,lasty
    canvas.bind("<B1-Motion>", mousemotionGetMass)
    canvas.bind("<ButtonRelease>", bReleaseGetMass)

def mousemotion(event):
    global ox, oy,lastx,lasty
    if ox == 0 and oy == 0:
        ox, oy = event.x, event.y
        canvas.create_oval(ox - 2, oy - 2, ox + 2, oy + 2, fill="#ff0000")
    else:
        canvas.delete("temp")
        canvas.create_line(ox, oy, event.x, event.y, fill="#00ff00",tags="temp")
        canvas.update()
        lastx, lasty = event.x, event.y  # Update starting point for next line

def bRelease(event):
    global ox, oy,lastx,lasty
    canvas.create_line(ox, oy, lastx,lasty, fill="#00ff00")
    getMass()
    # ox, oy,lastx,lasty = 0, 0,0,0

quitProg = False
objAddingFinished = False

def on_key_press(event):
    global quitProg, objAddingFinished
    char = event.char
    keycode = event.keycode
    if keycode == 27:  # Esc key
        quitProg = True
    if keycode == 13:  # ENTER KEY
        objAddingFinished = True
    if keycode == 8:    # Backspace KEY
        objects_loaded = load_celestial_bodies(canvas,"last_used.json")
        for obj in objects_loaded:
            objects.append(obj)
        objAddingFinished = True
        pass
    print(keycode)

def CreateObjects():
    global quitProg
    root.bind('<KeyPress>', on_key_press)
    canvas.bind("<B1-Motion>", mousemotion)
    canvas.bind("<ButtonRelease>", bRelease)
    while objAddingFinished == False:
        root.update()


def calculatemovement(theobj):
    if theobj.alive==True:
        ax,ay=0,0
        for obj2 in celestials:
            if theobj != obj2:
                dx = theobj.x - obj2.x  # horizontal distance
                dy = theobj.y - obj2.y  # vertical distance
                distance = (dx**2 + dy**2)**0.5  
                if distance > 10:
                    force = G  * obj2.mass / distance**2
                    ax += force * (dx / distance)
                    ay += force * (dy / distance)
                else:
                    bleep()
        theobj.dx -= ax * DT
        theobj.dy -= ay * DT 

start_time=None
def addtimer():
    global start_time
    if start_time is None:
        start_time = int(round(time.time() * 1000)) 
    new_time=int(round(time.time() * 1000)) 
    time_passed = (new_time-start_time)/1000
    canvas.delete("timer")
    canvas.create_text(30,30,text=str(time_passed), fill="white", font=("Arial", 10),tags="timer")


def centerall(celestials):
    xtt,ytt,obn=0,0,0
    for obj in celestials:
        xtt = xtt+obj.x
        ytt = ytt+obj.y
        obn+=1
    cenx,ceny = xtt/obn,ytt/obn

    cendx = WIDTH/2-cenx
    cendy = HEIGHT/2-ceny
    for obj in celestials:
        obj.x = obj.x+cendx
        obj.y = obj.y+cendy
        obj.canvas.move(obj.id,cendx,cendy)
    addtimer()
    root.update()
    
def updatepositions(celestials):
    for obj in celestials:
        # canvas.create_line(obj.x,obj.y,obj.x+1,obj.y+1,fill=obj.color)
        movementx, movementy = obj.dx , obj.dy
        obj.x += movementx
        obj.y += movementy
        obj.canvas.move(obj.id, movementx, movementy)
    centerall (celestials)

def update_board():
    for obj in celestials:
        calculatemovement(obj)
    updatepositions(celestials=celestials)
    #canvas.update()
    root.after(1,update_board)


if __name__ == '__main__':
    # Create main window
    root = tk.Tk()
    root.title("CPU xtra")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()

    totalscreenw = root.winfo_screenwidth()
    totalscreenh = root.winfo_screenheight()
    xx = totalscreenw / 2 - WIDTH / 2
    yy = (totalscreenh - 80) / 2 - HEIGHT / 2  # Adjusted for spacing

    # Set the window size
    root.geometry(f"{int(WIDTH)}x{int(HEIGHT)}+{int(xx)}+{int(yy)}")
    root.update()

    objects = []
    celestials =[]

    CreateObjects()
    canvas.destroy()
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()

    colorsets = ("#ff0000","#00ff00","#0000ff","#ffff00","#ff00ff","#00ffff")

    tt1= 0
    save_celestial_bodies(objects,"last_used.json")
    for obj in objects:
        celestials.append(CelestialBody(canvas,obj.x,obj.y ,obj.radius, obj.mass, obj.dx,obj.dy,colorsets[tt1]))
        tt1+=1
        if tt1 > 6: tt1=0

    tt1=0
    for obj in objects:
        mymass = "%.2f" % obj.mass
        canvas.create_text(30,60+30*tt1,text=mymass, fill=colorsets[tt1], font=("Arial", 12),tags=tt1)
        tt1 +=1

    update_board()
    root.mainloop()

