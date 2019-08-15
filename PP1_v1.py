# ligne de code pour actualiser le fichier design.ui
#/aller chercher PySide2-ui.exe > C:\Users\AELION\BCH\Qt_interface_graphique\venv\Scripts\pyside2-ui.exe
# C:\Users\AELION\BCH\Qt_interface_graphique\venv\Scripts\pyside2-uic.exe pp_Design_v1.ui > ui_pp_design_v1.py
#
#
# METHODE CLASS:
# Réaliser un fichier par class et l'appeler dans le prog


# METHODE PROCEDURALE:
import sys, json
from PySide2 import QtCore
from PySide2.QtWidgets import (QWidget, QApplication, QTableWidgetItem, QDoubleSpinBox, QMessageBox, QLabel,
                               QPushButton,QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QSpacerItem, QInputDialog )
import numpy as np
from ui_pp_design_v1 import Ui_Form     #design fenetre principale
from ui_pp_Design_v2 import Ui_Form_W2  #design fenetre secondaire
from pylab import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


# charger le JSON
filename= "structureDonnees.json"

class EditeurNote(QWidget):
    def __init__(self):
        super(EditeurNote, self).__init__()
        self.setWindowTitle(u"Editeur de note")

        global filename
        self.dicoJson = {}
        self.dicoJson = self.lireJSON(filename)

        self.ui = Ui_Form()
        self.ui.setupUi(self)  # permet de charger tous les composants graphiques coder dans un autre fichier
        # partir du fichier .py (au lieu du .ui) permet d'accéder à la complétion cad la liste des fonctions, widgets...

        # print(dicoJson)

        # lier mes comboBox aux listes dédiées
        self.ui.cbAcademieSelect.currentIndexChanged.connect(self.majEtablissements)
        self.ui.cbEtablissementSelect.currentIndexChanged.connect(self.majClasses)
        self.ui.cbClasseSelect.currentIndexChanged.connect(self.majMatiere)
        self.ui.cbClasseSelect.currentIndexChanged.connect(self.majAffichageMoyenne)
        self.ui.cbMatiereSelect.currentIndexChanged.connect(self.affichageEleves)
        self.ui.pbNoteAjout.clicked.connect(self.ajoutNote)
        self.ui.pbNoteAjout.clicked.connect(self.majAffichageMoyenne)
        self.ui.twAffichageMoyennes.itemClicked.connect(self.radar)
        self.ui.pbGestionDb.clicked.connect(self.nwGestionBd)

        self.majAcademies()

    def majAcademies(self): # creation liste académies  + maj comboBox
        self.ui.cbAcademieSelect.clear()
        listAcademies = [ac["nom"] for ac in self.dicoJson["academies"]]
        self.ui.cbAcademieSelect.addItems(listAcademies)
        # print("majAcademies")
    def majEtablissements(self): # creation liste etablissements  + maj comboBox
        self.ui.cbEtablissementSelect.clear()
        listEtablissements=[et["nom"] for et in self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()]["etablissements"]]
        self.ui.cbEtablissementSelect.addItems(listEtablissements)
        # print("majEtablissements")
    def majClasses(self): # creation liste des classes + maj comboBox
        self.ui.cbClasseSelect.clear()
        listClasses=[cl["nom"] for cl in self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
                    ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()]["classes"]]
        self.ui.cbClasseSelect.addItems(listClasses)
        # print("majClasses")
    def majMatiere(self): #recup liste eleves + liste matières de tous eleves sans doublons (np.unique) + maj comboBox
        self.ui.cbMatiereSelect.clear()
        self.ui.cbMatiereSelectSuppr.clear()
        dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
                            ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
                            ["classes"][self.ui.cbClasseSelect.currentIndex()] \
                            ["eleves"]
        listMatieres=[]
        for eleves in dicoEleves:
            for ma in eleves["matieres"]:
                listMatieres.append(ma["nom"])
        listMatieresUniques = np.unique(listMatieres)
        self.ui.cbMatiereSelect.addItems(listMatieresUniques)
        self.ui.cbMatiereSelectSuppr.addItems(listMatieresUniques)
        # print("majMatieres")
    def affichageEleves(self):
        cpt= 0
        self.ui.twSaisieNote.clearContents()
        header = ["Nom", "Prénom", "Note"]
        self.ui.twSaisieNote.setColumnCount(len(header))     # pour avoir X colonnes
        self.ui.twSaisieNote.setHorizontalHeaderLabels(header)  #pour avoir les titre de colonne
        dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
                            ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
                            ["classes"][self.ui.cbClasseSelect.currentIndex()] \
                            ["eleves"]
        for eleves in dicoEleves:
            for matiere in eleves["matieres"]:
                mat = self.ui.cbMatiereSelect.currentText()
                if matiere["nom"] == mat:
                    nomE = eleves["nom"]
                    prenomE = eleves["prenom"]
                    self.ui.twSaisieNote.setRowCount(cpt+1)
                    itemEn = QTableWidgetItem(nomE)
                    self.ui.twSaisieNote.setItem(cpt, 0, itemEn)
                    # self.ui.twSaisieNote.setRowCount(cpt+1)
                    itemEp = QTableWidgetItem(prenomE)
                    self.ui.twSaisieNote.setItem(cpt, 1, itemEp)
                    spinB = QDoubleSpinBox()
                    spinB.setProperty("nom", nomE)
                    self.ui.twSaisieNote.setCellWidget(cpt, 2, spinB)
                    cpt = cpt+1
        # print("affichageEleveTWajoutNote")
    def ajoutNote(self):
        dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
            ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
            ["classes"][self.ui.cbClasseSelect.currentIndex()] \
            ["eleves"]
        n = self.ui.twSaisieNote.rowCount()
        for i in range(0, n):
            mat = self.ui.cbMatiereSelect.currentText()
            eleveTw = self.ui.twSaisieNote.item(i,0).text()
            spinB = self.ui.twSaisieNote.cellWidget(i,2)
            noteSb = spinB.value()
            nomDevoir = self.ui.leDevoirEdit.text()
            coefDv = self.ui.dsbCoeffDevoir.value()
            if nomDevoir == '' or coefDv ==0.0:         #bloque l'ajout de devoir sans nom ou sans coef
                print("stop")
            else:
                for eleves in dicoEleves:
                    if eleves["nom"] == eleveTw:
                        for matiere in eleves["matieres"]:
                            if matiere["nom"] == mat :
                                # print(eleves["nom"], matiere["nom"], 'devoir:', nomDevoir, 'coefDv:', coeff, 'note:', noteSb)
                                ajoutNotes = matiere["notes"]
                                ajoutNotes.append({"nom": nomDevoir, "coef": coefDv, "valeur": noteSb})
                                print("Devoir ajouté !", eleves["nom"], matiere["nom"], ajoutNotes)
                                # self.sauveJSON(filename)
                # self.ui.twSaisieNote.cellWidget(i, 2).cleanText()
        self.ui.leDevoirEdit.clear()            #réinitialise le nom du devoir
        self.ui.dsbCoeffDevoir.setValue(0.0)   #réinitialise le coef du devoir
        self.majMatiere()
    def majAffichageMoyenne (self): #, classe, eleveNom, elevePrenom, moyEleve, moyClasse):

        dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
            ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
            ["classes"][self.ui.cbClasseSelect.currentIndex()] \
            ["eleves"]

        self.ui.twAffichageMoyennes.clearContents()

        listMatieres = []
        for eleves in dicoEleves:
            for ma in eleves["matieres"]:
                listMatieres.append(ma["nom"])
        listMatieresUniques = np.unique(listMatieres)
        header = np.insert(listMatieresUniques, 0, "Prénom")
        header = np.insert(header, 0, "Nom")
        self.ui.twAffichageMoyennes.setColumnCount(len(header))  # pour avoir X colonnes
        self.ui.twAffichageMoyennes.setHorizontalHeaderLabels(header)  # pour avoir les titres de colonne

        # header = ["Nom", "Prénom", "Matière"]
        # self.ui.twAffichageMoyennes.setColumnCount(len(header))  # pour avoir X colonnes
        # self.ui.twAffichageMoyennes.setHorizontalHeaderItem(header)

        cptRow = 0
        for eleves in dicoEleves:
            nomE = eleves["nom"]
            prenomE = eleves["prenom"]
            self.ui.twAffichageMoyennes.setRowCount(cptRow + 1)
            itemEn = QTableWidgetItem(nomE)
            self.ui.twAffichageMoyennes.setItem(cptRow, 0, itemEn)
            itemEp = QTableWidgetItem(prenomE)
            self.ui.twAffichageMoyennes.setItem(cptRow, 1, itemEp)
            cptCol = 2
            # print(eleves["nom"])
            for matiere in eleves["matieres"]:
                # self.ui.twAffichageMoyennes.setColumnCount(cptCol + 1)
                # itemMat = QTableWidgetItem(matiere["nom"])
                # self.ui.twAffichageMoyennes.setHorizontalHeaderItem(cptCol, itemMat)
                mat = self.ui.twAffichageMoyennes.horizontalHeaderItem(cptCol).text()
                if matiere["nom"] != mat:
                    end = 0
                    # print(len(eleves["matieres"]), matiere["nom"], matiere["notes"])
                    while matiere["nom"] != mat and end < (len(header)-2):
                        end += 1
                        cptCol += 1
                        mat = self.ui.twAffichageMoyennes.horizontalHeaderItem(cptCol).text()
                        # print('while', mat, matiere["nom"])
                if matiere["nom"] == mat and matiere["notes"] != []:
                    # Calcul Moyennes
                    sumNoteE = 0
                    sumCoefE = 0
                    for note in matiere["notes"]:
                            sumNoteE += note["valeur"]*note["coef"]
                            sumCoefE += note["coef"]
                    moyEleve = str(sumNoteE / sumCoefE)
                    # Affichage moyennes
                    itemEmoy = QTableWidgetItem(moyEleve)
                    self.ui.twAffichageMoyennes.setItem(cptRow, cptCol, itemEmoy)
                    cptCol=2
                    # print('for', matiere["nom"])
                else:
                    cptCol=2
                    # print('pass', matiere["nom"], "notes", matiere["notes"])
            cptRow += 1
        # print("affichageEleveTWradar")
    def lireJSON(self,fileName):
        with open(fileName) as json_file:
            dico = json.load(json_file)
            return dico
        return None
    def sauveJSON(self, fileName):
        jsonClasse = json.dumps(self.dicoJson, sort_keys=True, indent=2)
        f = open(fileName, 'w')
        f.write(jsonClasse)
        f.close()
    def radar(self):
        if self.ui.qRadar.count() >= 2:
            self.ui.qRadar.removeWidget(self.canvas)
        dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
            ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
            ["classes"][self.ui.cbClasseSelect.currentIndex()] \
            ["eleves"]
        row = self.ui.twAffichageMoyennes.currentRow()
        nomEleve = self.ui.twAffichageMoyennes.item(row, 0).text()
        prenomEleve = self.ui.twAffichageMoyennes.item(row, 1).text()
        eleveR = [nomEleve, prenomEleve]
        radarMatiere = []
        radarMoy = []
        matListe = []
        for eleve in dicoEleves:
            # print(eleve["nom"])
            if eleve["nom"] == nomEleve and eleve["prenom"] == prenomEleve:
                print(eleve["nom"])
                for matiere in eleve["matieres"]:
                    # print(eleve["nom"], matiere["nom"])
                    if matiere["notes"] != []:
                        # Calcul Moyennes
                        sumNoteE = 0
                        sumCoefE = 0
                        for note in matiere["notes"]:
                            sumNoteE += note["valeur"] * note["coef"]
                            sumCoefE += note["coef"]
                        moyEleve = sumNoteE / sumCoefE
                        matR = matiere["nom"]
                        moyER = moyEleve
                        radarMatiere.append(matR)
                        matListe.append([matR, 0, 0])
                        radarMoy.append(moyER)
        for eleve in dicoEleves:
            # liste de moyenne et nbre eleve par matiere:
            for matiere in eleve["matieres"]:
                cpt = 0
                for m in matListe:
                    if m[0] == matiere["nom"]:
                        matListe[cpt][1] += 1
                        sumNoteCE = 0
                        sumCoefCE = 0
                        for note in matiere["notes"]:
                            sumNoteCE += note["valeur"] * note["coef"]
                            sumCoefCE += note["coef"]
                        moyCEleve = sumNoteCE / sumCoefCE
                        matListe[cpt][2] += moyCEleve
                        break
                    # print(m[cpt][0])#,m[cpt][2],m[cpt][1])
                    # moyClasse=([m[cpt][0],float(m[cpt][2])/float(m[cpt][1])])
                    cpt += 1
        # print(matListe)
        # print(radarMatiere)
        listMoyC = []
        for i in range(len(matListe)):
            listMoyC.append(matListe[i][2]/matListe[i][1])
        # print(listMoyC)
        labels = radarMatiere
        moysE = radarMoy
        if moysE==[]:
            self.ui.qRadar.removeWidget(self.canvas)
            self.ui.qRadar.isEmpty()
        else:
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
            # close the plot
            moyenneEleveR = np.concatenate((moysE, [moysE[0]]))
            moyenneClasseR = np.concatenate((listMoyC, [listMoyC[0]]))
            angles = np.concatenate((angles, [angles[0]]))

            self.fig = plt.figure(figsize=(4,4))
            ax = self.fig.add_subplot(111, polar=True)
            ax.plot(angles, moyenneEleveR, 'o-', linewidth=2,label="Moyenne de l'élève")
            ax.fill(angles, moyenneEleveR, alpha=0.2)
            ax.plot(angles, moyenneClasseR, 'o-', linewidth=2, label="Moyenne de la classe")
            ax.fill(angles, moyenneClasseR, alpha=0.2)
            ax.set_thetagrids(angles * 180 / np.pi, labels)
            plt.yticks([2, 4, 6, 8, 10, 12, 14, 16, 18], color="grey", size=7)
            plt.ylim(0, 20)

            ax.set_title(eleveR)
            ax.grid(True)
            plt.legend(loc='upper right')

            self.canvas = FigureCanvas(self.fig)  # the matplotlib canvas
            self.ui.qRadar.addWidget(self.canvas)

            self.setLayout(self.ui.qRadar)
            self.show()
    def nwGestionBd (self):
        self.gestionBd = GestionBd() #Lance la deuxième fenêtre
        # la deuxième fenêtre sera 'modale' (la première fenêtre sera inactive)
        self.gestionBd.setWindowModality(QtCore.Qt.ApplicationModal)
        # appel de la deuxième fenêtre
        self.gestionBd.show()

class GestionBd(QWidget):
    def __init__(self):
        super(GestionBd, self).__init__()
        self.setWindowTitle(u"Gestion base de donnée")
        global filename
        self.dicoJson = {}
        self.dicoJson = self.lireJSON(filename)
        self.ui2 = Ui_Form_W2()
        self.ui2.setupUi(self)
# MATIERE__________________________________________________________________________
        self.ui2.BDcbMatAcaSelect.currentIndexChanged.connect(self.majMatEta)
        self.ui2.BDcbMatEtaSelect.currentIndexChanged.connect(self.majMatCla)
        self.ui2.BDcbMatClaSelect.currentIndexChanged.connect(self.majMatEle)
        self.ui2.BDcbMatEleNoSelect.currentIndexChanged.connect(self.majMat)
        self.ui2.BDcbMatModifSelect.currentIndexChanged.connect(self.majMatModif)
        self.ui2.BDpbMatModifValid.clicked.connect(self.confirmModifMat)
        self.ui2.BDpbMatAjoutValid.clicked.connect(self.ajoutMat)
        self.ui2.BDpbMatSupprValid.clicked.connect(self.confirmSupprMat)
        self.majMatAca()
# ELEVE__________________________________________________________________________
        self.ui2.BDcbEleAcaSelect.currentIndexChanged.connect(self.majEleEta)
        self.ui2.BDcbEleEtaSelect.currentIndexChanged.connect(self.majEleCla)
        self.ui2.BDcbEleClaSelect.currentIndexChanged.connect(self.majEle)
        self.ui2.BDcbEleModifSelectNom.currentIndexChanged.connect(self.majEleModif)
        self.ui2.BDpbEleModifValid.clicked.connect(self.confirmModifEle)
        self.ui2.BDpbEleAjoutValid.clicked.connect(self.ajoutEle)
        self.ui2.BDpbEleSupprValid.clicked.connect(self.confirmSupprEle)
        self.majEleAca()

# MATIERE__________________________________________________________________________
    def majMatAca(self):
        self.ui2.BDcbMatAcaSelect.clear()
        listAca = [ac["nom"] for ac in self.dicoJson["academies"]]
        self.ui2.BDcbMatAcaSelect.addItems(listAca)
    def majMatEta(self):
        self.ui2.BDcbMatEtaSelect.clear()
        listEta = [et["nom"] for et in
                              self.dicoJson["academies"][self.ui2.BDcbMatAcaSelect.currentIndex()]["etablissements"]]
        self.ui2.BDcbMatEtaSelect.addItems(listEta)
    def majMatCla(self):
        self.ui2.BDcbMatClaSelect.clear()
        listCla = [cl["nom"] for cl in self.dicoJson["academies"][self.ui2.BDcbMatAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbMatEtaSelect.currentIndex()]["classes"]]
        self.ui2.BDcbMatClaSelect.addItems(listCla)
    def majMatEle(self):
        self.ui2.BDcbMatEleNoSelect.clear()
        listEleNom = [el["nom"] for el in self.dicoJson["academies"][self.ui2.BDcbMatAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbMatEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbMatClaSelect.currentIndex()]["eleves"]]
        listElePrenom = [el["prenom"] for el in self.dicoJson["academies"][self.ui2.BDcbMatAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbMatEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbMatClaSelect.currentIndex()]["eleves"]]
        listEle=[]
        for i in range(0, len(listEleNom)):
            nl = f"{listEleNom[i]} {listElePrenom[i]}"
            listEle.append(nl)
        self.ui2.BDcbMatEleNoSelect.addItems(listEle)
    def majMat(self):
        self.ui2.BDcbMatModifSelect.clear()
        self.ui2.BDcbMatSupprSelect.clear()
        self.ui2.BDleMatModifApp.clear()
        dicoMat =self.dicoJson["academies"][self.ui2.BDcbMatAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbMatEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbMatClaSelect.currentIndex()] \
            ["eleves"][self.ui2.BDcbMatEleNoSelect.currentIndex()]["matieres"]
        listMatNom = [mat["nom"] for mat in dicoMat]
        self.ui2.BDcbMatModifSelect.addItems(listMatNom)
        self.ui2.BDcbMatSupprSelect.addItems(listMatNom)
        self.majMatModif()
    def majMatModif(self):
        self.ui2.BDdsbMatModifCoef.setValue(0.0)
        self.ui2.BDleMatModifApp.clear()
        self.ui2.BDleMatModifNom.clear()
        dicoMat = self.dicoJson["academies"][self.ui2.BDcbMatAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbMatEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbMatClaSelect.currentIndex()] \
            ["eleves"][self.ui2.BDcbMatEleNoSelect.currentIndex()]["matieres"]
        matCoef = dicoMat[self.ui2.BDcbMatModifSelect.currentIndex()]["coef"]
        matApp = dicoMat[self.ui2.BDcbMatModifSelect.currentIndex()]["appreciation"]
        matNom = dicoMat[self.ui2.BDcbMatModifSelect.currentIndex()]["nom"]
        self.ui2.BDdsbMatModifCoef.setValue(matCoef)
        self.ui2.BDleMatModifApp.setText(matApp)
        self.ui2.BDleMatModifNom.setText(matNom)
    def modifMat(self):
        dicoModifMat = self.dicoJson["academies"][self.ui2.BDcbMatAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbMatEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbMatClaSelect.currentIndex()] \
            ["eleves"][self.ui2.BDcbMatEleNoSelect.currentIndex()]\
            ["matieres"][self.ui2.BDcbMatModifSelect.currentIndex()]

        dicoModifMat["nom"] = self.ui2.BDleMatModifNom.text()
        dicoModifMat["coef"] = self.ui2.BDdsbMatModifCoef.value()
        dicoModifMat["appreciation"] = self.ui2.BDleMatModifApp.text()
        if dicoModifMat["nom"] == '' or dicoModifMat["coef"] == 0.0:
            print("stop")
        else:
            print("Matière modifiée !")
            # self.sauveJSON(filename)
            self.majMat()
    def ajoutMat(self):
        dicoAjoutMat = self.dicoJson["academies"][self.ui2.BDcbMatAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbMatEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbMatClaSelect.currentIndex()] \
            ["eleves"][self.ui2.BDcbMatEleNoSelect.currentIndex()] \
            ["matieres"]

        nomMat = self.ui2.BDleMatAjoutNom.text()
        coefMat = self.ui2.BDdsbMatAjoutCoef.value()
        appMat = self.ui2.BDleMatAjoutApp.text()
        if nomMat == '' or coefMat == 0.0:
            print("stop")
        else:
            dicoAjoutMat.append({"nom": nomMat, "coef": coefMat, "appreciation": appMat, "notes":[]})
            print("Matière ajoutée !")
            # self.sauveJSON(filename)
            self.majMat()
            self.ui2.BDleMatAjoutNom.clear()
            self.ui2.BDdsbMatAjoutCoef.setValue(0.0)
            self.ui2.BDleMatAjoutApp.clear()
    def supprMat(self):
        dicoModifMat = self.dicoJson["academies"][self.ui2.BDcbMatAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbMatEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbMatClaSelect.currentIndex()] \
            ["eleves"][self.ui2.BDcbMatEleNoSelect.currentIndex()] \
            ["matieres"]

        dicoModifMat.pop(self.ui2.BDcbMatSupprSelect.currentIndex())
        print("Matière supprimée !")
        # self.sauveJSON(filename)
        self.majMat()
    def confirmSupprMat(self):
        print("confirm suppr")
        msgSuppr = QMessageBox()
        msgSuppr.setWindowTitle("Suppression")
        msgSuppr.setText("Confirmer la suppression de la matière: {}".format(self.ui2.BDcbMatSupprSelect.currentText()))
        msgSuppr.setStandardButtons(QMessageBox.Yes| QMessageBox.No)
        buttonY = msgSuppr.button(QMessageBox.Yes)
        buttonN = msgSuppr.button(QMessageBox.No)
        msgSuppr.exec()
        if msgSuppr.clickedButton() == buttonY:
            self.supprMat()
        elif msgSuppr.clickedButton() == buttonN:
            pass
    def confirmModifMat(self):
        print("confirm modif")
        msgModif = QMessageBox()
        msgModif.setWindowTitle("Modification")
        msgModif.setText(
            "Confirmer la modification de la matière: {}".format(self.ui2.BDcbMatModifSelect.currentText()))
        msgModif.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY= msgModif.button(QMessageBox.Yes)
        buttonN= msgModif.button(QMessageBox.No)
        msgModif.exec()
        if msgModif.clickedButton() == buttonY:
            self.modifMat()
        elif msgModif.clickedButton() == buttonN:
            pass

# ELEVE__________________________________________________________________________
    def majEleAca(self):
        self.ui2.BDcbEleAcaSelect.clear()
        listAca = [ac["nom"] for ac in self.dicoJson["academies"]]
        self.ui2.BDcbEleAcaSelect.addItems(listAca)
    def majEleEta(self):
        self.ui2.BDcbEleEtaSelect.clear()
        listEta = [et["nom"] for et in
                              self.dicoJson["academies"][self.ui2.BDcbEleAcaSelect.currentIndex()]["etablissements"]]
        self.ui2.BDcbEleEtaSelect.addItems(listEta)
    def majEleCla(self):
        self.ui2.BDcbEleClaSelect.clear()
        listCla = [cl["nom"] for cl in self.dicoJson["academies"][self.ui2.BDcbEleAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbEleEtaSelect.currentIndex()]["classes"]]
        self.ui2.BDcbEleClaSelect.addItems(listCla)
    def majEle(self):
        self.ui2.BDcbEleModifSelectNom.clear()
        self.ui2.BDcbEleSupprSelectNom.clear()
        self.ui2.BDleEleModifApp.clear()
        dicoEle =self.dicoJson["academies"][self.ui2.BDcbEleAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbEleEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbEleClaSelect.currentIndex()] \
            ["eleves"]
        listEleNom = [el["nom"] for el in dicoEle]
        listElePrenom = [el["prenom"] for el in dicoEle]
        listEle = []
        for i in range(0, len(listEleNom)):
            nl = f"{listEleNom[i]} {listElePrenom[i]}"
            listEle.append(nl)
        self.ui2.BDcbEleModifSelectNom.addItems(listEle)
        self.ui2.BDcbEleSupprSelectNom.addItems(listEle)
        self.majEleModif()
    def majEleModif(self):
        self.ui2.BDleEleModifAdres.clear()
        self.ui2.BDleEleModifApp.clear()
        self.ui2.BDleEleModifNom.clear()
        self.ui2.BDleEleModifPrenom.clear()
        dicoEle = self.dicoJson["academies"][self.ui2.BDcbEleAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbEleEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbEleClaSelect.currentIndex()] \
            ["eleves"]
        eleAdres = dicoEle[self.ui2.BDcbEleModifSelectNom.currentIndex()]["adresse"]
        eleApp = dicoEle[self.ui2.BDcbEleModifSelectNom.currentIndex()]["appreciationPP"]
        eleNom = dicoEle[self.ui2.BDcbEleModifSelectNom.currentIndex()]["nom"]
        elePrenom = dicoEle[self.ui2.BDcbEleModifSelectNom.currentIndex()]["prenom"]
        self.ui2.BDleEleModifAdres.setText(eleAdres)
        self.ui2.BDleEleModifApp.setText(eleApp)
        self.ui2.BDleEleModifNom.setText(eleNom)
        self.ui2.BDleEleModifPrenom.setText(elePrenom)
    def modifEle(self):
        dicoModifEle = self.dicoJson["academies"][self.ui2.BDcbEleAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbEleEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbEleClaSelect.currentIndex()] \
            ["eleves"][self.ui2.BDcbEleModifSelectNom.currentIndex()]

        dicoModifEle["nom"] = self.ui2.BDleEleModifNom.text()
        dicoModifEle["prenom"] = self.ui2.BDleEleModifPrenom.text()
        dicoModifEle["adresse"] = self.ui2.BDleEleModifAdres.text()
        dicoModifEle["appreciationPP"] = self.ui2.BDleEleModifApp.text()
        if dicoModifEle["nom"] == '' or dicoModifEle["prenom"] == '':
            print("stop")
        else:
            print("Elève modifié !")
            self.sauveJSON(filename)
            self.majEle()
    def ajoutEle(self):
        dicoAjoutEle = self.dicoJson["academies"][self.ui2.BDcbEleAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbEleEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbEleClaSelect.currentIndex()] \
            ["eleves"]

        nomEle = self.ui2.BDleEleAjoutNom.text()
        prenomEle = self.ui2.BDleEleAjoutPrenom.text()
        adresEle = self.ui2.BDleEleAjoutAdres.text()
        appEle = self.ui2.BDleEleAjoutApp.text()
        if nomEle == '' or prenomEle == '':
            print("stop")
        else:
            dicoAjoutEle.append({"nom": nomEle, "prenom": prenomEle, "adresse": adresEle, "appreciationPP": appEle, \
                                "matieres": []})
            print("Elève ajouté !")
            self.sauveJSON(filename)
            self.majEle()
            self.ui2.BDleEleAjoutNom.clear()
            self.ui2.BDleEleAjoutPrenom.clear()
            self.ui2.BDleEleAjoutAdres.clear()
            self.ui2.BDleEleAjoutApp.clear()
    def supprEle(self):
        dicoModifEle = self.dicoJson["academies"][self.ui2.BDcbEleAcaSelect.currentIndex()] \
            ["etablissements"][self.ui2.BDcbEleEtaSelect.currentIndex()] \
            ["classes"][self.ui2.BDcbEleClaSelect.currentIndex()] \
            ["eleves"]
        dicoModifEle.pop(self.ui2.BDcbEleSupprSelectNom.currentIndex())
        print("Elève supprimé !")
        self.sauveJSON(filename)
        self.majEle()
    def confirmSupprEle(self):
        print("confirm suppr")
        msgSuppr = QMessageBox()
        msgSuppr.setWindowTitle("Suppression")
        msgSuppr.setText("Confirmer la suppression de l'élève: {}".format(self.ui2.BDcbEleSupprSelectNom.currentText()))
        msgSuppr.setStandardButtons(QMessageBox.Yes| QMessageBox.No)
        buttonY = msgSuppr.button(QMessageBox.Yes)
        buttonN = msgSuppr.button(QMessageBox.No)
        msgSuppr.exec()
        if msgSuppr.clickedButton() == buttonY:
            self.supprEle()
        elif msgSuppr.clickedButton() == buttonN:
            pass
    def confirmModifEle(self):
        print("confirm modif")
        msgModif = QMessageBox()
        msgModif.setWindowTitle("Modification")
        msgModif.setText(
            "Confirmer la modification de l'élève: {}".format(self.ui2.BDcbEleModifSelectNom.currentText()))
        msgModif.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY= msgModif.button(QMessageBox.Yes)
        buttonN= msgModif.button(QMessageBox.No)
        msgModif.exec()
        if msgModif.clickedButton() == buttonY:
            self.modifEle()
        elif msgModif.clickedButton() == buttonN:
            pass

# EXIT____________________________________________________________________________
    def closeEvent(self, event):
        print("confirm exit")
        msgExit = QMessageBox()
        msgExit.setWindowTitle("exit")
        msgExit.setText("Voulez-vous sauvegarder les changements effectués avant de quitter ?")
        msgExit.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Discard)
        buttonS = msgExit.button(QMessageBox.Save)
        buttonD = msgExit.button(QMessageBox.Discard)
        buttonC = msgExit.button(QMessageBox.Cancel)
        msgExit.exec()
        if msgExit.clickedButton() == buttonS:
            editeurNote = EditeurNote()
            editeurNote.update()
            print("save")
            # self.sauveJSON(filename)
            event.accept()
        elif msgExit.clickedButton() == buttonD:
            print("discard")
            event.accept()
        elif msgExit.clickedButton() == buttonC:
            print("cancel")
            event.ignore()
# JSON__________________________________________________________________________
    def lireJSON(self,fileName):
        with open(fileName) as json_file:
            dico = json.load(json_file)
            return dico
        return None
    def sauveJSON(self, fileName):
        jsonClasse = json.dumps(self.dicoJson, sort_keys=True, indent=2)
        f = open(fileName, 'w')
        f.write(jsonClasse)
        f.close()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    rep = EditeurNote()
    rep.show()
    # Run the main Qt loop
    sys.exit(app.exec_())