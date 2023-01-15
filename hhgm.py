# Highest Holywood Grossing Movies
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---- structure fichier CSV
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# '', 
# 'Title', 
# 'Movie Info', 
# 'Distributor', 
# 'Release Date', 
# 'Domestic Sales (in $)', 
# 'International Sales (in $)', 
# 'World Sales (in $)', 
# 'Genre', 
# 'Movie Runtime', 
# 'License'
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 
import csv, datetime, json
from typing_extensions import Self

class HHGM:
    # static attributes
    defaultFilename = "./data/Highest_Holywood_Grossing_Movies.csv"

    # constructor
    def __init__(self: Self) -> None:
        # attributes
        self.header : list[str] = []
        self.rows : list[list[str]] = []
        self.genres : list[str] = []
        self.distributors : list[str] = []
        self.licences : list[str] = []

        self.db : list[dict]= []
    # loadCSV
    def loadCSV(self: Self, filename :(str|None)= None) -> None:
        # 1: load cvs and read raw data
        filename = HHGM.defaultFilename if not filename else filename
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            self.header = next(csvreader)
            for row in csvreader:
                self.rows.append(row)
        # 2: parse data
        print(f'{len(self.rows)} records found!')
        for row in self.rows[:]:
            index, title, info, distributor, releaseDate, domesticSales, internationalSales, worldSales, genre, runtime, license = row
            self.db.append({
                "title" : title, 
                "info" : info, 
                "distributor" : self.parseDistributor(distributor), 
                "releaseDate" : str(HHGM.parseDate(releaseDate, title)), 
                "domesticSales" : int(domesticSales), 
                "internationalSales" : int(internationalSales), 
                "worldSales" : int(worldSales), 
                "genre" : self.parseGenre(genre), 
                "runtime":  HHGM.parseRuntime(runtime), 
                "license" : self.parseLicense(license)
                })
    # exportJSON
    def  exportJSON(self,filename :(str|None)= None) -> None:
        filename = HHGM.defaultFilename if not filename else filename
        if filename.endswith('.csv') : filename = filename[:-4]+'.json'
        if not filename.endswith('.json') : filename = filename+'.json'

        if len(self.db)>0:
            dbJ = {
                    'genres': self.genres,
                    'distributors': self.distributors,
                    'licenses': self.licences,
                    'films': self.db
                }
            with open(filename, 'w') as file: json.dump(dbJ, file)
    
    # parseLicense
    def parseLicense(self, license : str) -> int:
        if not license in self.licences: self.licences.append(license)
        return self.licences.index(license)
    
    # parseRuntime
    @staticmethod
    def parseRuntime(rt: str) -> int:
        nrt = rt.replace('hr',':').replace('min','').replace(' ','') 
        nrt = nrt+'00' if nrt[-1] ==':' else nrt
        h, m = nrt.split(':')
        rtm = int(h)*60+int(m)
        return rtm
    
    # parseDistributeur
    def parseDistributor(self : Self, distri : str) -> int: 
        if not distri in self.distributors: self.distributors.append(distri)
        #print(f'distributors::{distri} -> {self.distributors}:{self.distributors.index(distri)}')
        return self.distributors.index(distri)
    
    # parseGenre
    def parseGenre(self: Self, genre: str) -> list[int]:
        listGenre = list(map(lambda x:x.replace(" ","")[1:-1], genre[1:-1].split(',')))
        for g in listGenre: 
            if not g in self.genres:self.genres.append(g)
        #print(f'genre::{genre} ->  {self.genres}:{list(map(lambda genre:self.genres.index(genre), listGenre))}')
        return list(map(lambda genre:self.genres.index(genre), listGenre))
    
    # parseDate
    @staticmethod
    def parseDate(datestr : str, title: str) -> datetime.date:
        m = {'January':1,'February':2, 'March': 3, 'April':4, 'May':5,'June':6, 'July':7, 'August':8,'September':9,'October':10, 'November':11, 'December':12}
        if datestr != 'NA':
            mounthDay, year = datestr.split(',')
            mounth, day = mounthDay.split(' ')
            #print(f'date:: {datestr} -> {datetime.date(int(year), m[mounth], int(day))}')
            return datetime.date(int(year), m[mounth], int(day))
        else:
            _, end = title.split('(')
            year, _= end.split(')')
            year = int(year)
            #print(f'date:: {title} -> {datetime.date(year, 6,15)}')
            return datetime.date(year, 6,15)

    

# ------------------------------------------------------------
# --- create database as json file                         ---
# ------------------------------------------------------------
if __name__  == "__main__":
    db = HHGM()
    db.loadCSV()
    db.exportJSON()
    f = open("./data/Highest_Holywood_Grossing_Movies.json")
    test = json.load(f)
    for i in test['films']:
        print(i)
