import os,re
def calculate_blinddocking_box(receptor):
    excludes = ['ATOM','HETATM']
    x_list=[]
    y_list=[]
    z_list=[]
    xyz=[]
    for line in open(receptor, "r", encoding='UTF-8'):
        if any(e in line for e in excludes) and line[13]!='H':
            x_list.append(re.search(r'-?\d+\.?\d*e?-?\d*?', line[30:38])[0])
            y_list.append(re.search(r'-?\d+\.?\d*e?-?\d*?', line[38:46])[0])
            z_list.append(re.search(r'-?\d+\.?\d*e?-?\d*?', line[46:54])[0])
    x_list=[float(i) for i in x_list]
    y_list = [float(j) for j in y_list]
    z_list = [float(k) for k in z_list]
    x_list.sort()
    x_max=x_list[-1]
    x_min=x_list[0]
    y_list.sort()
    y_max=y_list[-1]
    y_min=y_list[0]
    z_list.sort()
    z_max=z_list[-1]
    z_min=z_list[0]
    xyz.append(round((x_max+x_min)/2,3))
    xyz.append(round((y_max+y_min)/2,3))
    xyz.append(round((z_max+z_min)/2,3))
    xyz.append(round((x_max-x_min)*1.05,3))
    xyz.append(round((y_max-y_min)*1.05,3))
    xyz.append(round((z_max-z_min)*1.05,3))
    return xyz

path=input("Please enter the path containing all the receptor files in format '.pdbqt':")
configpath=input("Please enter the path where the config files will be saved:")
allfiles=os.listdir(path)
allreceptors=[]
for file in allfiles:
    if file.endswith('.pdbqt'):
        allreceptors.append(file)
for receptor in allreceptors:
    blinddocking_box=calculate_blinddocking_box(path+os.path.sep+receptor)
    configfile=open(configpath+os.path.sep+receptor[:-6]+'.txt','w')
    configfile.write('center_x=%s\ncenter_y=%s\ncenter_z=%s\nsize_x=%s\nsize_y=%s\nsize_z=%s\nexhaustiveness=16\nnum_modes=9\nenergy_range=5\n'%(
        blinddocking_box[0],blinddocking_box[1],blinddocking_box[2],blinddocking_box[3],blinddocking_box[4],blinddocking_box[5]))
    configfile.close()
print('done')
