class Series:
    def __init__(self, data, name):
        self.data = data                    # Assigner les données à l'attribut 'data'
        self.name = name                    # Assigner le nom à l'attribut 'name'
        self.size = len(data)               # Calculer la taille des données et l'assigner à l'attribut 'size'
        self.missing_values = self.count_missing_values()  # Calculer le nombre de valeurs manquantes et l'assigner à l'attribut 'missing_values'
        self.data_type = self.detect_data_type()           # Déterminer le type de données et l'assigner à l'attribut 'data_type'

    def count_missing_values(self):
        return self.data.count(None)        # Compter le nombre de valeurs None dans les données

    def detect_data_type(self):
        data_types = set(type(value).__name__ for value in self.data)  # Créer un ensemble de types de données uniques dans les données
        if len(data_types) == 1:
            return data_types.pop()         # S'il n'y a qu'un seul type de données, le renvoyer
        else:
            return "Mixte"                   # S'il y a plusieurs types de données, renvoyer "Mixte"

    def __str__(self):
        return f"Série : {self.name}\nDonnées : {self.data}\nTaille : {self.size}\nValeurs manquantes : {self.missing_values}\nType de données : {self.data_type}"  # Renvoyer une représentation sous forme de chaîne de caractères de l'objet Series

    def iloc(self, index):
        if isinstance(index, int):
            return self.data[index]         # Renvoyer la valeur à l'index spécifié
        elif isinstance(index, slice):
            return Series(self.data[index], self.name)  # Renvoyer un nouvel objet Series avec les données découpées
        else:
            raise TypeError("Type d'index non valide")

    def max(self):
        return max(self.data)                # Renvoyer la valeur maximale dans les données

    def min(self):
        return min(self.data)                # Renvoyer la valeur minimale dans les données

    def mean(self):
        return sum(self.data) / len(self.data)  # Calculer la moyenne des données

    def std(self):
        mean = self.mean()                    # Calculer la moyenne des données
        squared_diffs = [(value - mean) ** 2 for value in self.data]  # Calculer les différences au carré par rapport à la moyenne
        variance = sum(squared_diffs) / len(self.data)                # Calculer la variance
        return variance ** 0.5                # Renvoyer l'écart type

    def count(self):
        return len(self.data)                 # Renvoyer le nombre d'éléments dans les données


class DataFrame:
    def __init__(self, data=None, columns=None):
        if data is None:
            self.data = []                    # Si aucune donnée n'est fournie, initialiser une liste vide pour les données
            self.columns = []                 # Si aucune colonne n'est fournie, initialiser une liste vide pour les colonnes
        elif isinstance(data, list) and all(isinstance(series, Series) for series in data):
            self.data = data                   # Si les données sont une liste d'objets Series, les assigner à l'attribut 'data'
            self.columns = [series.name for series in data]  # Récupérer les noms des séries et les assigner à l'attribut 'columns'
        elif isinstance(data, list) and columns is not None:
            if len(data) != len(columns):
                raise ValueError("Le nombre de colonnes ne correspond pas aux données")  # Lever une erreur si le nombre de colonnes ne correspond pas aux données
            self.data = [Series(col_data, col_name) for col_data, col_name in zip(data, columns)]  # Créer des objets Series à partir des données et noms fournis et les assigner à l'attribut 'data'
            self.columns = columns            # Assigner les colonnes fournies à l'attribut 'columns'
        else:
            raise TypeError("Type de données non valide")  # Lever une erreur si le type de données est invalide

    def __getitem__(self, index):
        if isinstance(index, tuple):
            row_index, col_index = index
            if isinstance(row_index, int) and isinstance(col_index, int):
                return self.data[col_index].data[row_index]  # Renvoyer la valeur à l'index de ligne et de colonne spécifié
            elif isinstance(row_index, slice) and isinstance(col_index, int):
                sub_series = self.data[col_index].data[row_index]  # Découper les données à l'index de ligne spécifié et à l'index de colonne spécifié
                sub_name = self.data[col_index].name                # Obtenir le nom de la sous-série
                return Series(sub_series, sub_name)                 # Renvoyer un nouvel objet Series avec les données découpées
            elif isinstance(row_index, int) and isinstance(col_index, slice):
                sub_data = [series.data[row_index] for series in self.data[col_index]]  # Découper les données à l'index de ligne spécifié et à la plage de colonnes spécifiée
                sub_names = self.columns[col_index]                                      # Obtenir les noms des sous-colonnes
                return DataFrame(sub_data, sub_names)                                    # Renvoyer un nouvel objet DataFrame avec les données découpées
            elif isinstance(row_index, slice) and isinstance(col_index, slice):
                sub_data = [series.data[row_index] for series in self.data[col_index]]  # Découper les données à la plage de lignes spécifiée et à la plage de colonnes spécifiée
                sub_names = self.columns[col_index]                                      # Obtenir les noms des sous-colonnes
                return DataFrame(sub_data, sub_names)                                    # Renvoyer un nouvel objet DataFrame avec les données découpées
        else:
            raise TypeError("Type(s) d'index non valide(s)")  # Lever une erreur si les types d'index sont invalides

    @property
    def iloc_df(self):
        return DataFrameIndexer(self.data, self.columns)  # Renvoyer un objet DataFrameIndexer pour l'indexation basée sur les entiers

    def __str__(self):
        return "\n".join(f"{col_name}: {series}" for col_name, series in zip(self.columns, self.data))  # Renvoyer une représentation sous forme de chaîne de caractères de l'objet DataFrame


class DataFrameIndexer:
    def __init__(self, data, columns):
        self.data = data                   # Assigner les données à l'attribut 'data' de l'indexeur
        self.columns = columns             # Assigner les colonnes à l'attribut 'columns' de l'indexeur

    def __getitem__(self, index):
        if isinstance(index, tuple):
            row_index, col_index = index
            if isinstance(row_index, int) and isinstance(col_index, int):
                return self.data[col_index].data[row_index]  # Renvoyer la valeur à l'index de ligne et de colonne spécifié
            elif isinstance(row_index, slice) and isinstance(col_index, int):
                sub_series = self.data[col_index].data[row_index]  # Découper les données à l'index de ligne spécifié et à l'index de colonne spécifié
                sub_name = self.data[col_index].name                # Obtenir le nom de la sous-série
                return Series(sub_series, sub_name)                 # Renvoyer un nouvel objet Series avec les données découpées
            elif isinstance(row_index, int) and isinstance(col_index, slice):
                sub_data = [series.data[row_index] for series in self.data[col_index]]  # Découper les données à l'index de ligne spécifié et à la plage de colonnes spécifiée
                sub_names = self.columns[col_index]                                      # Obtenir les noms des sous-colonnes
                return DataFrame([sub_data], sub_names)                                  # Renvoyer un nouvel objet DataFrame avec les données découpées
            elif isinstance(row_index, slice) and isinstance(col_index, slice):
                sub_data = [series.data[row_index] for series in self.data[col_index]]  # Découper les données à la plage de lignes spécifiée et à la plage de colonnes spécifiée
                sub_names = self.columns[col_index]                                      # Obtenir les noms des sous-colonnes
                return DataFrame(sub_data, sub_names)                                    # Renvoyer un nouvel objet DataFrame avec les données découpées
        else:
            raise TypeError("Type(s) d'index non valide(s)")  # Lever une erreur si les types d'index sont invalides
