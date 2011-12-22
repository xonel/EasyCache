# -*- coding: cp1252 -*-
# EasyCache V3test: Eclipse EasyCut
# + Add transformation 3D/2D formule
# + ....

import dicom
from math import*

ds = dicom.read_file("RP.dcm") # (rtplan.dcm is in the testfiles directory)
#Creation du fichier .ecf
dump_file = open("dumpDicom" , 'w')
dump_file.write(str(ds))
dump_file.close()

print ds
print "Presence de la Key True/False :" 
print [0x300a,0x106] in ds #detecte la presence du cache1 en [0].
print "Voici le nom du patient : " + ds[0x10,0x10].value

angle=ds[0x300a,0xb0][0][0x300a,0x111][0][0x300a,0x11e].value
item=ds[0x300a,0xb0][0][0x300a,0xf4][0][0x300a,0x106].value
litem = len(item)
print item
print angle

# Header pour le fichier .ecf EasyCut
namepat = ds[0x10,0x10].value
dateplan = ds[0x300a,0x06].value
datepat = ds[0x10,0x30].value

ecf_path = "d:\\" + str(namepat) + ".ecf"

ecf_header = "[Header]\n"
ecf_dateplan = "Date=" + str(dateplan)+ '\n'    
ecf_namepat = str("PatientName=" + namepat)+ '\n'
ecf_datepat = "PatientDate=" + str(datepat)+ '\n'
ecf_beam = """Comment=
ID=0
NoOfBeams=0
ProgVersion=0

[Beam0]
Description=
SSD=0
STD=0
NoOfBlocks=0
BLeft=0
BTop=0
BWidth=0
BHeight=0

[Beam0Block0]
Description=
DataSource=
Divergent=
""" #le triple """ permet le multiligne sans \n

ecf_out = ecf_header + ecf_dateplan + ecf_namepat + ecf_datepat + ecf_beam 

#Creation du fichier .ecf
ecf_file = open(ecf_path , 'w')
ecf_file.write(ecf_out)

# Recuperation des coordonn�es via Dicom du cache1(UNIQUEMENT):
i=0
cpt=0
coordonnees = []

while cpt<litem/3:
        coordonnees = item [i:i+3] # Repere Eclipse X/Y/Z - [0:3[ = de [0&1&2] 3 exclu
        x3D = coordonnees [0]
        y3D = coordonnees [1]
        z3D = coordonnees [2]
        print x3D, y3D, z3D, cpt, i, litem/3, coordonnees, item[litem-1]
        
        x2D = int(round(((sqrt(2))/2)*(x3D-y3D)*9,1))
        y2D = int(round((sqrt(2/3*z3D))-(1/sqrt(6))*(x3D+y3D)*9,1))     
                
        outx2D = "X"+ str(cpt)+ "=" + str(x2D)+'\n'
        outy2D = "Y"+ str(cpt)+ "=" + str(y2D)+'\n'

        ecf_file.write(outx2D)
        ecf_file.write(outy2D)
        
        cpt=cpt+1
        i=i+3

        #print cache #Debug
        
ecf_file.close()        

print """

"""
print "...... FINI ;o)"
