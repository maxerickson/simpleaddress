"""
Compare addresses by shortening them on word boundaries.
"""
import re

wordmap={
"North":"N",
"South":"S",
"East":"E",
"West":"W",
"Northwest":"NW",
"Northeast":"NE",
"Southwest":"SW",
"Southeast":"SE",
"Avenue":"Ave",
"Boulevard":"Blvd",
"Bypass":"Byp",
"Causeway":"Cswy",
"Circle":"Cir",
"Court":"Ct",
"Drive":"Dr",
"Expressway":"Expy",
"Gateway":"Gtwy",
"Highway":"Hwy",
"Lane":"Ln",
"Parkway":"Pkwy",
"Place":"Pl",
"Road":"Rd",
"Route":"Rt",
"Square":"Sq",
"Street":"St",
"Terrace":"Ter",
"Trail":"Trl"
}
# check for abbreviations followed by a period
for d in list(wordmap.values()):
    wordmap[d+"."]=d
# check for abbreviations with different capitalization style than OSM
for d in ["Sw","Se","Nw","Ne","Us"]:
    wordmap[d]=d.upper()

replacemap=dict()
for word,rep in wordmap.items():
    replacemap[word.lower()]=rep

numbersuffixes=["Nd","Rd","St","Th"]

def normalize(address):
    parts=address.split(" ")
    for i,part in enumerate(parts):
        if part.lower() in replacemap:
            parts[i]=replacemap[part.lower()]
        for s in numbersuffixes:
            if s in part and part[0].isnumeric():
                parts[i]=part.replace(s,s.lower())
    return " ".join(parts)

def compare(addr1,addr2):
    return normalize(addr1)==normalize(addr2)

units={
"Suite":"Ste",
"Unit":"Unit"
}

def hasunit(addr):
    for k,v in units.items():
        if k in addr or v in addr:
            return True

if __name__=="__main__":
    print(normalize("601 North Lincoln Road"))
    print(normalize("601 N Lincoln Road"))
    print(normalize("601 N. Lincoln Rd"))
    print(normalize("601 north Lincoln road"))
    print(normalize("7600 Sw Dartmouth St."))
    print(normalize("7600 Southwest Dartmouth Street"))
    print(normalize("1203 6Th Ave Se"))
    print(normalize("1203 6th Avenue Southeast"))
    print(normalize("16746 E Smoky Hill Rd"))
    print(normalize("16746 East Smoky Hill Road"))
    print(normalize("8270 Delta Shores Circle"))
    print(normalize("8270  Delta Shores Circle"))
    addrhousenumber="601"
    addrstreet="North Lincoln Road"
    addrfull="601 N Lincoln Road"
    osmaddress="{} {}".format(addrhousenumber,addrstreet)
    print(compare(osmaddress,addrfull))
