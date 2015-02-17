__author__ = 'DoctorWatson'




import Tkinter
from Tkinter import *
import goldenglobes

# import HTML
# import html2


#
# class resultsList(Tkinter.Tk):
#     def __init__(self, parent):
#         Tkinter.Tk.__init__(self,parent)
#         self.parent = parent
#         self.initialize()
#
#     def initialize(self):
#         listResults = Listbox()
#         listResults.insert(listResults.size() + 1, "lulz")
#
#     def addText(self, add):
#         self.listResults.insert(self.listResults.size()+1,add)

# def progressBarGUI:




class nlpGUI(Tkinter.Tk):

    test = Listbox()

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        resultList = Listbox()

    def initialize(self):
        self.grid()

        #two panes
        m1 = PanedWindow(width=800, height=700)
        m1.pack(fill=BOTH, expand=1)
        m2 = PanedWindow(m1, orient=VERTICAL)
        m1.add(m2)

        # m1L = PanedWindow(m1, orient=VERTICAL)
        # m1.add(m1L)
        #
        #
        # m1R = PanedWindow(m1, orient=VERTICAL)
        # m1.add(m1R)

        #two panes text
        top = Label(m2, text="options")
        m2.add(top)
        bottom = Label(m2, text="results")
        m2.add(bottom)

        #top buttons
        runButton = Button(top, text="RUN", fg="red", height=12, width=20, command=goldenglobes.main)
        runButton.pack(side=BOTTOM)

        worst_dressed = Checkbutton(top, text="Worst Dressed ", onvalue=1, offvalue=0, justify=LEFT)
        worst_dressed.pack(side=BOTTOM)

        best_dressed = Checkbutton(top, text="Best Dressed ", onvalue=1, offvalue=0, justify=LEFT)
        best_dressed.pack(side=BOTTOM)

        winners = Checkbutton(top, text="Winners ", onvalue=1, offvalue=0, justify=LEFT)
        winners.pack(side=BOTTOM)

        nominees = Checkbutton(top, text="Nominees ", onvalue=1, offvalue=0, justify=LEFT)
        nominees.pack(side=BOTTOM)








        # jsonEntry = Entry(top, text="Event:")
        # jsonEntry.pack(side=BOTTOM)
        #
        # jsonLabel = Label(top, text="Load JSON:")
        # jsonLabel.pack(side=BOTTOM)
        #
        # eventEntry = Entry(top, text="Event:")
        # eventEntry.pack(side=BOTTOM)
        #
        # eventLabel = Label(top, text="Event:")
        # eventLabel.pack(side=BOTTOM)
        #
        #
        # collectionEntry = Entry(top)
        # collectionEntry.pack(side=BOTTOM)
        #
        # eventLabel = Label(top, text="Set Pymongo Collection")
        # eventLabel.pack(side=BOTTOM)
        #
        # databaseEntry = Entry(top)
        # databaseEntry.pack(side=BOTTOM)
        #
        # eventLabel = Label(top, text="Set Database Path")
        # eventLabel.pack(side=BOTTOM)
        #
        #
        # twitterHandles = Checkbutton(top, text="Show Twitter Handles", justify=LEFT)
        # twitterHandles.pack(side=BOTTOM)
        #
        # forceReload = Checkbutton(top, text="Force JSON Reload", justify=LEFT)
        # forceReload.pack(side=BOTTOM,)
        #
        # verbose = Checkbutton(top, text="Verbose Mode", justify=LEFT)
        # verbose.pack(side=BOTTOM,)
        #
        # jsonLabel = Label(top, text="COMMAND LINE OPTIONS", width=40, bd=20)
        # jsonLabel.pack(side=BOTTOM)

        jsonLabel = Label(top, text="TEAM 1 GUI", width=40, bd=20)
        jsonLabel.pack(side=BOTTOM)

        m2.add(self.test)
        self.test.insert(1,"yeee")
        self.test.pack()


    def addText(self, addedText):
        self.test.insert(self.test.size()+1, addedText)
        return


#
# def GUImain():
#
#
#     m1 = PanedWindow(width=800, height=700)
#     m1.pack(fill=BOTH, expand=1)
#
#     m2 = PanedWindow(m1, orient=VERTICAL)
#     m1.add(m2)
#
#     top = Label(m2, text="options")
#     m2.add(top)
#
#     bottom = Label(m2, text="results")
#     m2.add(bottom)
#
#     runButton = Button(top, text="RUN", fg="red", command=addText("lulz"))
#     runButton.pack(side=BOTTOM)
#
#
#     listResults.insert(listResults.size() + 1, "lulz")
#
#     mainloop()

# top = Tk()
# testFrame = Frame(top, width=500, height=400)
# testFrame.pack()




#
# def makeGUI():
#     top = Tk()
#     testFrame = Frame(top, width=500, height=400)
#     testFrame.pack()
#
#
#     welcome = Text(top)
#     welcome.insert(INSERT, "'sup")
#     welcome.pack()
#
#     redbutton = Button(testFrame, text="Red", fg="red")
#     redbutton.pack(side=BOTTOM)
#
#     bluebutton = Button(testFrame, text="blue", fg="blue")
#     bluebutton.pack(side=BOTTOM)
#
#     top.mainloop()

#
# def htmlAdd(text):
#     newText=


if __name__ == "__main__":
    app = nlpGUI(None)
    app.title('Team 1 Golden Globes')
    app.mainloop()


def startInterface():
    app = nlpGUI(None)
    app.title('Team 1 Golden Globes')
    app.mainloop()