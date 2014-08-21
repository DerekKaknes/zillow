import pprint
import xml.etree.ElementTree as ET
import requests

API_BASE = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm'
ZWSID = 'X1-ZWz1b5gu59r30r_2uji4'

address = '619 W 142nd St Apt 3'
city = 'New York'
state = 'NY'
zipcode = '10031'

address = '733 Cambridge Street Apt 2'
city = 'Brighton'
state = 'MA'
zipcode = '02135'

# address = '118 Market St'
# city = 'Philadelphia'
# state = 'PA'
# zipcode = '19106'

citystatezip = city+', '+state+' '+zipcode

parameters = [('zws-id', ZWSID), ('address',address), ('citystatezip', citystatezip), ('rentzestimate', 'True')]
payload = {}
for param in parameters:
    payload[param[0]] = param[1]

r= requests.get(API_BASE, params=payload)

try:
    root = ET.fromstring(r.content)
    result = root.find('response').find('results').find('result')

    addr = result.find('address').find('street')
    rent = result.find('rentzestimate')
    bedrooms = result.find('bedrooms')
    baths = result.find('bathrooms')
    usecode = result.find('useCode')
    print addr.text
    print usecode.text
    try:
        print bedrooms.text
    except:
        print 'Unknown Bedrooms'
    try:
        print baths.text
    except:
        print 'Unknown Baths'
    val_range = [int(rent.find('valuationRange').find('low').text), int(rent.find('valuationRange').find('high').text)]

    for child in rent:
        try:
            print child.tag + ' : ' + child.text
        except:
            print child.tag
    print val_range
    print ((val_range[1])/float(val_range[0]) -1)*100
    try:
        print sum(val_range)/2 / int(bedrooms.text)
    except:
        print 'Unknown $ / Bdrm'

except:
    print r.content
