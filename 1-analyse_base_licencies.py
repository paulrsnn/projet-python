import numpy as np
import pandas as pd
import seaborn as sns
import pyproj
import fiona
import geopandas

lic_comm = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/1825fde3-a668-47e3-a46d-b62b5af6560a", encoding = 'Latin-1', sep = ';')

lic_comm.head(5)


lic_comm.columns

lic_comm.dtypes
lic_comm['fed_2019'].astype(str)
lic_comm.dtypes

lic_comm['code_commune'].nunique() #34893 communes
lic_comm['region'].nunique() #18 regions
lic_comm['fed_2019'].nunique() #99 identifiants de federation
lic_comm['nom_fed'].unique()
lic_comm['nom_fed'].nunique() #99

lic_comm['l_f_2019'].dtypes
lic_comm.isnull().sum()
lic_comm['l_h_2019'].astype(int)
lic_comm[['code_commune', 'l_2019']].groupby('code_commune').sum() 
#La base lic_comm regroupée par commune : cela donne le nb de licenciés 
# par commune pour chaque sport
lic_comm.dtypes
lic_comm[['region', 'l_2019']].groupby('region').sum().sort_values(by = 'l_2019', ascending = False)

lic_comm[['libelle', 'l_2019']].groupby('libelle').sum().sort_values(by = 'l_2019', ascending = False) #On groupe la base par les libelles : cela donne

lic_comm[lic_comm['code_commune'] == 75101]

lic_comm.columns

sorted(a, key = 'l_2019')


# Pour simplifier l'analyse et la représentation graphique, faudrait transposer colonnes en ligne (ajouter une colonne sexe, tranche d'age...) 
# pour réduire le nb de colonnes et faire stats par groupe. => utiliser fonction .pivot ou melt

# Statistiques par régions :
 #Pourcentage de licencies dans chaque sport par région

# Sports les plus pratiqués en France par région

lic_comm[['region', 'nom_fed', 'l_2019']].groupby(['region', 'nom_fed']).sum().sort_values(by = 'l_2019', ascending = False).head(10)

lic_comm[['region', 'nom_fed', 'l_2019']].groupby(['region', 'nom_fed']).sum().sort_values(by = 'l_2019', ascending = False).tail(20)
# On pourrait : ajouter stats par depart comme on a le code commune pour affiner


# Sports les plus pratiqués en France par sexe
f = lic_comm[['nom_fed', 'l_f_2019']].groupby(['nom_fed']).sum().sort_values(by = 'l_f_2019', ascending = False).head(20)

f.head()

lic_comm[['nom_fed', 'l_f_2019', 'l_h_2019']].groupby(['nom_fed']).sum().sort_values(by = 'l_h_2019', ascending = False).head(20)

#sns.barplot(x = 'nom_fed', y = 'l_2019', hue = 'region', data = lic_comm)

test = lic_comm[['nom_fed', 'l_h_2019']].groupby(['nom_fed']).sum().sort_values(by = 'l_h_2019', ascending = False).head(10).reset_index()

test.head()

sns.barplot(x = 'nom_fed', y = 'l_h_2019', data = test)
plt.show()


# Creation d'un df contenant les 10 sports les plus pratiques par les femmes en 2019
femmes = lic_comm[['nom_fed', 'l_f_2019']].groupby(['nom_fed']).sum().sort_values(by = 'l_f_2019', ascending = False).head(10).reset_index()
sns.barplot(x = 'nom_fed', y = 'l_f_2019', data = femmes)
plt.show()


#Selectionner les colonnes de 2019 

lic_comm.columns

lic_comm.iloc[: , 0:15]
fh = lic_comm[['nom_fed', 'code_commune', 'libelle','region', 'l_f_2019', 'l_h_2019']]
fh.head()


fh = fh.melt(id_vars=['nom_fed', 'code_commune', 'libelle', 'region'], value_vars=['l_f_2019', 'l_h_2019'], var_name = 'sexe', value_name = 'nb_licencies')
fh.head()

fh['sexe'] = fh['sexe'].replace(['l_f_2019', 'l_h_2019'], ['F', 'H'])

fh.head()

top = fh[['nom_fed', 'region', 'sexe', 'nb_licencies']].groupby(['nom_fed', 'sexe']).sum('nb_licencies').sort_values(by = 'nb_licencies', ascending = False).head(20).reset_index()
top.head(20)



sns.barplot(x = 'nom_fed', y = 'nb_licencies', hue = 'sexe', data = top)
plt.show()

# Transposer la base 

top_reg = fh[['nom_fed', 'region', 'sexe', 'nb_licencies']].groupby(['nom_fed', 'sexe', 'region']).sum('nb_licencies').sort_values(by = 'nb_licencies', ascending = False).reset_index()

top_reg.columns

top_reg.head()
top_reg[top_reg['sexe'] == 'F']


#Selectionner le sport le plus pratique dans chaque région

fh.columns


#
reg = fh.groupby(['region', 'sexe', 'nom_fed']).sum('nb_licencies').reset_index()
reg.columns

# Pour sélectionner le sport le plus pratiqué dans chaque région : faire une boucle sur le df reg, pour i in region, on selctionne la région i,
# et on filtre pour ne garder que le sport le plus pratiqué par les hommes et par les femmes dans la région
reg.head(5)
reg.ndim
reg.columns

reg['max_licencies'] = reg.groupby(['sexe', 'region']).max('nb_licencies')

reg = reg.drop(columns = ['max_licencies'])
reg.head()

for r in reg['region'] :
    test1 = reg[['region'] == r].reset_index()
    test1['max_licencies'] == test1.groupby(['sexe']).max('nb_licencies')
    print(test1)


test.head()
a.columns


reg.groupby(['region', 'sexe']).max('nb_licencies')


top_reg[top_reg['nb_licencies'] == 157169]




### Transposer la base



### Carte des communes de France

communes = fiona.open("https://www.data.gouv.fr/fr/datasets/r/a01aff2a-8f36-4a77-a73f-efc212fe2899", sep = ';')

communes.head()

import shapefile
