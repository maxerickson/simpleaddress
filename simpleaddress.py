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
rmap2=dict()
for word,rep in wordmap.items():
    regex=re.compile("(^|(?<=\s))"+re.escape(word)+"(?=\s|$)", re.I)
    replacemap[regex]=rep
    rmap2[word.lower()]=rep

numbersuffixes=["Nd","Rd","St","Th"]
# check for number suffixes with different capitalization style than OSM
for suffix in ["Nd","Rd","St","Th"]:
    regex=re.compile("\d"+suffix+"(?=\s|$)",re.I)
    replacemap[regex]=suffix.lower()
    #~ rmap2[suffix.lower()]=suffix.lower()

def replacer(address):
    for word,rep in replacemap.items():
        address=word.sub(rep, address)
    return address

def replacer2(address):
    parts=address.split(" ")
    for i,part in enumerate(parts):
        if part.lower() in rmap2:
            parts[i]=rmap2[part.lower()]
        for s in numbersuffixes:
            if s in part and part[0].isnumeric():
                parts[i]=part.replace(s,s.lower())
    return " ".join(parts)
replacer=replacer2
print(rmap2)
def compare(addr1,addr2):
    return replacer(addr1)==replacer(addr2)

units={
"Suite":"Ste",
"Unit":"Unit"
}

def hasunit(addr):
    for k,v in units.items():
        if k in addr or v in addr:
            return True

if __name__=="__main__":
    print(replacer("601 North Lincoln Road"))
    print(replacer("601 N Lincoln Road"))
    print(replacer("601 N. Lincoln Rd"))
    print(replacer("601 north Lincoln road"))
    print(replacer("7600 Sw Dartmouth St."))
    print(replacer("7600 Southwest Dartmouth Street"))
    print(replacer("1203 6Th Ave Se"))
    print(replacer("1203 6th Avenue Southeast"))
    print(replacer("16746 E Smoky Hill Rd"))
    print(replacer("16746 East Smoky Hill Road"))
    addrhousenumber="601"
    addrstreet="North Lincoln Road"
    addrfull="601 N Lincoln Road"
    osmaddress="{} {}".format(addrhousenumber,addrstreet)
    print(compare(osmaddress,addrfull))
