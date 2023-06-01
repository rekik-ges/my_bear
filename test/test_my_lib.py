
import sys
import os
sys.path.append('./../../my_lib')
from my_lib import Series, DataFrame

# Exemple avec une liste de Series
series1 = Series([1, 2, 3], "Colonne 1")
series2 = Series([4, 5, 6], "Colonne 2")
series3 = Series([7, 8, 9], "Colonne 3")
data_frame1 = DataFrame([series1, series2, series3])
print(data_frame1)

# Exemple avec des colonnes et des listes de valeurs
columns = ["Colonne 1", "Colonne 2", "Colonne 3"]
values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
data_frame2 = DataFrame(values, columns)
print(data_frame2)

# Accès aux éléments avec iloc_df
print(data_frame2.iloc_df[1, 2])
print(data_frame2.iloc_df[0:2, 1])
