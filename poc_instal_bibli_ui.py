# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020

from PyQt5 import QtCore, QtGui, QtWidgets, QtQuick 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QAction, QMenu , QMenuBar, QApplication, QMessageBox, QFileDialog, QPlainTextEdit, QDialog, QDockWidget, QVBoxLayout, QTabWidget, QWidget, QDesktopWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel

from . import bibli_poc_instal_bibli
from .bibli_poc_instal_bibli import *

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import QUrl

import qgis
import os
import time
import sys

class Ui_Dialog_POC(object):
    def __init__(self):
        self.iface = qgis.utils.iface
        self.firstOpen = True
        self.firstOpenConnect = True
    
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        lScreenDialog, hScreenDialog = 700, 500
        #--------
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,lScreenDialog, hScreenDialog).size()).expandedTo(Dialog.minimumSizeHint()))
        Dialog.setWindowTitle("Library installation")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        iconSource = bibli_poc_instal_bibli.pathIcon("poc_instal_bibli.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconSource), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)

        #=====================================================  
        #=====================================================
        #Image
        labelImage = QtWidgets.QLabel(Dialog)
        myPath = bibli_poc_instal_bibli.pathIcon("poc_instal_bibli.png")
        myDefPath = myPath.replace("\\","/")
        carIcon = QtGui.QImage(myDefPath)
        labelImage.setPixmap(QtGui.QPixmap.fromImage(carIcon))
        labelImage.setGeometry(QtCore.QRect(20, 20, 150, 80))
        labelImage.setObjectName("labelImage")
        
        #Zone affichage
        self.bibliInstaller = QtWidgets.QTextEdit(Dialog)
        larg, haut =  Dialog.width()/3 + 60, Dialog.width()/3
        x, y = ((Dialog.width()/2) - larg) / 2, 100
        self.bibliInstaller.setGeometry(QtCore.QRect(x, y, larg, haut))
        self.bibliInstaller.setObjectName("bibliInstaller") 
        self.bibliInstaller.setStyleSheet("QTextEdit {   \
                                border-style: outset;    \
                                border-width: 2px;       \
                                border-radius: 10px;     \
                                border-color: blue;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")
        
        #Zone affichage
        bibli_poc_instal_bibli.majListeBibli(Dialog)
        #--
        mDicAinstaller = bibli_poc_instal_bibli.returnListBibliAinstaller()
        mDicInstalle   = bibli_poc_instal_bibli.returnListBibli()
        #--
        mTextAinstaller = ''
        x, y = ((Dialog.width()/2) + ((Dialog.width()/2) - larg) / 2), 100

        for k, v in mDicAinstaller.items() :
            if k in mDicInstalle : 
               mTextAinstaller = k + " " + v + ' ** <b>MAJ</b>'
            else :            
               mTextAinstaller = k + " " + v
            bibli_poc_instal_bibli.createLabelCase( Dialog, x, y, mTextAinstaller, k, v )
            y += 30 
        
        #=====================================================
        #Boutons  
        #------       
        self.installeButton = QtWidgets.QPushButton(Dialog)
        self.installeButton.setGeometry(QtCore.QRect(((Dialog.width() / 2)  + 50),  (Dialog.height() - 80), 100,23))
        self.installeButton.setObjectName("installeButton")

        self.desinstalleButton = QtWidgets.QPushButton(Dialog)
        self.desinstalleButton.setGeometry(QtCore.QRect(((Dialog.width() / 2) - 150),  (Dialog.height() - 80), 100,23))
        self.desinstalleButton.setObjectName("desinstalleButton")

        self.okhButton = QtWidgets.QPushButton(Dialog)
        self.okhButton.setGeometry(QtCore.QRect(((Dialog.width() / 2) - 50),  (Dialog.height() - 50), 100,23))
        self.okhButton.setObjectName("okhButton")
        #------  
        #Connections  
        self.installeButton.clicked.connect(lambda : bibli_poc_instal_bibli.executeInstalle(Dialog, mDicAinstaller, mDicInstalle, "INSTALLE"))        
        self.desinstalleButton.clicked.connect(lambda : bibli_poc_instal_bibli.executeInstalle(Dialog, mDicAinstaller, mDicInstalle, "DESINSTALLE"))        
        self.okhButton.clicked.connect(Dialog.reject)        
                             
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("poc_instal_bibli_ui", "POC Library installation", None) + "  (" + str(bibli_poc_instal_bibli.returnVersion()) + ")")
        self.installeButton.setText(QtWidgets.QApplication.translate("poc_instal_bibli_ui", "Installe / Maj", None))
        self.desinstalleButton.setText(QtWidgets.QApplication.translate("poc_instal_bibli_ui", "Désinstalle", None))
        self.okhButton.setText(QtWidgets.QApplication.translate("poc_instal_bibli_ui", "Close", None))

    def resizeEvent(self, event):
        self.installeButton.setGeometry(QtCore.QRect(((self.width() / 2)  + 50),  (self.height() - 80), 100,23))
        self.desinstalleButton.setGeometry(QtCore.QRect(((self.width() / 2) - 150),  (self.height() - 80), 100,23))
        self.okhButton.setGeometry(QtCore.QRect(((self.width() / 2) - 50),  (self.height() - 50), 100,23))
                 