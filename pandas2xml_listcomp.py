#!/usr/bin/env python
# coding: utf-8

"""Convert pandas dataframe to XML (cdisc dataset-xml)
   by Dirk Engfer, https://www.datascience-dirk-engfer.de/
   Updates:
     May 18, 2021: apply listcomp instead of itertuples.
"""

import os, numpy as np
import pandas as pd
from xml.etree.ElementTree import ( Element, ElementTree,
                                    SubElement,
                                    Comment
                                    )
#from xml.etree.ElementTree import dump

homedir = os.getenv('HOME')

datapath = os.path.join(homedir, 'Dokumente','cdisc_dataset_xml_v1','Example', 'xml_concomitant_medication')

df = pd.read_csv(datapath+'/cm.csv', header=0, sep=',')
df['cmdose'] = df['cmdose'].astype(str) # strings to enable serialization
df['cmseq'] = df['cmseq'].astype(str)

#print(df.head())

output_xml_file = 'xml_cm_from_pandas_listcomp.xml'
sasvarL = ['STUDYID','DOMAIN','USUBJID','CMSEQ','CMTRT','CMSTDTC','CMDOSE','CMDOSU']

# Full variable List of SDTM.CM (all specified vars in the order they must appear in xml form)
fullvarL = ['studyid','domain','usubjid','cmseq','cmtrt','cmdecod','cmstdtc','cmdose','cmdosu']

# Configure attributes
root = Element('ODM')
root.set('xmlns', 'http://www.cdisc.org/ns/odm/v1.3')
root.set('xmlns:data', 'http://www.cdisc.org/ns/Dataset-XML/v1.0')
root.set('FileType', 'Snapshot')
root.set('FileOID', "www.cdisc.org.Studycdisc01-Define-XML_2.0.0(IG.CM)")
root.set('CreationDateTime', "2014-03-20T21:45:33")
root.set('data:DatasetXMLVersion', "1.0.0")

root.append(
    Comment('Dataset CM')
    )
tree = ElementTree(root)
clinicaldata = SubElement(root, 'ClinicalData')
clinicaldata.set('StudyOID', "abc")
clinicaldata.set('MetaDataVersionOID', "MDV.CDISC01.SDTMIG.3.1.2.SDTM.1.2")

def process_rows(l):
  igd = SubElement(clinicaldata, 'ItemGroupData')
  igd.set('ItemGroupOID', "IG.CM")
  igd.set('data:ItemGroupDataSeq', "{}".format(l[0]))

  item = SubElement(igd, 'ItemData')
  item.set('ItemOID', 'IT.STUDYID')
  item.set('Value', df.loc[l[0], 'studyid'])

  item = SubElement(igd, 'ItemData')
  item.set('ItemOID', 'IT.CM.DOMAIN')
  item.set('Value', df.loc[l[0], 'domain'])

  item = SubElement(igd, 'ItemData')
  item.set('ItemOID', 'IT.USUBJID')
  item.set('Value', df.loc[l[0], 'usubjid'])

  item = SubElement(igd, 'ItemData')
  item.set('ItemOID', 'IT.CM.CMSEQ')
  item.set('Value', df.loc[l[0], 'cmseq'])

  test = pd.notna(df.loc[l[0], 'cmtrt'])
  if test == True:
    item = SubElement(igd, 'ItemData')
    item.set('ItemOID', 'IT.CM.CMTRT')
    item.set('Value', df.loc[l[0], 'cmtrt'])

  test = pd.notna(df.loc[l[0], 'cmstdtc'])
  if test == True:
    item = SubElement(igd, 'ItemData')
    item.set('ItemOID', 'IT.CM.CMSTDTC')
    item.set('Value', df.loc[l[0], 'cmstdtc'])

  test = df.loc[l[0], 'cmdose'] != 'nan'
  #print(test)
  if test == True:
    item = SubElement(igd, 'ItemData')
    item.set('ItemOID', 'IT.CM.CMDOSE')
    item.set('Value', df.loc[l[0], 'cmdose'])

  test = pd.notna(df.loc[l[0], 'cmdosu'])
  if test == True:
    item = SubElement(igd, 'ItemData')
    item.set('ItemOID', 'IT.CM.CMDOSU')
    item.set('Value', df.loc[l[0], 'cmdosu'])

[process_rows([i]) for i in df.index]

with open(output_xml_file, 'w') as f:
  try:
    tree.write(f, encoding='unicode')
  finally:
    f.close()
#xml.etree.ElementTree.parse('some.xml')
