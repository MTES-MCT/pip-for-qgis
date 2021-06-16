# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog
from qgis.core import *

from .poc_instal_bibli_ui import Ui_Dialog_POC

from . import bibli_poc_instal_bibli
from .bibli_poc_instal_bibli import *

class Dialog(QDialog, Ui_Dialog_POC):
      def __init__(self):
          QDialog.__init__(self)
          self.setupUi(self)
