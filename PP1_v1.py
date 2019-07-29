# ligne de code pour actualiser le fichier design.ui
#/aller chercher PySide2-ui.exe > C:\Users\AELION\BCH\Qt_interface_graphique\venv\Scripts\pyside2-ui.exe
# C:\Users\AELION\BCH\Qt_interface_graphique\venv\Scripts\pyside2-uic.exe pp_Design_v1.ui > ui_pp_design_v1.py
#
#
# METHODE CLASS:
# Réaliser un fichier par class et l'appeler dans le prog


# METHODE PROCEDURALE:
import sys, json
from PySide2.QtWidgets import (QLabel, QApplication,QPushButton,QVBoxLayout, QHBoxLayout, QWidget, QLineEdit,
                               QListWidget, QSpacerItem, QInputDialog, QTableWidgetItem, QDoubleSpinBox )
from ui_pp_design_v1 import Ui_Form
import numpy as np

# charger le JSON dans un dico
# dicoJson= json.load(open("structureDonnees.json"))
filename= "structureDonnees.json"


class EditeurNote(QWidget):
    def __init__(self):
        super(EditeurNote, self).__init__()

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
        self.ui.cbMatiereSelect.currentIndexChanged.connect(self.affichageEleves)
        self.ui.pbNoteAjout.clicked.connect(self.ajoutNote)


        self.majAcademies()

    # faire une liste des académies et en ajouter une
    def majAcademies(self):
        self.ui.cbAcademieSelect.clear()
        listAcademies = [ac["nom"] for ac in self.dicoJson["academies"]]
        self.ui.cbAcademieSelect.addItems(listAcademies)
        # print(listAcademies)

    # faire une liste des etablissements et en ajouter un
    def majEtablissements(self):
        self.ui.cbEtablissementSelect.clear()
        listEtablissements=[et["nom"] for et in self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()]["etablissements"]]
        self.ui.cbEtablissementSelect.addItems(listEtablissements)
        # print(listEtablissements)

    # faire une liste des classes et en ajouter une
    def majClasses(self):
        self.ui.cbClasseSelect.clear()
        listClasses=[cl["nom"] for cl in self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
                    ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()]["classes"]]
        self.ui.cbClasseSelect.addItems(listClasses)
        # print(listClasses)

    # recup liste eleves puis liste des matières de tous les eleves sans doublons (np.unique)
    def majMatiere(self):
        self.ui.cbMatiereSelect.clear()
        dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
                            ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
                            ["classes"][self.ui.cbClasseSelect.currentIndex()] \
                            ["eleves"]
        # print(dicoEleves)
        listMatieres=[]
        for eleves in dicoEleves:
            for ma in eleves["matieres"]:
                listMatieres.append(ma["nom"])
        listMatieresUniques = np.unique(listMatieres)
        self.ui.cbMatiereSelect.addItems(listMatieresUniques)
        # print(listMatieresUniques)

    def affichageEleves(self):
        cpt= 0
        self.ui.twSaisieNote.clearContents()
        # self.ui.twSaisieNote.selectColumnCount(2)     # pour avoir '2' colonnes
        dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
                            ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
                            ["classes"][self.ui.cbClasseSelect.currentIndex()] \
                            ["eleves"]
        for eleves in dicoEleves:
            for matiere in eleves["matieres"]:
                mat = self.ui.cbMatiereSelect.currentText()
                if matiere["nom"] == mat:
                    nomE = eleves["nom"]
                    self.ui.twSaisieNote.setRowCount(cpt+1)
                    itemE = QTableWidgetItem(nomE)
                    self.ui.twSaisieNote.setItem(cpt, 0, itemE)
                    spinB = QDoubleSpinBox()
                    spinB.setProperty("nom", nomE)
                    self.ui.twSaisieNote.setCellWidget(cpt, 1, spinB)
                    cpt = cpt+1

    def ajoutNote(self):
        dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
            ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
            ["classes"][self.ui.cbClasseSelect.currentIndex()] \
            ["eleves"]

        n = self.ui.twSaisieNote.rowCount()
        for i in range(0, n):
            mat = self.ui.cbMatiereSelect.currentText()
            eleveTw = self.ui.twSaisieNote.item(i, 0).text()
            spinB = self.ui.twSaisieNote.cellWidget(i,1)
            note = spinB.value()
            nomDevoir = self.ui.leDevoirEdit.text()
            coeff = self.ui.dsbCoeffDevoir.value()
            for eleves in dicoEleves:
                if eleves["nom"] == eleveTw:
                    for matiere in eleves["matieres"]:
                        if matiere["nom"] == mat :
                            # print(eleves["nom"], matiere["nom"], 'devoir:', nomDevoir, 'coeff:', coeff, 'note:', note)
                            ajoutNotes = matiere["notes"]
                            ajoutNotes.append({"nom": nomDevoir, "coefficient": coeff, "valeur": note})
                            print(ajoutNotes)
                            self.sauveJSON(filename)

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



    # def ajoutNotes(nom, coefficient, valeur):
    #     dicoJson["academies"][0]["etablissements"][0]["classes"]["eleves"][0]["matieres"][0]["notes"].append('{\
    #     "nom": nom, "coefficient": coeff, "valeur": valeur}')
    #
    # def ajoutAcademie(nom, adresse, classes):
    #     dicoJson["academies"][0]["etablissements"].append('{"nom": nom, "adresse":adresse, "classes": []}')
    #
    # def ajoutEtablissement(nom, adresse, classes):
    #     dicoJson["academies"][0]["etablissements"].append('{"nom": nom, "adresse":adresse, "classes": []}')
    #
    # def ajoutClasse(nom, pp, anneesco, eleve):
    #     dicoJson["academies"][0]["etablissements"][0]["classes"].append('{"nom": nom, "PP": pp, "anneeSco": anneesco, \
    #               "eleves": []}')
    #
    # def ajoutEleve(nom, prenom, adresse, appreciationPP, matieres):
    #     dicoJson["academies"][0]["etablissements"][0]["classes"][0]["eleves"].append('{"nom": nom, "prenom": prenom, \
    #               "adresse": adresse, "appreciationPP": appreciation, "matieres": []}')
    #
    # def ajoutMatière(nom, appreciation, coefficient, notes):
    #     dicoJson["academies"][0]["etablissements"][0]["classes"][0]["eleves"][0]["matieres"].append('{"nom": nom, \
    #     "appreciation": appreciation, "cefficient": coeff, "appreciationPP": appreciation, "matieres": []}')
    #
    # def ajoutNotes(nom, coefficient, valeur):
    #     dicoJson["academies"][0]["etablissements"][0]["classes"][0]["eleves"][0]["matieres"][0]["notes"].append('{\
    #     "nom": nom, "coefficient": coeff, "valeur": valeur}')



if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    rep = EditeurNote()
    rep.show()
    # Run the main Qt loop
    sys.exit(app.exec_())