Word lists and some simple building blocks for altering the formatting of US addresses.

    >>> from simpleaddress import normalize, expand_streetname
    >>> normalize("2200 Bostill Rd Se Suite A")
    '2200 Bostill Rd SE Ste A'
    >>> expand_streetname("2200 Bostill Rd Se Suite A")
    '2200 Bostill Road Se Suite A'
    >>> expand_streetname(normalize("2200 Bostill Rd Se Suite A"))
    '2200 Bostill Road Southeast Suite A'
    >>> 
