# Graphical User Interfaces
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np


def save(event):
    print("save")

def exit(event):
    root.quit()


last_x = 0
last_y = 0
first_x = 0
first_y = 0

class MainGUI: # building main Window

    def __init__(self, master):
        self.master = master
        master.title("AnnoPro")


        # leftButtonPanel Layout
        self.leftPanelFrame = Frame(master, width=300, height=1000)
        self.leftPanelFrame.config(borderwidth=3, relief=GROOVE)
        self.leftPanelFrame.pack_propagate(0)
        self.leftPanelFrame.pack(side=LEFT, padx=10, pady=20)

        self.openImageButton = Button(self.leftPanelFrame, text="Open Image for annotation", command=self.openImage)
        self.openImageButton.pack(fill=X)

        self.drawButton = Button(self.leftPanelFrame, text="Draw", command=self.draw)
        self.drawButton.pack(fill=X)

        # PictureFrame
        self.imageFrame = Frame(master)
        self.imageFrame.config(borderwidth=3, relief=GROOVE)
        self.imageFrame.pack(side=LEFT, fill=BOTH, expand=1, padx=10, pady=20)

        # canvas where actually image is displayed
        self.canvas = Canvas(self.imageFrame)
        self.canvas.pack(fill=BOTH, expand=1)
        self.img = PhotoImage(file="C:/MinnoProto/welcome.gif")
        self.canvas.update()  # needed for getting dimension information
        self.image_on_canvas = self.canvas.create_image((self.imageFrame.winfo_width() - 300) / 2, self.imageFrame.winfo_height() / 2, anchor=CENTER, image=self.img)
        print(self.imageFrame.winfo_width())
        # rightButtonPanel Layout
        self.rightPanelFrame = Frame(master, width=300, height=1040)
        self.rightPanelFrame.config(borderwidth=3, relief=GROOVE)
        self.rightPanelFrame.pack_propagate(0)
        self.rightPanelFrame.pack(side=TOP, anchor=NE, padx=10, pady=20)

        self.saveButton = Button(self.rightPanelFrame, text="Save", command=save)
        self.saveButton.pack(fill=X, side=BOTTOM, pady=20)

        self.canvas.bind("<Button-1>", self.mark)

        self.canvas.bind("<Button-2>", self.closeMark)

    def openImage(self):
        #opens file open dialog
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        global newImg   #glopbal that other function can use it too

        #opens image to canvas
        im = Image.open(filename)
        newImg = self.canvas.image=ImageTk.PhotoImage(im)
        self.canvas.itemconfig(self.image_on_canvas, image=newImg)

    #not in use
    def draw(self):
        self.canvas.create_line(500,500,550,550,fill="red",width=5)
        print("draw function")
        numpyArray = np.random.random((6, 2))
        #for i in range (np.size(numpyArray,0))


    #Erases and draws again whole markingarray content
    def updateMarkingArrayToCanvas(self,markingArray):
        global newImg
        #refresh the canvas with original image
        self.canvas.itemconfig(self.image_on_canvas, image=newImg)

        #draws lines between markingArray points
        if (np.size(markingArray,0) == 2):
            self.canvas.create_line(markingArray[0,0],markingArray[0,1],markingArray[1,0],markingArray[1,1],fill="red",width=5)

        if (np.size(markingArray,0)>2):
            for i in range (2,(np.size(markingArray,0))):
                self.canvas.create_line(markingArray[i-1, 0], markingArray[i-1, 1], markingArray[i, 0],
                                        markingArray[i, 1],fill="red",width=5 )


    #ads new point to markingArray, after that calls to
    # updateMarkingArrayToCanvas-function to refresh the canvas
    def mark(self,event):
        global last_x

        if last_x == 0:
            print("first click")
            global markingArray
            markingArray = np.array(([event.x,event.y]))
            print(markingArray)
            """tempArray=np.array(([event.x,event.y]))
            print(tempArray)
            markingArray = np.vstack((markingArray,tempArray))
            print(markingArray)
            last_x = event.x
            last_y = event.y
            """
            last_x=event.x

        else:
            print("new Click")
            tempArray = np.array(([event.x, event.y]))
            print(tempArray)
            markingArray = np.vstack((markingArray, tempArray))
            print(markingArray)
            self.updateMarkingArrayToCanvas(markingArray)

    #closes the markingArray by copying markingArrays first coordinates to the last and
    #calls updateMarkingArrayToCanvas to draw the line to the first point
    def closeMark(self,event):
        global markingArray
        print("Closing mark")
        if (np.size(markingArray, 0) == 0):
            print("Start marking with left button")
        if (np.size(markingArray, 0) > 1):
            tempArray = np.array([(markingArray[0,0]),(markingArray[0,1])])

            print(tempArray)
            markingArray = np.vstack((markingArray, tempArray))
            self.updateMarkingArrayToCanvas(markingArray)







root = Tk()
#root.title("AnnoPro")
root.configure(width=1920, height=1000)
#root.resizable(width=False, height=False)  # disaple window resize
root.pack_propagate(0)  # disaple window size following widgets amount
root.bind('<Escape>', exit)
my_gui = MainGUI(root)
root.mainloop()





