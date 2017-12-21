import simpleaddress

# patch in a data specific value
simpleaddress.replacemap["no."]="N"

def parts(address):
    number, street=address.split(" ",1)
    unit=""
    for test in [" Suite "," Unit "]:
        if test in street:
            street,ste,uni=street.partition(test)
            unit=ste.lstrip()+uni
            street=street.strip(",")
    return number, street, unit

addresses="""3-3300 Kuhio Hwy
11400 Highway 99
2909 Austell Rd Sw Suite 100
1334 Flammang Dr
1335 No. Flamingo Ln.""".splitlines()

for address in addresses:
	normal=simpleaddress.normalize(address)
	#~ print(address, normal)
	expand=simpleaddress.expand_streetname(normal)
	#~ print(address, expand)
	number, street, unit=parts(expand)
	print(number, street, unit, sep="|")