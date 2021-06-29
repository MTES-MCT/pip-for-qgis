# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé mars 2021

from PyQt5 import QtCore, QtGui, QtWidgets, QtQuick 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QAction, QMenu , QMenuBar, QApplication, QMessageBox, QFileDialog, QPlainTextEdit, QDialog, QDockWidget, QVBoxLayout, QTabWidget, QWidget, QDesktopWidget, QSizePolicy

from qgis.utils import iface
from qgis.core import *
from qgis.gui import *
import subprocess
import re

import qgis                              
import os                       
import datetime
import sys
import os.path
import time
import pathlib

#==================================================
#Gestion de l'installation de bibliothèques
#==================================================
def majListeBibli(mDialog, mDic = None) :
    #Zone affichage
    mTextInstaller = ''
    for k, v in returnListBibli().items() : 
        mTextInstaller += k + " " + v + '\n'         
    mDialog.bibliInstaller.setText(mTextInstaller)
    #--
    mDicAinstaller = returnListBibliAinstaller()
    mDicInstalle   = returnListBibli()
    
    if mDic != None :
       for elemLabel in mDialog.children() :
          for cle, valeur in mDic.items() :
              if elemLabel.objectName() == 'label_' + (str(cle) + str(valeur[0])) :
                 if cle in mDicInstalle :
                    elemLabel.setText(str(cle) + " " + str(valeur[0]) + ' ** <b>MAJ</b>')
                 else :   
                    elemLabel.setText(str(cle) + " " + str(valeur[0]) )

#==================================================
def returnListBibli() :
    try:
        import pip
    except ImportError:
        exec(
            open(str(pathlib.Path(plugin_dir, 'scripts', 'get_pip.py'))).read()
        )
        import pip
        # just in case the included version is old
        subprocess.check_call(['python3', '-m', 'pip', 'uninstall', '--upgrade', 'pip'])

    mPathPerso = os.path.dirname(__file__) + '\\bibli_liste.txt'
    mPathPerso = mPathPerso.replace("\\","/")
    with open(mPathPerso, "w") as f:
         subprocess.check_call(['python3', '-m', 'pip', 'freeze'], stdout = f)
    #--
    with open(mPathPerso, "r") as requirements:
        mDic = {}
        for dep in requirements.readlines():
            mDic[dep.strip().split("==")[0].strip()] = dep.strip().split("==")[1].strip() 
    return mDic
    
#==================================================
def returnListBibliAinstaller():
    mPathPerso = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(mPathPerso,'bibli_a_installer.txt'), "r") as requirements:
        mDic = {}
        for dep in requirements.readlines():
            mDic[dep.strip().split("==")[0].strip()] = dep.strip().split("==")[1].strip() 
    return mDic

#==================================================
def createLabelCase( mDialog, mX, mY, mMTextAinstaller, cle, val ) :
    case = QtWidgets.QCheckBox(mDialog)    
    case.setGeometry(QtCore.QRect(mX, mY, 23, 23))
    case.setObjectName("case_" + str(cle) + str(val))
    case.setChecked(False)
    #-- 
    label = QtWidgets.QLabel(mDialog)
    label.setGeometry(QtCore.QRect(mX + 40, mY + 4, 200, 20))
    label.setObjectName("label_" + str(cle) + str(val))
    label.setAlignment(Qt.AlignLeft)
    label.setText(mMTextAinstaller)
     
    return

#==================================================
def executeInstalle( mDialog, mDicAinstaller, mDicInstalle, mOptions ) :

    mDic = {}
    for elemCase in mDialog.children() :
        for k, v  in mDicAinstaller.items() :
            if elemCase.objectName()[5:] == (str(k) + str(v)) :
               if elemCase.isChecked() :
                  #** MAJ
                  if k in mDicInstalle : 
                     mDic[str(k)] = [ str(v), 'MAJ']
                  else :   
                     mDic[str(k)] = [ str(v), 'INS']
    if len(mDic) == 0 : 
       QMessageBox.information(None, "Informations", "Pas de bibliothèque sélectionnée")
    else :
       installer_func(mDialog, mOptions, mDic)
    return

#==================================================
def installer_func(mDialog, mOptions, mDic):
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        import pip
    except ImportError:
        exec(
            open(str(pathlib.Path(plugin_dir, 'scripts', 'get_pip.py'))).read()
        )
        import pip
        # just in case the included version is old
        subprocess.check_call(['python3', '-m', 'pip', 'uninstall', '--upgrade', 'pip'])

    sys.path.append(plugin_dir)

    mProxy, mParamGlobPythonExe, mParamGlobParam1Pip, mParamGlobParam2Pip = returnProxyPac(), 'python3', '-m', 'pip'
    
    for cle,valeur in mDic.items():
         
        if mOptions == "INSTALLE" :
          try :
           mParamGlob = [] 
           mParamGlob.append(mParamGlobPythonExe) 
           mParamGlob.append(mParamGlobParam1Pip) 
           mParamGlob.append(mParamGlobParam2Pip)
           existeProxy = False 
           if valeur[1] == 'INS' :
              mParamGlob.append('install') 
              mParamGlob.append('--user') 
              if mProxy != None :
                 existeProxy = True 
                 mParamGlob.append('--proxy=' + str(mProxy)) 
                 mParamGlob.append('--no-warn-script-location') 
              mParamGlob.append(cle) 
           else :
              mParamGlob.append('install') 
              mParamGlob.append('--upgrade') 
              mParamGlob.append('--user') 
              if mProxy != None :
                 existeProxy = True 
                 mParamGlob.append('--proxy=' + str(mProxy)) 
                 mParamGlob.append('--no-warn-script-location') 
              mParamGlob.append(cle) 

           print("mParamGlob 1 {}".format(str(mParamGlob)))
           subprocess.check_call(mParamGlob, shell=False)
          except :
           mParamGlob = [] 
           mParamGlob.append(mParamGlobPythonExe) 
           mParamGlob.append(mParamGlobParam1Pip) 
           mParamGlob.append(mParamGlobParam2Pip) 
           if valeur[1] == 'INS' :
              mParamGlob.append('install') 
              mParamGlob.append('--user') 
              if existeProxy : 
                 mParamGlob.append('--no-warn-script-location') 
              mParamGlob.append(cle) 
           else :
              mParamGlob.append('install') 
              mParamGlob.append('--upgrade') 
              mParamGlob.append('--user') 
              if mProxy != None :
                 mParamGlob.append('--no-warn-script-location') 
              mParamGlob.append(cle) 

           print("mParamGlob 2 {}".format(str(mParamGlob)))
           subprocess.check_call(mParamGlob, shell=False)
          
        elif mOptions == "DESINSTALLE" :   
           subprocess.check_call(['python3', '-m', 'pip', 'uninstall', '--yes', cle])
    #--
    majListeBibli(mDialog, mDic)
    return       


#==================================================
def returnProxyPac():
    #ajout Alain
    try :
        import pypac
    except ImportError:
        import sys
        this_dir = os.path.dirname(os.path.realpath(__file__))
        import_path = os.path.join(this_dir, 'site-packages')
        sys.path.insert(0, import_path)
        import pypac
        from pypac import get_pac
    #ajout Alain 

    pac = pypac.get_pac(url=None, js=None, from_os_settings=True)
    
    if pac :
       mProxy = pac.find_proxy_for_url('www.google.fr', 'www.google.fr')
       print("mRet 1 {}".format(str(mProxy)))
       if mProxy.strip().upper() !=  "DIRECT" : 
          mPattern = '^PROXY'
          try :
             mProxy = mProxy[re.search(mPattern, mProxy).end():-1].strip()
          except :
             mProxy = None
       else :
          mProxy = None
       print("mRet 2 {}".format(str(mProxy)))
    else :
       mProxy = None
    return mProxy
    
#==================================================
def returnVersion() : return "version 0.2.0"

#==================================================
def pathIcon(name):
    MonFichierPath = os.path.join(os.path.dirname(__file__))
    MonFichierPath = MonFichierPath.replace("\\","/")        
    return MonFichierPath + "//icons/logo//" + name
    
    
#==================================================
#==================================================
def debugMess(type,zTitre,zMess, level=Qgis.Critical):
    #type 1 = MessageBar
    #type 2 = QMessageBox
    if type == 1 :
       qgis.utils.iface.messageBar().pushMessage(zTitre, zMess, level=level)
    else :
       QMessageBox.information(None,zTitre,zMess)
    return  

#==================================================
# FIN
#==================================================
