# (c) Didier  LECLERC 2021 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé mars 2021

def classFactory(iface):
  from .poc_instal_bibli import MainPlugin
  return MainPlugin(iface)