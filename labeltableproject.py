from tkinter import *
import tkinter.messagebox
import shelve
from pathlib import Path


#
recsList = []

# insert number of recordings current system allows
recs = 16

# when instatiated, this class opens a proprietary shelve file for saving.
class Db():

    def __init__(self, dbName):
        self.dbName = dbName

    def setList(self, key, value):
        with shelve.open(self.dbName) as db:
            db[key] = value

    def getList(self, key):
        try:
            with shelve.open(self.dbName) as db:
                existing = db[key]
                return(existing)
        except:
            tkinter.messagebox.showinfo("So Freaking Sorry", "This freaking layout doesn't exist")
            pass

    def delList(self, key):
        with shelve.open(self.dbName) as db:
            del db[key]


# This class is the main Window of the program.
class MainWindow():

    # recs = 16

    def __init__(self, master):
        # This init method creates the recording label window based on the number stored in global recs

        frame = Frame(master)

        frame.pack()
        global recsList

        self.loadBut = Button(frame, text="Load", command=self.loadData).grid(row=0, column=4, sticky=NE)
        self.saveAs = Button(frame, text="Save", command=self.saveData).grid(row=1, column=4, sticky=E)

        self.showList = ['Show One', 'Show Two', 'Show Three']
        self.blockMenuList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Part One', 'Part Two']
        self.varMenuValues = ['1', '2', '3', '4']

        self.variationMenu = Db('variationDb')
        self.vDbFile = Path('variationDb.db')

        if self.vDbFile.is_file() == False:
            self.variationMenu.setList('variation', self.varMenuValues)
        else:
            self.varMenuValues = self.variationMenu.getList('variation')

        self.mainDb = Db('mainLayoutDb')

        self.showTitle = StringVar()
        self.showTitle.set("Show")
        self.show = OptionMenu(frame, self.showTitle, *self.showList)
        self.show.grid(row=1, column=0, sticky=W)

        self.blockTitle = StringVar()
        self.blockTitle.set("Block/Half")
        self.block = OptionMenu(frame, self.blockTitle, *self.blockMenuList)
        self.block.grid(row=1, column=1, sticky=W)

        self.titleStrVar = StringVar()
        self.titleStrVar.set('Variation')
        self.variationTitle = StringVar()
        self.variationTitle.set(self.titleStrVar.get())
        self.variation = OptionMenu(frame, self.variationTitle, *self.varMenuValues)
        self.variation.grid(row=1, column=2, sticky=W)

        primaryGui = recs + 2

        self.strVar = [None]*primaryGui
        self.checkVar = [None]*primaryGui
        self.labels = [None]*primaryGui
        self.guiText = [None]*primaryGui
        self.guiCheck = [None]*primaryGui
        self.primaryGuiList = [None]*primaryGui

        i = 0
        while i <= primaryGui:
            self.checkVar.insert(i, IntVar())
            self.strVar.insert(i, StringVar())
            i += 1

        self.bottomRowVar = 0

        count = 0

        labelRow = 2
        labelColumn = 0

        while count < primaryGui:
            if count >= recs:
                self.labels[count] = Label(frame, text="Variation")
                self.labels[count].grid(row=0, column=3)
                self.guiText[count] = Entry(frame, textvariable=self.strVar[count])
                self.guiText[count].grid(row=1, column=3, sticky=W)
            # if count == primaryGui:
            #     self.bottomRowVar = textRow + 1
            else:
                checkRow = labelRow
                checkColumn = labelColumn
                textRow = labelRow + 2
                textColumn = labelColumn
                self.labels[count] = Label(frame, text="Recording " + str((count) + 1))
                self.labels[count].grid(row=labelRow, column=labelColumn, sticky=W)
                self.guiCheck[count] = Checkbutton(frame, variable=self.checkVar[count])
                self.guiCheck[count].grid(row=checkRow, column=checkColumn, sticky=NE)
                self.guiText[count] = Entry(frame, textvariable=self.strVar[count])
                self.guiText[count].grid(row=textRow, column=textColumn)
                self.bottomRowVar = textRow + 1
            labelColumn += 1
            if labelColumn >= 4:
                labelRow += 3
                labelColumn = 0
            count += 1

        self.sendBut = Button(frame, text="Send", command=self.sendData).grid(row=self.bottomRowVar, column=4, sticky=SE)
        self.delBut = Button(frame, text="Delete Layout", command=self.deleteLayout).grid(row=self.bottomRowVar, column=0, sticky=SW)
        self.variationDict = {}
        self.blockMenuStatus = 0


    def menuAppend(self, value):
        list = self.variationMenu.getList('variation', )
        list.append(value)
        self.variationMenu.setList('variation', list)
        self.variationTitle.set('Variation')

    def keyMaster(self):
        show = self.showTitle.get()
        block = self.blockTitle.get()
        variation = self.variationTitle.get()
        key = show + block + variation
        return(key)

    def layoutToDb(self):
        key = self.keyMaster()
        self.mainDb.setList(key, self.primaryGuiList[0:-2])
        voo = self.mainDb.getList(key)

    def dbToLayout(self):
        key = self.keyMaster()
        yo = self.mainDb.getList(key)
        counter = 0
        list = self.mainDb.getList(key)
        tempList = []
        while counter < recs:
            tempList.insert(counter, list[counter])
            counter += 1
        tempList.append([0, ''])
        tempList.append([0, ''])
        self.primaryGuiList = tempList



    def clearBoxes(self):
        counter = 0
        while counter < len(self.primaryGuiList):
            self.checkVar[counter].set(0)
            self.strVar[counter].set('')
            counter += 1
        self.showTitle.set('Show')
        self.blockTitle.set('Block/Half')
        self.variationTitle.set('Variation')

    def deleteLayout(self):
        key = self.keyMaster()
        self.mainDb.delList(key)
        self.clearBoxes()
        tkinter.messagebox.showinfo("Delete Layout", "Layout has been Deleted")

    def deliveryDisplay(self):
        counter = 0
        localList = recsList
        try:
            while counter < len(self.primaryGuiList):
                check = self.checkVar[counter].get()
                word = self.strVar[counter].get()
                if check == 0:
                   pass
                else:
                    tkinter.messagebox.showinfo("Rec " + str(counter + 1),
                                                "Label sent to Rec " + str(counter + 1) + ":\n" + '"' + word +'"')
                counter += 1
        except:
            tkinter.messagebox.showinfo('So Sorry!',  'The Send Was Not Successful!')
        self.clearBoxes()

    def sendData(self):
         self.deliveryDisplay()

    def loadData(self):
        list = []
        counter = 0
        #This spot is for db or hash table retrieval
        if self.primaryGuiList == None:
            self.saveData()
        else:
            self.localGlobalInt('fromGlobal')
            try:
                self.dbToLayout()
            except:
                pass
            self.localGlobalInt('toGlobal')
        while counter <= recs:
            self.checkVar[counter].set(self.primaryGuiList[counter][0])
            self.strVar[counter].set(self.primaryGuiList[counter][1])
            counter = counter + 1
        self.localGlobalInt('toGlobal')

    def saveData(self):
        counter = 0
        list = []
        size = len(self.primaryGuiList)
        while counter < size:
            list.append([self.checkVar[counter].get(), self.strVar[counter].get()])
            counter += 1
        self.primaryGuiList = list
        self.localGlobalInt('toGlobal')
        voo = self.primaryGuiList
        if self.primaryGuiList[-1][1] != '':
            self.variationTitle.set(self.primaryGuiList[-1][1])
            self.menuAppend(recsList[-1][1])
            self.layoutToDb()
        else:
            self.layoutToDb()

    def localGlobalInt(self, direction):
        global recsList
        if direction == 'toGlobal':
            recsList = self.primaryGuiList
        elif direction == 'fromGlobal':
            self.primaryGuiList = recsList
        else:
            print('nope, did not make it through the localGlobalInt method')



root = tkinter.Tk()
root.title('Label Table')

window = MainWindow(root)
root.mainloop()

