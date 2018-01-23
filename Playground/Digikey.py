
import httplib

conn = httplib.HTTPSConnection("api.digikey.com")

payload = "{\"SearchOptions\":[\"ExcludeNonStock\"],\"Keywords\":\"p5555-nd\",\"RecordCount\":\"10\",\"RecordStartPosition\":\"0\",\"Filters\":{\"CategoryIds\":[91068335],\"FamilyIds\":[54499193],\"ManufacturerIds\":[98654823],\"ParametricFilters\":[{\"ParameterId\":94204645,\"ValueId\":\"6422679122870272\"}]},\"Sort\":{\"Option\":\"SortByUnitPrice\",\"Direction\":\"Ascending\",\"SortParameterId\":66919715},\"RequestedQuantity\":20}"

headers = {
    'x-ibm-client-id': "REPLACE_THIS_KEY",
    'content-type': "application/json",
    'accept': "application/json",
    'x-digikey-locale-site': "REPLACE_THIS_VALUE",
    'x-digikey-locale-language': "REPLACE_THIS_VALUE",
    'x-digikey-locale-currency': "REPLACE_THIS_VALUE",
    'x-digikey-locale-shiptocountry': "REPLACE_THIS_VALUE",
    'x-digikey-customer-id': "REPLACE_THIS_VALUE",
    'x-digikey-partner-id': "REPLACE_THIS_VALUE",
    'authorization': "REPLACE_THIS_VALUE"
    }

conn.request("POST", "/services/partsearch/v2/keywordsearch", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
