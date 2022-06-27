import os,re
import pandas as pd

def calculate_distance(line,x,y,z):
    receptor_x=float(re.findall(r'-?\d+\.?\d*e?-?\d*?', line[30:38])[0])
    receptor_y=float(re.findall(r'-?\d+\.?\d*e?-?\d*?', line[38:46])[0])
    receptor_z=float(re.findall(r'-?\d+\.?\d*e?-?\d*?', line[46:54])[0])
    for i in range(len(x)):
        distance=((receptor_x-float(x[i]))**2+(receptor_y-float(y[i]))**2+(receptor_z-float(z[i]))**2)**0.5
        if distance<4.5:
            return re.findall(r'[A-Z]{3}',line[17:22])[0]


def calculate_ratio(aminoacid):
    aminoacid_ratio={'ALA':1.077645,'ARG':0.756287,'ASN':0.944213,'ASP':1.103226,'CYS':1.224506,'GLN':0.780122,'GLU':0.767545,'GLY':1.210283,'HIS':0.904045,'ILE':1.261891,
               'LEU':1.107638,'LYS':0.825124,'MET':1.221941,'PHE':1.082683,'PRO':0.668084,'SER':0.877358,'THR':0.883335,'TRP':1.098844,'TYR':1.082018,'VAL':1.117822}
    # The preference factor for type x amino acid calculated from our dataset
    total=0
    for i in aminoacid:
        total+=aminoacid[i]
    if total!=0:
        for j in aminoacid_ratio:
            aminoacid_ratio[j]=round(aminoacid[j]*aminoacid_ratio[j]/total,3)
    return aminoacid_ratio

def calculate_preference(receptor,ligand):
    aminoacid={'ALA':0,'ARG':0,'ASN':0,'ASP':0,'CYS':0,'GLN':0,'GLU':0,'GLY':0,'HIS':0,'ILE':0,
               'LEU':0,'LYS':0,'MET':0,'PHE':0,'PRO':0,'SER':0,'THR':0,'TRP':0,'TYR':0,'VAL':0}
    ligand_x=[]
    ligand_y=[]
    ligand_z=[]
    for line in open(ligand, "r", encoding='UTF-8'):
        if any(e in line for e in ['ATOM','HETATM']) and line[13] != "H":
            ligand_x.extend(re.findall(r'-?\d+\.?\d*e?-?\d*?', line[30:38]))
            ligand_y.extend(re.findall(r'-?\d+\.?\d*e?-?\d*?', line[38:46]))
            ligand_z.extend(re.findall(r'-?\d+\.?\d*e?-?\d*?', line[46:54]))
    for line in open(receptor, "r", encoding='UTF-8'):
        if any(e in line for e in ['ATOM']) and line[13] != "H":
            one=calculate_distance(line,ligand_x,ligand_y,ligand_z)
            if one!=None:
                aminoacid[one]=aminoacid[one]+1
    return aminoacid,calculate_ratio(aminoacid)

receptor=input("Please enter the receptor file(.pdbqt):")
ligandpath=input("Please enter the path where all the docking conformations are saved:")
outputpath=input("Please enter the path where the result will be saved(aminoacid_preference.csv):")
ligand_list=os.listdir(ligandpath)
ligandlist=[]
for i in ligand_list:
    if i.endswith('.pdbqt'):
        ligandlist.append(i)
result={}
for ligand in ligandlist:
    oneligand=ligandpath+os.path.sep+ligand
    aminoacid_ratio=calculate_preference(receptor,oneligand)[1]
    result.setdefault(ligand[:-6],aminoacid_ratio)
result_df=pd.DataFrame(result)
result_ratio_T= pd.DataFrame(result_df.values.T, index=result_df.columns, columns=result_df.index)
result_ratio_T.to_csv(outputpath+os.path.sep+'aminoacid_preference.csv')

print('done')