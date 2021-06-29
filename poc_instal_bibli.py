# (c) Didier  LECLERC 2021 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé mars 2021

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QAction, QMenu , QApplication, QMessageBox
from PyQt5.QtGui import QIcon

from qgis.core import *
from qgis.gui import *

from . import dopoc_instal_bibli_ui
from . import bibli_poc_instal_bibli
from .bibli_poc_instal_bibli import *

import os


class MainPlugin(object):
  def __init__(self, iface):
     self.name = "Installation de bibliothèques"
     self.iface = iface
    
     # Generation de la traduction selon la langue choisie   
     overrideLocale = QSettings().value("locale/overrideFlag", False)
     localeFullName = QLocale.system().name() if not overrideLocale else QSettings().value("locale/userLocale", "")
     if localeFullName == None :
        self.localePath = os.path.dirname(__file__) + "/i18n/poc_instal_bibli_fr.qm"
     else :
        self.localePath = os.path.dirname(__file__) + "/i18n/poc_instal_bibli_" + localeFullName[0:2] + ".qm"
     if QFileInfo(self.localePath).exists():
        self.translator = QTranslator()
        self.translator.load(self.localePath)
        QCoreApplication.installTranslator(self.translator)
     # Generation de la traduction selon la langue choisie   

  def initGui(self):
     #Construction du menu
     self.menu=QMenu("BIBLI")
     self.menu.setTitle(QtWidgets.QApplication.translate("poc_instal_bibli_main", "POC Library installation") + "  (" + str(bibli_poc_instal_bibli.returnVersion()) + ")")

     menuIcon = bibli_poc_instal_bibli.pathIcon("poc_instal_bibli.png")
     self.poc = QAction(QIcon(menuIcon),"POC Library installation " + "  (" + str(bibli_poc_instal_bibli.returnVersion()) + ")",self.iface.mainWindow())
     self.poc.setText(QtWidgets.QApplication.translate("poc_instal_bibli_main", "Library installation") + "  (" + str(bibli_poc_instal_bibli.returnVersion()) + ")")
     self.poc.triggered.connect(self.run)
     
     #Ajouter une barre d'outils'
     self.toolBarName = QtWidgets.QApplication.translate("poc_instal_bibli_main", "My tool bar Library installation")
     self.toolbar = self.iface.addToolBar(self.toolBarName)
     # Pour faire une action
     self.toolbar.addAction(self.poc)
     #=========================
     
  def run(self):
      d = dopoc_instal_bibli_ui.Dialog()
      d.exec_()

  def unload(self):
      pass  
       
