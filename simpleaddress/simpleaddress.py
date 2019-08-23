# Copyright 2017 Max Erickson

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

    # http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
__location__=os.path.dirname(os.path.realpath(__file__))

directions={
"North":"N",
"South":"S",
"East":"E",
"West":"W",
"Northwest":"NW",
"Northeast":"NE",
"Southwest":"SW",
"Southeast":"SE"
}

street_suffixes={
"Avenue":"Ave",
"Boulevard":"Blvd",
"Bypass":"Byp",
"Causeway":"Cswy",
"Circle":"Cir",
"Court":"Ct",
"Drive":"Dr",
"Expressway":"Expy",
"Freeway":"Fwy",
"Gateway":"Gtwy",
"Highway":"Hwy",
"Lane":"Ln",
"Parkway":"Pkwy",
"Place":"Pl",
"Plaza":"Plz",
"Road":"Rd",
"Route":"Rt",
"Saint":"St",
"Square":"Sq",
"Street":"St",
"Suite":"Ste",
"Terrace":"Ter",
"Trail":"Trl"
}

saints=open(os.path.join(__location__,"saints")).read().splitlines(False)
saints=set(saints)

abpairs=open(os.path.join(__location__,"abbreviations")).read().splitlines(False)
expansions=dict()
words=list()
for line in abpairs:
    ab,word = line.split(",")
    if ab in expansions:
        print(ab,word)
    expansions[ab]=word
    words.append(word)
wm=dict()
for ab,word in expansions.items():
    if words.count(word)==1:
        wm[word]=ab

wordmap=dict()
wordmap.update(directions)
wordmap.update(street_suffixes)
# check for abbreviations followed by a period
for d in list(wordmap.values()):
    wordmap[(d+".").lower()]=d

# check for abbreviations with different capitalization style than OSM
for d in ["Sw","Se","Nw","Ne","Us"]:
    wordmap[d]=d.upper()

# normalize keys to lowercase
replacemap=dict((word.lower(),rep) for word,rep in wordmap.items())
numbersuffixes=["Nd","Rd","St","Th"]

def normalize(address):
    """Normalize individual words to titlecase, abbreviated versions."""
    parts=address.split(" ")
    for i,part in enumerate(parts):
        if part.lower() in replacemap:
            parts[i]=replacemap[part.lower()]
        if part and part[0].isnumeric():
            for s in numbersuffixes:
                if s in part:
                    parts[i]=part.replace(s,s.lower())
    return " ".join(parts)

"""
Compare addresses by shortening them on word boundaries.
"""
def compare(addr1,addr2):
    return normalize(addr1)==normalize(addr2)

def expand_saint(parts):
    sainted=saints.intersection(parts)
    for s in sainted:
        i=parts.index(s)
        if i > 0 and parts[i-1].lower() in {"st.","st"}:
            parts[i-1]="Saint"
        if i > 0 and parts[i-1].lower() in {"ste","ste."}:
            parts[i-1]="Sainte"
    return parts

#~ revmap=dict((v,k) for k,v in street_suffixes.items())
revmap=expansions
for k,v in directions.items():
    revmap[v]=k
def expand_streetname(name):
    parts=name.split()
    parts=expand_saint(parts)
    for i in range(len(parts)):
        if parts[i] in revmap:
            parts[i]=revmap[parts[i]]
    return " ".join(parts)
            


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

    print(expand_streetname("Mary Street"))
    print(expand_streetname("St. Mary St"))
    print(expand_streetname("St Mary Ave"))
    print(expand_streetname("150 St Mark Court, Dallas"))