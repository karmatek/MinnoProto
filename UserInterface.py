# Graphical User Interfaces
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter.scrolledtext as tkst
from PIL import ImageTk, Image
import numpy as np
from VisualRecognitionTiles import *
from AreaFinder import *
import xml.etree.ElementTree as ET
import os.path


def save(event):
    print("save")

def exit(event):
    root.quit()


last_x = 0
last_y = 0
first_x = 0
first_y = 0
drawMode = False

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

        self.analyzeWithWatsonButton = Button(self.leftPanelFrame, text="Analyze with Watson", command = self.visualRecognitionTiles_analyze)
        self.analyzeWithWatsonButton.pack(fill=X)

        self.smartSelectButton = Button(self.leftPanelFrame, text = "Smart select tool", command = self.smartSelect )
        self.smartSelectButton.pack(fill=X)

        self.drawButton = Button(self.leftPanelFrame, text="Draw", command=self.draw)
        self.drawButton.pack(fill=X)

        # PictureFrame
        self.imageFrame = Frame(master)
        self.imageFrame.config(borderwidth=3, relief=GROOVE)
        self.imageFrame.pack(side=LEFT, fill=BOTH, expand=1, padx=10, pady=20)

        # canvas where actually image is displayed
        self.canvas = Canvas(self.imageFrame)
        self.canvas.pack(fill=BOTH, expand=1)
        #self.img = PhotoImage(file="C:/MinnoProto/welcome.gif")
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "welcome.gif")
        self.img = PhotoImage(file=path)

        self.canvas.update()  # needed for getting dimension information
        self.image_on_canvas = self.canvas.create_image((self.imageFrame.winfo_width() - 300) / 2, self.imageFrame.winfo_height() / 2, anchor=CENTER, image=self.img)
        print(self.imageFrame.winfo_width())
        # rightButtonPanel Layout
        self.rightPanelFrame = Frame(master, width=300, height=1040)
        self.rightPanelFrame.config(borderwidth=3, relief=GROOVE)
        self.rightPanelFrame.pack_propagate(0)
        self.rightPanelFrame.pack(side=TOP, anchor=NE, padx=10, pady=20)


        #label
        quickAnnotationBoxLabel=Label(self.rightPanelFrame,text="Quick Annotation")
        quickAnnotationBoxLabel.pack()

        'quickAnnotationstextbox'
        self.quickAnnotations = tkst.ScrolledText(
            master=self.rightPanelFrame,
            wrap='word',  # wrap text at full words only

            width=60,  # characters
            height=10,  # text lines
            bg='beige'  # background color of edit area
        )
        self.quickAnnotations.pack(fill=X)
        self.quickAnnotations.bind("<Button-3>",MainGUI.rightClickOnQuickComment)

        #label
        freeTextLabel = Label(self.rightPanelFrame,text="Freetext")
        freeTextLabel.pack()


        'textbox'
        self.freeTxt = tkst.ScrolledText(
            master=self.rightPanelFrame,
            wrap='word',  # wrap text at full words only

            width=60,  # characters
            height=10,  # text lines
            bg='beige'  # background color of edit area
        )
        self.freeTxt.pack(fill=X)


        self.saveButton = Button(self.rightPanelFrame, text="Save", command=save)
        self.saveButton.pack(fill=X, side=BOTTOM, pady=20)

        self.canvas.bind("<Button-1>", self.mark)

        self.canvas.bind("<Button-2>", self.closeMark)

    def openImage(self):
        #opens file open dialog
        global filename
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        global newImg   #glopbal that other function can use it too
        global im
        #opens image to canvas
        im = Image.open(filename)
        newImg = self.canvas.image=ImageTk.PhotoImage(im)
        self.canvas.itemconfig(self.image_on_canvas, image=newImg)

    #enables marking mode
    def draw(self):
        global drawMode
        drawMode=True
        print("draw function")



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
        if drawMode:
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
        if drawMode:
            global markingArray
            print("Closing mark")
            if (np.size(markingArray, 0) == 0):
                print("Start marking with left button")
            if (np.size(markingArray, 0) > 1):
                tempArray = np.array([(markingArray[0,0]),(markingArray[0,1])])
                print(tempArray)
                markingArray = np.vstack((markingArray, tempArray))
                self.updateMarkingArrayToCanvas(markingArray)

    #crop image to tiles and run it through watson and return tile repsentation from picture
    def visualRecognitionTiles_analyze(self):
        analyzeImageMask = analyzeImage(im)
        tempImage=im
        blend = Image.blend(tempImage, analyzeImageMask, 0.3)
        temp=self.canvas.image = ImageTk.PhotoImage(blend)
        self.canvas.itemconfig(self.image_on_canvas, image=temp)

    #automatic selection
    def smartSelect(self):
        cv2_im = smartSelectFunc(filename)
        ####cv2 uses BGR color scheme and pil uses RGB here we conver them
        destRGB = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(destRGB)
        temp = self.canvas.image = ImageTk.PhotoImage(pil_im)
        self.canvas.itemconfig(self.image_on_canvas, image=temp)




    #quickAnnotation
    def rightClickOnQuickComment(event):
        #tree = ET.parse('C:/Users/veeti/Desktop/inno/xml/annotationOptions.xml')
        # EtRoot = tree.getroot()
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "annotationOptions.xml")

        tree = ET.parse(path)
        EtRoot = tree.getroot()
        print("Right")
        master = Tk()

        listbox = Listbox(master)

        listbox.pack()

        # listbox.insert(END, "a list entry")

        for child in EtRoot:
            listbox.insert(END, child.attrib['category'])
        listbox.bind('<<ListboxSelect>>', MainGUI.onselect)



    def onselect(evt,):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        my_gui.quickAnnotations.insert('insert', value + '\n')

        print('You selected item %d: "%s"' % (index, value))


root = Tk()
#root.title("AnnoPro")
#root.configure(width=1920, height=1000)
root.geometry("{0}x{1}+0+0".format(
            root.winfo_screenwidth(), root.winfo_screenheight()))
#root.resizable(width=False, height=False)  # disaple window resize
root.pack_propagate(0)  # disaple window size following widgets amount
root.bind('<Escape>', exit)
my_gui = MainGUI(root)
root.mainloop()





