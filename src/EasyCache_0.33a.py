#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright chezlenox (2013) - chezlenox@gmail.com
Contributor(s) : DQ (2011 - 2013)

Version : 0.33 branche (a)

It is a pure python module that depends on:
- scipy       : http://www.scipy.org/
- numpy       : http://numpy.scipy.org/
- matplotlib  : http://matplotlib.sourceforge.net/
- pyDicom     : http://code.google.com/p/pydicom/

INSTALL :
---------
Debian / Ubuntu :
	sudo apt-get install python-matplotlib python-dicom

Windows (win32):
	python-2.7.3.msi
	pydicom-0.9.8.win32.exe
	numpy-1.7.0-win32-superpack-python2.7.exe
	matplotlib-1.2.0.win32-py2.7.exe


This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.


Facteur e- = 905/950 env 0.953



"""



import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkMessageBox as Msg
import tkFileDialog
import dicom
import time
import os.path

from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

# ==> Click GUI
def buttonClickSource():
        global Vsource
        f_exploSource()
        labelScrVar.set(Vsource)

def buttonClickCible():
	global Vcible
	Vcible = tkFileDialog.askdirectory()
	labelCblVar.set(Vcible)

def buttonClickProcess():
        f_checkProcess()
        labelScrVar.set(Vsource)
        labelCblVar.set(Vcible)
        print'1 f_checkProcess() DONE'

        f_openDcm()
        print'2 f_openDcm() DONE'

        f_creerEcf()
        print'3 f_creerEcf() DONE'

        f_headerEcf()
        print'4 f_headerEcf() DONE'

        f_coord(0)
        print'5 f_coord(0) DONE'

        ecf_file.close()

        f_graphCache()
        print'6 f_graphCache() DONE'

        print '\n >>>> Vsource = \n', Vsource
        print '\n >>>> Vcible = \n', Vcible
        print '\n >>>> Fichier .ECF =\n' ,ecf_path
        print '\n -- PROCEDURE TERMINE --'

def buttonClickClear():
        global Vcible, Vsource

        Vcible=''
        Vsource=''

        labelCblVar.set('')
        labelScrVar.set('')
        labeltxt1Var.set('')

        f.clf() # matplotlib.pyplot.clf() => Clear the current figure.
        f_creerMatplotGraphe()

# <== Click GUI

def f_exploSource():
	global Vsource, filetypes
	Vsource = os.path.normpath(tkFileDialog.askopenfilename(filetypes = [("RP_dicom (Eclispe)","*.dcm"),("All", "*")]))

def f_exploCible(Vinitialdir):
	global Vcible
	if Vinitialdir == '':
		Vcible = tkFileDialog.askdirectory()
	else:
		Vcible = Vinitialdir

def f_checkProcess():
	global Vinitialdir
	
	if Vsource == '':
		f_exploSource()

	if Vcible == '':
		Vinitialdir = os.path.normpath(r'//ficpc-exp1/pc$/Radiotherapie/echange/_LOGICIELS/EasyCache/')
		print Vinitialdir			
		f_exploCible(Vinitialdir)

def f_checkDcm():
        #Controle si le dcm est bien un RT Plan comprenant un cache
        if not nbrBlocks > 0:
                Msg.showwarning(title="",message="Le fichier Dicom ne possede pas de Block(Cache)")
                f_exploSource()
                f_openDcm()

def f_openDcm():
        global ds, diverg, namepat, dateplan, datepat, headercom,  nbrBlocks, machine, nbrOfbeam, nomsdubeam, planlabel , idpat

        #Source fichier dcm
        ds = dicom.read_file(Vsource)

        #Controle presence de cache
        nbrBlocks = ds[0x300a,0xb0][0][0x300a,0xf0].value
        f_checkDcm()

        #Header pour le fichier .ecf EasyCut
        namepat = ds[0x10,0x10].value
        dateplan = ds[0x300a,0x06].value
        datepat = ds[0x10,0x30].value
        headercom = ds[0x300a,0xb0][0][0x300a,0xc2].value
        nbrOfbeam = ds[0x300a,0x70][0][0x300a,0x80].value
        machine = ds[0x300a,0xb0][0][0x300a,0xb2].value
        nomsdubeam = ds[0x300a,0xb0][0][0x300a,0xc2].value #(300a, 00c2) Beam Name LO: 'CCP G'
        planlabel = ds[0x300a,0xb0][0][0x300a,0xc2].value#(300a, 0002) RT Plan Label                       SH: 'CCP G'
        idpat = ds[0x10,0x20].value        # (0010, 0020) Patient ID                          LO: '00620138'
        
        #Ici dump dans fichier texte du dcm pour visualisation
        dump_file = open(Vsource+"_dump.txt", 'w')
        dump_file.write(str(ds))
        dump_file.close()

        # retour des variables dans GUI
        labeltxt1Var.set(
        "Patient Name : " +str(namepat)+ '\n'
        "Patient ID : " +str(idpat)+ '\n'       
        "Date Naissance : " +str(datepat)+ '\n' + '\n' +
        "Faisceau : " +str(nomsdubeam)+ '\n'
        "Plan : " +str(planlabel)+ '\n'        
        "Machine : " +str(machine)+ '\n')

def f_headerEcf():
        #Mise en forme du fichier .ecf
        global ecf_out

        ecf_header = "[Header]\n"
        ecf_dateplan = "Date=" + str(dateplan)+ '\n'
        ecf_namepat = "PatientName=" + str(namepat)+ tictac + '\n'
        ecf_datepat = "PatientDate=" + str(datepat)+ '\n'
        ecf_beam = """Comment="""+ str(headercom)+"_"+ str(machine) +"_"+ str(idpat) +"_"+ str(namepat) +"_"+ str(planlabel) +"_"+ str(nomsdubeam)+"""
ID=0
NoOfBeams="""+ str(nbrOfbeam) +"""
ProgVersion=0

""" #le triple """ permet le multiligne sans \n

        ecf_out = ecf_header + ecf_dateplan + ecf_namepat + ecf_datepat + ecf_beam
        ecf_file.write(ecf_out)

def f_coord(nivo) :
        global item, Xlist, Ylist

        # Recuperation des coordonnees via Dicom du cache0(UNIQUEMENT):
        ssd = ds[0x300a,0xb0][0][0x300a,0xb4].value
        std = ds[0x300a,0xb0][0][0x300a,0xf4][nivo][0x300a,0xf6].value # Source to Block Tray Distance
        diverg = ds[0x300a,0xb0][0][0x300a,0xf4][nivo][0x300a,0xf5].value #(300a, 00f8) Block Type CS: 'APERTURE'
        if diverg == 'Plaque electron': #Au CHU si plaque e- divergence OFF
                diverg = "N"
        if diverg == 'Plaque photon':
                diverg = "Y"
		# Beurk a modifier si possible Parser fichier gabarit xml
        outBeam = """[Beam"""+ str(nivo) +"""]
Description="""+ str(headercom)+"_"+ str(machine) +"_"+ str(idpat) +"_"+ str(namepat) +"_"+ str(planlabel) +"_"+ str(nomsdubeam)+"""
SSD="""+ str(ssd) +"""
STD="""+ str(std) +"""
NoOfBlocks=1
BLeft=0
BTop=0
BWidth=0
BHeight=0

[Beam"""+ str(nivo) +"""Block0]
Description= """+ str(namepat)+"-"+ str(nomsdubeam) +"""
DataSource=EasyCache
Divergent="""+ str(diverg) +"""
"""
        ecf_file.write(outBeam)

       # A data stream of (x,y) pairs which comprise the block edge.
       # The number of pairs shall be equal to Block Number of Points (300A,0104), and the vertices shall be interpreted as a closed polygon.
       # Coordinates are projected onto the machine socentric plane i
        item = ds [0x300a,0xb0][0][0x300a,0xf4][nivo][0x300a,0x106].value
        litem = len(item)

        i=0 # compteur de boucle while
        cpt=0 #compteur pour point .ecf
        coordonnees = []
        Xlist= []
        Ylist= []

        while i<litem:

                coordonnees = item [i:i+2] # [0_ixOK 1_iyOK  [2 Exit non compris
                X = coordonnees [0]
                Y = coordonnees [1]

                Xlist.append(X)
                Ylist.append(Y)

                #Facteur agrandissement fixe a 9
                Xeasycut = int(X*9)
                Yeasycut = int(Y*9)

                #Ecriture du .ecf coordonnees
                outX = "X"+ str(cpt)+ "=" + str(Xeasycut)+'\n'
                outY = "Y"+ str(cpt)+ "=" + str(Yeasycut)+'\n'

                ecf_file.write(outX)
                ecf_file.write(outY)

                cpt = cpt + 1 #Compteur de point dans .ecf
                i=i+2

def f_graphCache():
        #Dessine le cache item = ds [0x300a,0xb0][nivo][0x300a,0xf4][0][0x300a,0x106].value
        a.plot(Xlist,Ylist, 'b', label=''+namepat+' - ('+nomsdubeam+')')
        a.legend()
        canvas.show()


def f_creerEcf():
        global ecf_path, tictac, ecf_out, ecf_file
        #Creation du fichier .ecf
        tictac = time.strftime('_%d%m%y%H%M',time.localtime())
        ecf_folder = str(Vcible) + '/' #Remarque les \\ au lieu de \ ( r'\'' == "\\'")
        ecf_path = str(ecf_folder) + str(namepat) +"_"+ str(planlabel) +"_"+ str(nomsdubeam) + ".ecf"
        ecf_file = open(ecf_path , 'w')

def f_creerMatplotGraphe():
	global f, a, canvas
	f = Figure()
	a = f.add_subplot(111)
	a.axis([-100,100,-100,100])
	a.axvline(color='k')  # axe des y
	a.axhline(color='k')  # axe des x
	a.grid()            # reprend les labels des plots

	# Figure matplotlib dans GUI
	canvas = FigureCanvasTkAgg(f, master=root)
	canvas._tkcanvas.grid(column=1, row=1,rowspan =4)
	canvas.show()

# ====> GUI
root = Tk.Tk()
root.wm_title("EasyCache")

f_creerMatplotGraphe()

#Infos Pat.
labeltxt1Var=Tk.StringVar()
labeltxt1Var.set('')
labeltxt1 = Tk.Label(root, textvariable=labeltxt1Var, anchor="w", fg="blue")
labeltxt1.grid(column=0, row=1, sticky="W")

#Source
Vsource = ''
buttonSource = Tk.Button(master=root, text = "Source >", command= buttonClickSource, bg='red' )
buttonSource.grid(column=0, row=5, sticky='EW')

labelScrVar=Tk.StringVar()
labelScrVar.set("     <<<     RT_PLAN.DCM Eclipse")
labelScr = Tk.Label(master=root, textvariable=labelScrVar,anchor="w",fg="red",bg="white")
labelScr.grid(column=1, row=5, sticky="EW")

#Cible
Vcible = ""
Vinitialdir = ""
buttonCible = Tk.Button(master=root,text = "   Cible >",command= buttonClickCible, bg='#01A2FF')
buttonCible.grid(column=0, row=6, sticky='EW')

labelCblVar=Tk.StringVar()
labelCblVar.set("     <<<    Disquette Decoupeur EasyCut")
labelCbl = Tk.Label(master=root, textvariable=labelCblVar, anchor="w",fg="blue",bg="white")
labelCbl.grid(column=1, row=6, sticky="EW")

#process
buttonProcess = Tk.Button(master=root,text = "Process",command= buttonClickProcess, bg='green')
buttonProcess.grid(column=1, row=7, sticky='EW')

#clear
buttonClear = Tk.Button(master=root,text = "Clear",command= buttonClickClear, bg='gray')
buttonClear.grid(column=0, row=7, sticky='EW')

root.grid_rowconfigure(0, minsize=10)
root.resizable(False,False) #Verrouille le redimentionement de la fenetre en (Largeur, Hauteur)
# <==== GUI

#Mainloop GUI
Tk.mainloop()


