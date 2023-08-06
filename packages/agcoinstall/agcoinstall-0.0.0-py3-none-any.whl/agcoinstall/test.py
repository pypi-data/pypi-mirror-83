import xml.etree.ElementTree as ET

mytree = ET.parse(r'C:\Program Files (x86)\AGCO Corporation\EDT\EDTUpdateService.exe.config')
myroot = mytree.getroot()


for child in myroot.iter('value'):
    if 'https' in child.text:
        print(child.text)


