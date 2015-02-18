__author__ = 'Nowakowski'


import Tkinter
from Tkinter import *
import cmd_line
import util
import tkFileDialog
import cmd_line

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




def gui_run(target):

    root=Tk()
    event_input = ""

    #two panes
    m1 = PanedWindow(root, width=800, height=700)
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
    top = Label(m2, text="OPTIONS")
    m2.add(top)
    # bottom = Label(m2, text="results")
    # m2.add(bottom)

    #top buttons
    runButton = Button(top, text="RUN", fg="red", height=12, width=20, command=lambda: button_pressed(root, database, col))
    runButton.pack(side=BOTTOM)

    html_label = Checkbutton(top, text="Print fancy HTML results page", command=html_status)
    html_label.pack(side=BOTTOM)

    col = Entry(top, text="MongoDB collection OR tweet JSON file path:")
    col.pack(side=BOTTOM)
    Label(top, text="MongoDB collection OR tweet JSON file path:").pack(side=BOTTOM)

    database = Entry(top, text="MongoDB database:")
    database.pack(side=BOTTOM)
    Label(top, text="MongoDB database:").pack(side=BOTTOM)


    # event_label = Checkbutton(top, text="Event Name", justify=LEFT)
    # event_label.pack(side=BOTTOM)

    # json_reload = Checkbutton(top, text="Force Reload JSON", justify=LEFT, command=json_status)
    # json_reload.pack(side=BOTTOM)

    # autograder_running = Checkbutton(top, text="Run Autograder", justify=LEFT, command=autograder_status)
    # autograder_running.pack(side=BOTTOM)

    twitter_handles = Checkbutton(top, text="Search Twitter Handles (takes longer)", justify=LEFT, command=search_handles)
    twitter_handles.pack(side=BOTTOM)

    verbose = Checkbutton(top, text="Verbose Mode", justify=LEFT, command=run_verbose)
    verbose.pack(side=BOTTOM,)

    # head_label = Label(top, text="TEAM 1 GUI", width=40, bd=20)
    # head_label.pack(side=BOTTOM)

    top.mainloop()


def button_pressed(window, database, col):
    # print "RUN"
    cmd_line.args.database = database
    cmd_line.args.collection = col
    window.destroy();
    return


def html_status():
    util.html_display=True
    return


def run_verbose():
    util.verbose=True
    return


def search_handles():
    util.search_twitter_handles = True
    return


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
    gui_run(None);


def startInterface():
    gui_run();
