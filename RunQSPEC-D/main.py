
import numpy as np
from libs.quasiparticle import *
from multiprocessing import Pool
import time
import os
from tqdm import tqdm

name = "st5"
with open(f"{name}.qp", 'r') as infile:
    data = infile.read()

file = data.split("             ")
gs_ar = file[0].split("\n")[3:-1]
calc_infos = file[1].split("\n")[4:-1]
coordinates = file[2].split("\n")[4:-1]
bondings = file[3].split("\n")[4:-1]
dis_info = file[4].split("\n")[4:-1]
da_info = file[5].split("\n")[4:-1]
doaping_info = file[6].split("\n")[4:-1]




grid_s = gs_ar[0].split(" ")
grid_s = int([item for item in grid_s if item != ''][-1])

atom_rad = gs_ar[1].split(" ")
atom_rad = int([item for item in atom_rad if item != ''][-1])

lbonds = gs_ar[2].split(" ")
lbonds = float([item for item in lbonds if item != ''][-1])


nparticles = calc_infos[0].split(" ")
nparticles = int([item for item in nparticles if item != ''][-1])

nbonds = calc_infos[1].split(" ")
nbonds = [item for item in nbonds if item != ''][-1]
nbonds = [int(i) for i in nbonds.split("-")]

max_vib = calc_infos[2].split(" ")
max_vib = int([item for item in max_vib if item != ''][-1])

aparticle = calc_infos[3].split(" ")
aparticle = [item for item in aparticle if item != ''][-2]



atoms = []
da_dic = {}
atom_dic = {}
atom_stac_dic = {}

for text in coordinates:
    text_l = text.split(" ")
    text_l = [item for item in text_l if item != '']
    
    atoms.append(int(text_l[0]))
    da_dic[f"{text_l[0]}"] = 1 if text_l[1] == "D" else -1
    atom_dic[f"{text_l[0]}"] = (float(text_l[2]), float(text_l[3]))
    atom_stac_dic[f"{text_l[0]}"] = int(text_l[-1])

bfind = bondings.index('')
b_inter = bondings[ : bfind]
nb_inter = bondings[(bfind+1) : ]

bond_dic = {}
nbond_dic = {}

for text in b_inter:
    text_l = text.split(" ")
    text_l = [int(item) for item in text_l if item != '']

    bond_dic[f"{text_l[0]}"] = text_l[1:]

for text in nb_inter:
    text_l = text.split(" ")
    text_l = [int(item) for item in text_l if item != '']

    nbond_dic[f"{text_l[0]}"] = text_l[1:]
 


isdis_act = dis_info[0].split(" ")
isdis_act = [item for item in isdis_act if item != ''][-1]
isdis_act = True if isdis_act == "TRUE" else False

num_nods = dis_info[1].split(" ")
num_nods = int([item for item in num_nods if item != ''][-1])

num_config = dis_info[2].split(" ")
num_config = int([item for item in num_config if item != ''][-1])

sigma = dis_info[3].split(" ")
sigma = float([item for item in sigma if item != ''][-1])

issite_missing = dis_info[4].split(" ")
issite_missing = [item for item in issite_missing if item != ''][-1]
issite_missing = True if issite_missing == "TRUE" else False

site_missing = dis_info[5].split(" ")
site_missing = int([item for item in site_missing if item != ''][-1])

isbond_missing = dis_info[6].split(" ")
isbond_missing = [item for item in isbond_missing if item != ''][-1]
isbond_missing = True if isbond_missing == "TRUE" else False

bond_missing = []
b_m = dis_info[7].split(" ")
bond_missing.append(int([item for item in b_m if item != ''][-2]))
bond_missing.append(int([item for item in b_m if item != ''][-1]))





isda_act = da_info[0].split(" ")
isda_act = [item for item in isda_act if item != ''][-1]
isda_act = True if isda_act == "TRUE" else False


da_values = []
for text in da_info[1:-1]:
    text_l = text.split(" ")
    text_l = [item for item in text_l if item != '']
    da_values.append((float(text_l[-2]), float(text_l[-1])))

da_energy = da_info[-1].split(" ")
da_energy = float([item for item in da_energy if item != ''][-1])


isdoap_act = doaping_info[0].split(" ")
isdoap_act = [item for item in isdoap_act if item != ''][-1]
isdoap_act = True if isdoap_act == "TRUE" else False

anion_ind = []
for text in doaping_info[1:]:
    text_l = text.split(" ")
    text_l = [item for item in text_l if item != '']
    if text_l[-1] != "None":
        anion_ind.append(float(text_l[-1]))
    else:
        anion_ind.append(None)






if aparticle == "One":
    one_p = True
    two_p = False
    three_p = False
elif aparticle == "Two":
    one_p = True
    two_p = True
    three_p = False
elif aparticle == "Three":
    one_p = True
    two_p = True
    three_p = True


spec_step = 20000
abs_lw = 350

max_eigen = 1000

system = Quasi(atoms, max_vib, num_config, atom_dic, da_dic, bond_dic, nbond_dic, 
               da_values, da_energy, num_nods, num_config, sigma, atom_stac_dic, lbonds,
               one_p, two_p, three_p, isdoap_act, anion_ind,
               isdis_act = isdis_act, isda_act = isda_act, max_eigen = max_eigen, pbc=False, s=1.0)

system.fc_gf()



hs_t = time.time()
Hamiltonian = system.construct_hamiltonian(one_p, two_p, three_p)
#print(system.array_1p)


def printHamil(array):
    arra = array.toarray()
    with open("myHamil.txt", "w") as file:
        for i in range(Hamiltonian.shape[0]):
	        txt = ""
	        for j in range(Hamiltonian.shape[0]):
	            if Hamiltonian[i, j] != 0:
	                txt += f"({j}, {Hamiltonian[i, j]:.5f}) "
	        if txt != "":
	            file.write(f"row {i}: {txt}\n")
#printHamil(Hamiltonian)
he_t = time.time()

#print(system.calc_dis_doaping(1))


def run(n_config):
    print(f'Process {n_config} has started.\n')
    ps_t = time.time()
    array = Hamiltonian.copy()

    if isdis_act:
        array = system.SS_disorder(n_config, array)

    if isda_act:
        array = system.add_DA(array)

    if isdoap_act:
        array = system.doaping_activate(array)

    # if isbond_missing:
    #     array = system.bond_missing_active(array, bond_missing)

    if issite_missing:
        array = system.site_missing_active(array, site_missing)

    f_ex = system.cms_osc(array, max_eigen, one_p, two_p, three_p)
    cms_osc_sum_arr = system.cms_osc_sum(f_ex)
    ab_s = system.cms_spec(spec_step, abs_lw, f_ex, lorentzian=False)
    pe_t = time.time()
    print(f'Process {n_config} has ended. Time taken {pe_t-ps_t}\n')
    return ab_s

def update_progress(_):
    progress_bar.update()


if __name__ == '__main__':
    configs = [i for i in range(num_config)]
    arr = np.zeros([3, spec_step])

    with tqdm(total=num_config) as progress_bar:
        with Pool(processes=num_nods) as pool:
            results = [pool.apply_async(run, args=(config,), callback=update_progress) for config in configs]
            pool.close()
            pool.join()

        for result in results:
            ab_s = result.get()
            arr[0] += ab_s[0]
            arr[1] += ab_s[1]
            arr[2] += ab_s[2]

    arr = arr / num_config
    # title = f"{sys1.x_dim}-{sys1.y_dim}-{sys1.z_dim}-{sys1.max_vibronic-1}-{sys1.config}"
    system.cms_out(arr, spec_step, task_title=name)

    


