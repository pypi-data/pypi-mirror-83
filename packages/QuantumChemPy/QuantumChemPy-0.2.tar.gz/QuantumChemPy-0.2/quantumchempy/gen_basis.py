import numpy as np

def Gen_Ans(molecule,orbital,An=2,star=True):
    """
    Función para generar Gen-An y Gen-An* bases auxiliares.
      Se asume lo siguiente:
        molecule: es un objeto que puede regresar el número de átomos con molecule.natoms()
        y la carga del i-ésimo átomo con molecule.Z(i).
        orbital: es un objeto que puede regresar cuantos shells hay en el i-ésimo átomo con
        orb.nshell_on_center(i), a su vez puede regresar el j-ésimo shell con orbital.shell(j).
        El objeto tipo shell puede regresar el número de primitivas con shell.nprimitive y el 
        k-ésimo exponente con shell.exp(k)

    Regresa
      Un string con la base auxiliar generada.
    """

    aux_basis = ""

    elements = ['H','He',
            'Li','Be','B','C','N','O','F','Ne',
            'Na','Mg','Al','Si','P','S','Cl','Ar']
    elem = [False for i in range(len(elements))]
    angular = ['S','P','D','F','G','H','I']

    aux_basis += "cartesian\n"

    natom = molecule.natom()

    ishell = 0
    for iatom in range(natom):

        nshell_on_center = orbital.nshell_on_center(iatom)

        if(not elem[int(molecule.Z(iatom)-1)]):
    
            elem[int(molecule.Z(iatom)-1)] = True
    
            aux_basis += "****\n"
            aux_basis += '{:s}    0\n'.format(elements[int(molecule.Z(iatom)-1)])
    
            maxexp = 0
            for jshell in range(nshell_on_center):
                shell = orbital.shell(ishell+jshell)
                nprim = shell.nprimitive
                for iprim in range(nprim):
                    maxexp = max(maxexp,shell.exp(iprim))
            minexp = maxexp
            for jshell in range(nshell_on_center):
                shell = orbital.shell(ishell+jshell)
                nprim = shell.nprimitive
                for iprim in range(nprim):
                    minexp = min(minexp,shell.exp(iprim))            

            r = 6.0 - An
    
            nblock = 2
            if(star):
                nblock = nblock + 1
    
#   H and He
            if (molecule.Z(iatom)<=2):
                r = r - 0.5*An + 2.0
                nblock = nblock - 1

#   How many z?
            N = int(np.log(maxexp/minexp)/np.log(r) + 0.5)

            maxexp = minexp*r**(N-1)
            maxexp = 2.0*maxexp

            tmpexp = maxexp*r
  
            for iblock in range(1,nblock+1):
                if (iblock == 1):
                    nauxis = int(max(1,N/nblock + N%nblock))
                else:
                    nauxis = int(max(1,N/nblock))
                for ifa in range(1,nauxis+1):
                    tmpexp = tmpexp/r
                    if (ifa == 1):
                        tmpexp = tmpexp*(r+0.5*An)/r
                    for L in range(0,2*(iblock-1)+1):
                        aux_basis += '{:s}   1   1.0\n'.format(angular[L])
                        aux_basis += '      {:11f}           1.0000000\n'.format(tmpexp)
                    if (ifa == 1):
                        tmpexp = tmpexp*r/(r+0.5*An)    
            
        ishell = ishell + nshell_on_center  
    aux_basis += "****"

    return aux_basis
