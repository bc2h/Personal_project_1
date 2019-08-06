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
from pylab import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


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
        self.ui.cbClasseSelect.currentIndexChanged.connect(self.majAffichageMoyenne)
        self.ui.pbNoteAjout.clicked.connect(self.ajoutNote)
        self.ui.pbNoteAjout.clicked.connect(self.majAffichageMoyenne)
        self.ui.twAffichageMoyennes.itemClicked.connect(self.radar)

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
            for eleves in dicoEleves:
                if eleves["nom"] == eleveTw:
                    for matiere in eleves["matieres"]:
                        if matiere["nom"] == mat :
                            # print(eleves["nom"], matiere["nom"], 'devoir:', nomDevoir, 'coefDv:', coeff, 'note:', noteSb)
                            ajoutNotes = matiere["notes"]
                            ajoutNotes.append({"nom": nomDevoir, "coef": coefDv, "valeur": noteSb})
        print(ajoutNotes)
                            # self.sauveJSON(filename)

    # def majMoyenne(self):
    #     print("majMoyenneIN")
    #     dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
    #         ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
    #         ["classes"][self.ui.cbClasseSelect.currentIndex()] \
    #         ["eleves"]
    #
    #     listMoyEleve = []
    #     for eleves in dicoEleves:
    #         for matiere in eleves["matieres"]:
    #             #Calcul Moyenne + Ajout twAffichageMoyenne
    #             sumNoteE = 0
    #             sumCoefE = 0
    #             for note in matiere["notes"]:
    #                 sumNoteE += note["valeur"]*note["coef"]
    #                 sumCoefE += note["coef"]
    #             moyEleve = sumNoteE / sumCoefE
    #             listMoyEleve.append(moyEleve)
    #     moyClasse = sum(listMoyEleve) / len(listMoyEleve)
    #     print (eleves["nom"], moyEleve, moyClasse)
    #     # self.majAffichageMoyenne(classe["nom"], eleve["nom"], eleve["prenom"], moyEleve, moyClasse)
    #     print("majMoyenneOUT")

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
        self.ui.twAffichageMoyennes.setHorizontalHeaderLabels(header)  # pour avoir les titre de colonne

        # header = ["Nom", "Prénom", "Matière"]
        # self.ui.twAffichageMoyennes.setColumnCount(len(header))  # pour avoir X colonnes
        # self.ui.twAffichageMoyennes.setHorizontalHeaderLabels(header)

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
            for matiere in eleves["matieres"]:
                # self.ui.twAffichageMoyennes.setColumnCount(cptCol + 1)
                itemMat = QTableWidgetItem(matiere["nom"])
                self.ui.twAffichageMoyennes.setHorizontalHeaderItem(cptCol, itemMat)
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
                cptCol += 1
                # print(eleves["nom"], eleves["prenom"], moyEleve)
            cptRow += 1


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

    def radar(self): #, matieres, moyEleve, moyClasse):
        print("radar")

        self.ui.twAffichageMoyennes.itemClicked

        dicoEleves = self.dicoJson["academies"][self.ui.cbAcademieSelect.currentIndex()] \
            ["etablissements"][self.ui.cbEtablissementSelect.currentIndex()] \
            ["classes"][self.ui.cbClasseSelect.currentIndex()] \
            ["eleves"]

        listMatieres = []
        for eleves in dicoEleves:
            for ma in eleves["matieres"]:
                listMatieres.append(ma["nom"])
            eleveR = (eleves["nom"], eleves["prenom"])
        listMatieresUniques = np.unique(listMatieres)
        print(eleveR)

        labels = listMatieresUniques
        moys = [10, 15, 18]

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        # close the plot
        stats = np.concatenate((moys, [moys[0]]))
        angles = np.concatenate((angles, [angles[0]]))

        self.fig = plt.figure()
        ax = self.fig.add_subplot(111, polar=True)
        ax.plot(angles, stats, 'o-', linewidth=2)
        ax.fill(angles, stats, alpha=0.25)
        ax.set_thetagrids(angles * 180 / np.pi, labels)
        plt.yticks([5, 10, 15], color="grey", size=7)
        plt.ylim(0, 20)

        ax.set_title(eleveR)
        ax.grid(True)

        self.canvas = FigureCanvas(self.fig)
        self.ui.lRadar.addWidget(self.canvas)  # the matplotlib canvas

        self.setLayout(self.ui.lRadar)
        self.show()


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    rep = EditeurNote()
    rep.show()
    # Run the main Qt loop
    sys.exit(app.exec_())