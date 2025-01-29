import numpy as np


taulist = open("/home/spandan.sarma/work_ecc/bank_generation/tau0_list.txt", 'r')
size=np.array([])
file_name=np.array([])
#psi42=[]
for aline in taulist.readlines():
    values=aline.split()
    #print(values[4])
    size = np.append(size, float(values[4]))
    file_name = np.append(file_name, values[8])
    #print(values[8])
    
start_values = np.array([])
end_values = np.array([])
for i in np.arange(len(file_name)):
    if i < 288:
        #end_values = np.append(end_values, file_name[i][16:]
        file_name[i] = file_name[i][16:27]

    elif i==288:
        file_name[i] = file_name[i][16:26]

    elif i>288:
        file_name[i] = file_name[i][16:25]
        
        
ls1e3 = np.array([])
ls5e5 = np.array([])
ls1e6 = np.array([])
ls1p25e6 = np.array([])
ls1p5e6 = np.array([])
lsrest = np.array([])
for i in np.arange(len(size)):
    if size[i]<1e3:
        ls1e3 = np.append(ls1e3, file_name[i])

    elif size[i]<5e5:
        ls5e5 = np.append(ls5e5, file_name[i])

    elif size[i]<1e6:
        ls1e6 = np.append(ls1e6, file_name[i])

    elif size[i]<1.25e6:
        ls1p25e6 = np.append(ls1p25e6, file_name[i])

    elif size[i]<1.5e6:
        ls1p5e6 = np.append(ls1p5e6, file_name[i])

    elif size[i]>=1.5e6:
        lsrest = np.append(lsrest, file_name[i])
        
namelist1e3 = np.array([])
namelist5e5 = np.array([])
namelist1e6 = np.array([])
namelist1p25e6 = np.array([])
namelist1p5e6 = np.array([])
namelistrest = np.array([])
for i in ls1e3[::-1]:
    var1 = float(i[:4])
    var2 = float(i[5:])
    namelist1e3 = np.append(namelist1e3, np.arange(var1, var2, 1))

for i in ls5e5[::-1]:
    var1 = float(i[:4])
    var2 = float(i[5:])
    namelist5e5 = np.append(namelist5e5, np.arange(var1, var2, 0.5))

#ls1e6[::-1][:53]
for i in ls1e6[::-1][:53]:
    var1 = float(i[:4])
    var2 = float(i[5:])
    namelist1e6 = np.append(namelist1e6, np.arange(var1, var2, 0.2))

for i in ls1e6[::-1][53:]:
    var1 = float(i[:5])
    var2 = float(i[6:])
    namelist1e6 = np.append(namelist1e6, np.arange(var1, var2, 0.2))

for i in ls1p25e6[::-1][:13]:
    var1 = float(i[:4])
    var2 = float(i[5:])
    namelist1p25e6 = np.append(namelist1p25e6, np.arange(var1, var2, 0.1))

for i in ls1p25e6[::-1][14:]:
    var1 = float(i[:5])
    var2 = float(i[6:])
    namelist1p25e6 = np.append(namelist1p25e6, np.arange(var1, var2, 0.1))

for i in ls1p5e6[::-1]:
    var1 = float(i[:5])
    var2 = float(i[6:])
    namelist1p5e6 = np.append(namelist1p5e6, np.arange(var1, var2, 0.1))

for i in lsrest[::-1]:
    var1 = float(i[:5])
    var2 = float(i[6:])
    namelistrest = np.append(namelistrest, np.arange(var1, var2, 0.1))
    
namelistrest = np.append(namelistrest, np.arange(250, 273, 0.1))



