import json
from time import sleep

from matplotlib.pyplot import title
import hhgm

class ModeleBDD:
    def __init__(self, path:(str|None)= None) -> None:
        # Récupere les données du JSON fournis ou par défault.
        # Le créer à partir du CSV par défault si inexistant.  
        try:
            if path: f=open(path)
            else : f=open(hhgm.HHGM.defaultFilename[:-4]+'.json')
            db = json.load(f)
        except OSError:
            print("Fichier non existant ou accesible! Génération d'un json dans :  ")
            
            csv = hhgm.HHGM()
            csv.loadCSV()
            csv.exportJSON()
            f=open("./data/Highest_Holywood_Grossing_Movies.json")
            db = json.load(f)
        
        
        # attribut
        self.genres : list[str] = db['genres']
        self.distributors : list[str] = db['distributors']
        self.licenses : list[str] = db['licenses']
        self.films : list[dict] = db['films']
        self.filmsTrie : list[dict] = self.films.copy()
        self.indice=0    
    
    def filtrer(self, distrib: list[str], genre: list[str], lic: list[str]):
        if not distrib or not genre or not lic :
            return self.filmsTrie
        test = 0
        for film in self.films:
            if (self.distributors[film['distributor']] in distrib) and (self.licenses[film['license']] in lic):
                if [i for i in film['genre'] if self.genres[i] in genre]:
                    test = 1
        if (test == 1):
            self.filmsTrie.clear()
            for film in self.films:
                if (self.distributors[film['distributor']] in distrib) and (self.licenses[film['license']] in lic):
                    if [i for i in film['genre'] if self.genres[i] in genre]:
                        self.filmsTrie.append(film)
            self.indice=0
        else:
            return self.filmsTrie


    
    # liste globale
    def getAllGenres(self):
        return self.genres
    
    def getAllDistibutors(self):
        return self.distributors
    
    def getAllLicenses(self):
        return self.licenses
    
    def getFilms(self):
        return self.filmsTrie

    def getAllFilms(self):
        return self.films
    
    def getI(self):
        return self.indice
    
    # infos des films filtrés
    def next(self):
        self.indice=(self.indice+1)%len(self.filmsTrie)
        
    def prev(self):
        self.indice=(self.indice-1)%len(self.filmsTrie)
        
    def getWS(self):
        return self.filmsTrie[self.indice]['worldSales']
    
    def getIS(self):
        return self.filmsTrie[self.indice]['internationalSales']
    
    def getDS(self):
        return self.filmsTrie[self.indice]['domesticSales']
    
    def getTitle(self):
        return self.filmsTrie[self.indice]['title']
    
    def getInfo(self):
        return self.filmsTrie[self.indice]['info']
    
    def getGenre(self):
        return self.filmsTrie[self.indice]['genre']
    
    def getRuntime(self):
        return self.filmsTrie[self.indice]['runtime']
    
    def getLicense(self):
        return self.filmsTrie[self.indice]['license']
    
    def getDistributor(self):
        return self.filmsTrie[self.indice]['distributor']
    
    
    # renvoie une liste contenant toutes les valeurs des films filtrés
    def getListWS(self):
        return [self.filmsTrie[i]['worldSales'] for i in range(len(self.filmsTrie))]
    
    def getListIS(self):
        return [self.filmsTrie[i]['internationalSales'] for i in range(len(self.filmsTrie))]
    
    def getListDS(self):
        return [self.filmsTrie[i]['domesticSales'] for i in range(len(self.filmsTrie))]
    
    def getListTitle(self):
        return [self.filmsTrie[i]['title'] for i in range(len(self.filmsTrie))]
    
    def getListInfo(self):
        return [self.filmsTrie[i]['info'] for i in range(len(self.filmsTrie))]
    
    def getListGenre(self):
        return [self.filmsTrie[i]['genre'] for i in range(len(self.filmsTrie))]
    
    def getListRuntime(self):
        return [self.filmsTrie[i]['runtime'] for i in range(len(self.filmsTrie))]
    
    def getListLicense(self):
        return [self.filmsTrie[i]['license'] for i in range(len(self.filmsTrie))]
    
    def getListDistributor(self):
        return [self.filmsTrie[i]['distributor'] for i in range(len(self.filmsTrie))]
        
    
if __name__ == "__main__" :

    test=ModeleBDD()
    # for film in test.getFilms():
    #     print(film['title'])
    # sleep(5)
    print("-----------------------------")
    test.filtrer(["Summit Entertainment"],test.getAllGenres(),test.getAllLicenses())
    print(test.getFilms())
    