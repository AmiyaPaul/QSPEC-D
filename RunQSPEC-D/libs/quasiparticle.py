import numpy as np
import random as rd
import math

import scipy.sparse
from scipy.sparse import csr_matrix , lil_matrix
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigh
from itertools import groupby



class Quasi:
    def __init__(self, 
                 atoms,
                 max_vibronic,
                 config, 
                 atom_dic, 
                 da_dic, 
                 bond_dic, 
                 nbond_dic,
                 da_values, 
                 da_energy, 
                 num_nods, 
                 num_config,
                 sigma,
                 atom_stac_dic,
                 lbonds,
                 one_p, 
                 two_p, 
                 three_p,
                 isdoap_act, 
                 anion_ind,
                 isdis_act, 
                 isda_act,
                 max_eigen,
                 pbc = False,
                 s = 0.0,
                 ):

        self.s = s
        self.atoms = np.array(atoms)
        self.max_vibronic = max_vibronic + 1
        self.isdis_act = isdis_act
        self.isda_act = isda_act
        self.pbc = pbc
        self.config=config

        self.isdoap_act = isdoap_act 
        self.anion_ind = anion_ind

        self.atom_dic = atom_dic
        self.da_dic = da_dic
        self.bond_dic = bond_dic
        self.nbond_dic = nbond_dic

        self.da_values = da_values 
        self.da_energy = da_energy
        self.num_nods = num_nods
        self.num_config = num_config
        self.sigma = sigma
        self.atom_stac_dic = atom_stac_dic
        self.lbonds = lbonds
        self.max_eigen = max_eigen
        
        self.kount = 0
        self.num_particle = 0
        self.kount_1 = 0
        self.kount_2 = 0
        self.kount_3 = 0
        self.kount_4 = 0

        self.one_p = one_p
        self.two_p = two_p
        self.three_p = three_p

        self.ss_disorder_list = None
        self.one_p_list = None
        self.del_site = []




    

    def one_particle(self,if_log):
        if if_log == True:
          one_particle_excitation = []
          for i in self.atoms:
            for v in range(self.max_vibronic):
                one_particle_excitation.append((i, v))

          return one_particle_excitation, len(one_particle_excitation)
        

    def two_particle(self, if_log):
        if if_log == True:
            two_particle_excitation = []
            for i1 in self.atoms:
                for v1 in range(self.max_vibronic):
                    for i2 in self.atoms:
                        for v2 in range(1,self.max_vibronic):
                            if i1 != i2:
                                if v1 + v2 <= self.max_vibronic-1:
                                    two_particle_excitation.append(((i1, v1), ((i2, v2))))

            return two_particle_excitation, len(two_particle_excitation)
        else:
          return None, None

    
    def three_particle(self,iftrue):
        if iftrue:
            three_particle_excitation = []
            for i1 in self.atoms:
                for v1 in range(self.max_vibronic):
                    for i2 in self.atoms:
                        for v2 in range(1,self.max_vibronic):
                            for i3 in self.atoms:
                                for v3 in range(1,self.max_vibronic):
                                    if i1 == i2  or i2 == i3 or i1 == i2:
                                        pass
                                    else:
                                        if v1 + v2 + v3 <= self.max_vibronic-1:
                                            three_particle_excitation.append(((i1, v1),((i2, v2),(i3, v3))))
                                            
            def make_unique(data):
                unique_data = set((pair[0], tuple(sorted(pair[1]))) for pair in data)
                return list(unique_data)

            unique_data = sorted(make_unique(three_particle_excitation), key=lambda x: x[0])
            return unique_data, len(unique_data)
        else:
          return None, None
        
        
    def fcfac(self, n,m):
        if self.max_vibronic-1 == 0:
            ss = 0
        else:
            ss = self.s
        fc = 0
        for k in range(0,m+1):
            if (n-m+k) >= 0:
                f_mk = math.factorial(m-k)
                f_nmk = math.factorial(n-m+k)
                f_k = math.factorial(k)
                facin = 1.0/(f_k*f_mk*f_nmk)

                fc = fc + facin * ss**(k/2) * ss**((n-m+k)/2) * (-1)**(n-m+k)

            else:
                pass

        f_n = math.factorial(n)
        f_m = math.factorial(m)
        fc = fc * math.sqrt(f_m * f_n) * math.exp(-ss/2)
        
        return fc
    
    
    def fc_gf(self):
        fc_gf_list = np.zeros([self.max_vibronic,self.max_vibronic])
        for i in range(0,self.max_vibronic):
            for j in range(0,self.max_vibronic):
                fc_gf_list[i,j] = self.fcfac(i, j)
        self.fc_gf_list = fc_gf_list
        return self


    
    
    def get_j(self, pa1, pa2):
        bval = list(self.bond_dic.keys())
        nbval = list(self.nbond_dic.keys())

        j_val = 0
        
        if str(pa1) in bval:
            if pa2 in self.bond_dic[f"{pa1}"]:
                if self.isda_act:
                    if (self.da_dic[f"{pa1}"] == 1 and self.da_dic[f"{pa2}"] == -1) or (self.da_dic[f"{pa1}"] == -1 and self.da_dic[f"{pa2}"] == 1):
                        j_val = self.da_values[2][0]
                    elif (self.da_dic[f"{pa1}"] == 1 and self.da_dic[f"{pa2}"] == 1):
                        j_val = self.da_values[0][0]
                    elif (self.da_dic[f"{pa1}"] == -1 and self.da_dic[f"{pa2}"] == -1):
                        j_val = self.da_values[1][0]
                else:
                    j_val = self.da_values[0][0]

        if str(pa1) in nbval:
            if pa2 in self.nbond_dic[f"{pa1}"]:
                if self.isda_act:
                    if (self.da_dic[f"{pa1}"] == 1 and self.da_dic[f"{pa2}"] == -1) or (self.da_dic[f"{pa1}"] == -1 and self.da_dic[f"{pa2}"] == 1):
                        j_val = self.da_values[2][1]
                    elif (self.da_dic[f"{pa1}"] == 1 and self.da_dic[f"{pa2}"] == 1):
                        j_val = self.da_values[0][1]
                    elif (self.da_dic[f"{pa1}"] == -1 and self.da_dic[f"{pa2}"] == -1):
                        j_val = self.da_values[1][1]
                else:
                    j_val = self.da_values[0][1]

        return j_val


        
    def hamiltonian_1p_1p(self, iftrue, array):
        if iftrue:
            array_1p, _ = self.one_particle(iftrue)
            for i in range(len(array_1p)):
                for j in range(i, len(array_1p)):
                    part1 = array_1p[i]
                    part2 = array_1p[j]
                    if part1[0] == part2[0]:
                        if part1[1] == 0 and part2[1] == 0:
                            pass
                        elif part1[1] != part2[1]:
                            pass
                        else:
                            array[i,j] = part1[1]
                    else:
                        coupling = self.eV_to_quanta(self.get_j(part1[0],part2[0]) * self.fc_gf_list[0,part2[1]] * self.fc_gf_list[0, part1[1]])
                        if coupling != 0:
                            array[i, j] = coupling
                            array[j, i] = coupling

        
    def hamiltonian_2p_2p(self, iftrue, array, ini):
        if iftrue:
            array_2p, _ = self.two_particle(iftrue)
            for i in range(0, len(array_2p)):
                for j in range(i, len(array_2p)):
                    part1 = array_2p[i]
                    part2 = array_2p[j]
                    if part1[0][0] == part2[0][0]:
                        if part1 == part2:
                            array[ini+i, ini+j] = part1[0][1] + part1[1][1]
                    else:
                        if (part1[1][0] != part2[0][0] and part1[1][0] != part2[1][0]) or (part2[1][0] != part1[0][0] and part2[1][0] != part1[1][0]):
                            pass
                        elif part1[1][0] == part2[1][0]:
                            if part1[1][1] != part2[1][1]:
                                pass
                            else:
                                coupling = self.eV_to_quanta(self.get_j(part1[0][0],part2[0][0]) * self.fc_gf_list[0,part1[0][1]] * self.fc_gf_list[0,part2[0][1]])
                                if coupling != 0:
                                    array[ini+i, ini+j] = coupling
                                    array[ini+j, ini+i] = coupling
                        else:
                            coupling = self.eV_to_quanta(self.get_j(part1[0][0],part2[0][0]) * self.fc_gf_list[part2[1][1],part1[0][1]] * self.fc_gf_list[part1[1][1],part2[0][1]])
                            if coupling != 0:
                                array[ini+i, ini+j] = coupling
                                array[ini+j, ini+i] = coupling
                     


    def hamiltonian_1p_2p(self, iftrue, array):
        if iftrue:
            array_1p, _ = self.one_particle(iftrue)
            array_2p, _ = self.two_particle(iftrue)
            for i in range(len(array_1p)):
                for j in range(len(array_2p)):
                    part1 = array_1p[i]
                    part2 = array_2p[j]
                    if part1[0] == part2[0][0]:
                        pass
                    else:
                        for k in part2:
                            if part1[0] != k[0]:
                                pass
                            else:
                                coupling = self.eV_to_quanta(self.get_j(part1[0], part2[0][0]) * self.fc_gf_list[part2[1][1],part1[1]] * self.fc_gf_list[0, part2[0][1]])
                                if coupling != 0:
                                    array[i, len(array_1p)+j] = coupling
                                    array[len(array_1p)+j, i] = coupling

    def eV_to_quanta(self, val):
        return val * 8065 / 1400
                
    def construct_hamiltonian(self, one_p, two_p, three_p=False, four_p=False):
        array_1p, kount_1p = self.one_particle(one_p)
        array_2p, kount_2p = self.two_particle(two_p)
        array_3p, kount_3p = self.three_particle(three_p)
        self.array_1p = array_1p
        self.array_2p = array_2p
        self.array_3p = array_3p

        mat_len = 0
        if one_p:
            mat_len += len(array_1p)
            print('Number of one particle excitation - ', len(array_1p))
        if two_p:
            mat_len += len(array_2p)
            print('Number of two particle excitation - ', len(array_2p))
        if three_p:
            mat_len += len(array_3p)
            print('Number of three particle excitation - ', len(array_3p))
        self.mat_len = mat_len

        print(f'Dimension of Hamiltonian is {self.mat_len} X {self.mat_len}')

        Hamiltonian_lil = lil_matrix((mat_len, mat_len), dtype=np.float32)

        if one_p == True:
            self.hamiltonian_1p_1p(True, Hamiltonian_lil)

        if two_p == True:
            if one_p == False:
                ini, fin = 0, len(array_2p)
            else:
                ini, fin = len(array_1p), len(array_1p)+len(array_2p)
            self.hamiltonian_2p_2p(True, Hamiltonian_lil, ini)

        if one_p == True and two_p == True:
            self.hamiltonian_1p_2p(True, Hamiltonian_lil)

        return Hamiltonian_lil.tocsr()


    def find_particle(self, part):
        crd = self.atom_dic[f"{part}"]
        cval = self.atom_stac_dic[f"{part}"]
        a1 = crd[0] / self.lbonds
        a2 = crd[1] / self.lbonds
        
        return (a1, a2, cval)



    def SS_disorder(self, config, array):

        if self.ss_disorder_list is None:
            self.one_p_list = self.one_particle(self.one_p)[0]
            self.two_p_list = self.two_particle(self.two_p)[0]
            self.three_p_list = self.three_particle(self.three_p)[0]
            self.ss_disorder_list = np.random.normal(0, self.sigma, self.num_config * len(self.atoms)).reshape([self.num_config, len(self.atoms)]) *8065/1400
            

        dis = self.ss_disorder_list[config]

        dis_arr = []
        if self.one_p:
            for i in range(len(self.array_1p)):
                dis_arr.append(dis[self.array_1p[i][0]-1])

            if self.two_p:
                for i in range(len(self.array_2p)):
                    dis_arr.append(dis[self.array_2p[i][0][0]-1])

                if self.three_p:
                    for i in range(len(self.array_3p)):
                        dis_arr.append(dis[self.array_3p[i][0][0]-1])

        array_lil = array.tolil()
        for i in range(array.shape[0]):
            array_lil[i, i] += dis_arr[i]
        return array_lil.tocsr()
    

    def add_DA(self, array):
        if self.one_p_list is None:
            self.one_p_list = self.one_particle(self.one_p)[0]
            self.two_p_list = self.two_particle(self.two_p)[0]
            self.three_p_list = self.three_particle(self.three_p)[0]

        DA_arr = []
        if self.one_p:
            for i in range(len(self.array_1p)):
                a = self.da_dic[f"{self.array_1p[i][0]}"]
                DA_arr.append(a)

            if self.two_p:
                for i in range(len(self.array_2p)):
                    a = self.da_dic[f"{self.array_2p[i][0][0]}"]
                    DA_arr.append(a)

                if self.three_p:
                    for i in range(len(self.array_3p)):
                        a = self.da_dic[f"{self.array_3p[i][0][0]}"]
                        DA_arr.append(a)

        array_lil = array.tolil()
        for i in range(array.shape[0]):
            array_lil[i, i] += self.da_energy * DA_arr[i] * 8065 / 1400

        
        return array_lil.tocsr()
    



    def calc_dis_doaping(self, part):
        x, y = self.atom_dic[f"{part}"]
        z = (int(self.atom_stac_dic[f"{part}"]) - 1) * self.lbonds
        distance_doaping = np.sqrt((x - self.anion_ind[0])**2 + 
                                       (y - self.anion_ind[1])**2 +
                                       (z - self.anion_ind[2])**2, dtype=np.float32)
        return distance_doaping
            


    def doaping_distance_table_gen(self):
        if self.one_p_list is None:
            self.one_p_list = self.one_particle(self.one_p)[0]
            self.two_p_list = self.two_particle(self.two_p)[0]
            self.three_p_list = self.three_particle(self.three_p)[0]
        doping_arr = []
        if self.one_p:
            for a in self.one_p_list:
                doping_arr.append(self.calc_dis_doaping(a[0]))

            if self.two_p:
                for a in self.two_p_list:
                    doping_arr.append(self.calc_dis_doaping(a[0][0]))

                if self.three_p:
                    for a in self.three_p_list:
                        doping_arr.append(self.calc_dis_doaping(a[0][0]))
        return -8.3/np.array(doping_arr, dtype=np.float32).T
    
    def doaping_activate(self, array):
        try:
            self.doaping_array
        except:
             self.doaping_array = self.doaping_distance_table_gen()

        array_lil = array.tolil()
        for i in range(array.shape[0]):
            array_lil[i, i] += self.doaping_array[i]
        return array_lil.tocsr()

    # def bond_missing_active(self, array, bond_missing):
    #     bonds = [[],[]]
    #     bkeys = list(self.bond_dic.keys())
    #     nbkeys = list(self.nbond_dic.keys())
    #
    #     for i in bkeys:
    #         for j in self.bond_dic[i]:
    #             bar = (int(i), j)
    #             abar = (min(bar), max(bar))
    #             if abar not in bonds[0]:
    #                 bonds[0].append(abar)
    #
    #     for i in nbkeys:
    #         for j in self.nbond_dic[i]:
    #             bar = (int(i), j)
    #             abar = (min(bar), max(bar))
    #             if abar not in bonds[1]:
    #                 bonds[1].append(abar)
    #
    #     bnd_mis_arr = rd.sample(bonds[0], bond_missing[0])
    #     nbnd_mis_arr = rd.sample(bonds[1], bond_missing[1])
    #     del_ind = []
    #     if self.one_p:
    #         for a in range(len(self.array_1p)):
    #             for b in range(len(self.array_1p)):
    #                 arr = (min([self.array_1p[a][0], self.array_1p[b][0]]), max([self.array_1p[a][0], self.array_1p[b][0]]))
    #                 if arr in bnd_mis_arr:
    #                     del_ind.append((a, b))
    #                 if arr in nbnd_mis_arr:
    #                     del_ind.append((a, b))
    #
    #
    #         if self.two_p:
    #             for a in self.array_2p:
    #                 doping_arr.append(self.calc_dis_doaping(a[0][0]))
    #
    #             if self.three_p:
    #                 for a in self.array_3p:
    #                     doping_arr.append(self.calc_dis_doaping(a[0][0]))
    #
    #
    #
    #
    #
    #
    #
    #
    #     return array



    def site_missing_active(self, array, site_missing):
        self.del_site = list(rd.sample(list(self.atoms), site_missing))
        # self.del_site = [3, 10]
        b_miss = []
        nb_miss = []

        for i in self.del_site:
            for j in self.bond_dic[f"{i}"]:
                arr = (min([i, j]), max([i, j]))
                if arr not in b_miss:
                    b_miss.append(arr)

            for j in self.nbond_dic[f"{i}"]:
                arr = (min([i, j]), max([i, j]))
                if arr not in nb_miss:
                    nb_miss.append(arr)

        ind = []
        if self.one_p:
            for a in range(len(self.array_1p)):
                for i in self.del_site:
                    if i == self.array_1p[a][0]:
                        ind.append(a)

            if self.two_p:
                for a in range(len(self.array_2p)):
                    for i in self.del_site:
                        if i == self.array_2p[a][0][0] or i == self.array_2p[a][1][0]:
                            ind.append(len(self.array_1p)+a)

                if self.three_p:
                    for a in range(len(self.array_3p)):
                        for i in self.del_site:
                            if i == self.array_3p[a][0][0]:
                                ind.append(len(self.array_1p) + a)

        unique_sorted_numbers = sorted(set(ind))
        chunks = []
        for k, g in groupby(enumerate(unique_sorted_numbers), lambda x: x[1] - x[0]):
            group = [num for _, num in g]
            chunks.append((group[0], group[-1]))

        new_array = array.copy()
        consum = 0
        for ara in chunks:
            new_array = scipy.sparse.vstack([new_array[: (ara[0] - consum)], new_array[(ara[1] + 1 - consum) :]])
            new_array = scipy.sparse.hstack([new_array[:, : (ara[0] - consum)], new_array[:, (ara[1] + 1 - consum) :]])
            consum += ara[1] + 1 - ara[0]

        return new_array
















    def cms_osc(self, array, max_eigen, one_p, two_p, three_p):  
        if max_eigen < array.shape[0]:
            self.eigval, self.eigvec = eigsh(array, k=max_eigen, which="SA")
            self.max_eigen = max_eigen
        else:
            self.eigval, self.eigvec = eigh(array.toarray())
            self.max_eigen = array.shape[0]

        f_ex = []
        for i in range(1, self.max_eigen):
            tem_x = 0
            tem_y = 0
            tem_z = 0


            if one_p == True and two_p == False:
                cnt = 0
                for j in range(0,len(self.array_1p)):
                    if self.array_1p[j][0] not in self.del_site:
                        a, b, c = self.find_particle(self.array_1p[j][0])
                        tem_x += (a+1) * (self.eigvec[cnt][0] * self.eigvec[cnt][i])
                        tem_y += (b+1) * (self.eigvec[cnt][0] * self.eigvec[cnt][i])
                        tem_z += (c+1) * (self.eigvec[cnt][0] * self.eigvec[cnt][i])
                        cnt += 1
                    
            elif one_p == True and two_p == True:
                cnt = 0
                for j in range(0,len(self.array_1p)):
                    if self.array_1p[j][0] not in self.del_site:
                        a, b, c = self.find_particle(self.array_1p[j][0])
                        tem_x += (a + 1) * (self.eigvec[cnt][0] * self.eigvec[cnt][i])
                        tem_y += (b + 1) * (self.eigvec[cnt][0] * self.eigvec[cnt][i])
                        tem_z += (c + 1) * (self.eigvec[cnt][0] * self.eigvec[cnt][i])
                        cnt += 1
                for k in range(0,len(self.array_2p)):
                    if (self.array_2p[k][0][0] not in self.del_site) and (self.array_2p[k][1][0] not in self.del_site):
                        a, b, c = self.find_particle(self.array_2p[k][0][0])
                        tem_x += (a+1) * (self.eigvec[cnt][0] * self.eigvec[cnt][i])
                        tem_y += (b+1) * (self.eigvec[cnt][0] * self.eigvec[cnt][i])
                        tem_z += (c+1) * (self.eigvec[cnt][0] * self.eigvec[cnt][i])
                        cnt += 1


            osc_x = tem_x**2
            osc_y = tem_y**2
            osc_z = tem_z**2
            f_ex.append([osc_x, osc_y, osc_z])
        return np.array(f_ex)
    

    def cms_osc_sum(self, f_ex):
        sum_x = 0
        sum_y = 0
        sum_z = 0
        for i in range(1, self.max_eigen):
            del_e = self.eigval[i] - self.eigval[0]
            sum_x += del_e * f_ex[i-1][0]
            sum_y += del_e * f_ex[i-1][1]
            sum_z += del_e * f_ex[i-1][2]

        return [sum_x, sum_y, sum_z]

    def cms_spec(self, spec_step, gamma, f_ex, lorentzian=False):
        ab = np.zeros((3, spec_step))
        gamma /= 1400
        spec_range = np.linspace(0, 20000/1400, spec_step)

        del_e = self.eigval[1:self.max_eigen] - self.eigval[0]

        for k, energy in enumerate(spec_range):
            if lorentzian:
                lineshape = gamma / ((energy - del_e) ** 2 + gamma ** 2) / np.pi
            else:
                lineshape = np.exp(-((energy - del_e) / gamma) ** 2) / (np.sqrt(np.pi) * gamma)

            ab[:, k] = np.dot(f_ex.T, lineshape * del_e)

        return ab

    def cms_out(self, arr, spec_step, task_title="job_inf"):
        ab_x = arr[0]
        ab_y = arr[1]
        ab_z = arr[2]

        file = open(f"{task_title}.dat","w")
        file.write(f"Task Title: {task_title}\n")
        file.write('CMS Data\n')
        file.write('Energy CMS CMS \n')
        file.write(' cm\+(-1) a.u. a.u. a.u. \n')
        file.write(' n.a. sum x y z\n')
        spec_start = 0
        spec_end = spec_start + spec_step/1400

        for k in range(1,spec_step+1):
            energy = spec_start + k/spec_step * (spec_end-spec_start)
            file.write(f"{energy:.7f} {(ab_x[k-1] + ab_y[k-1] + ab_z[k-1]):.7f} {ab_x[k-1]:.7f} {ab_y[k-1]:.7f} {ab_z[k-1]:.7f}\n")

        file.close()

    





    





        


                  







                            







