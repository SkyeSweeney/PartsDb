
import collections

#######################################################################
#
#######################################################################
class Fields():

    ###################################################################
    #
    ###################################################################
    def __init__(self):

        # Create a named tuple type
        PartFieldInfo = collections.namedtuple("PartFieldInfo", ["id", "SqlName", "HumanName", "SqlType", "Editable"])

        # Create a list for each field
        self.fields = []

        #                                 id, fieldName        HumanName,        type                   editable
        self.fields.append( PartFieldInfo(0,  "PartNo",        "Part #",         "INTEGER PRIMARY KEY", False) )
        self.fields.append( PartFieldInfo(1,  "Barcode",       "Barcode",        "TEXT",                False) )
        self.fields.append( PartFieldInfo(2,  "Website",       "Website",        "TEXT",                True) )
        self.fields.append( PartFieldInfo(3,  "Mfg",           "Mfg",            "TEXT",                True) )
        self.fields.append( PartFieldInfo(4,  "MfgPartNo",     "Mfg Part #",     "TEXT",                True) )
        self.fields.append( PartFieldInfo(5,  "MfgBarcode",    "Mfg Barcode",    "TEXT",                True) )
        self.fields.append( PartFieldInfo(6,  "MfgWebsite",    "Mfg Website",    "TEXT",                True) )
        self.fields.append( PartFieldInfo(7,  "Vendor",        "Vendor",         "TEXT",                True) )
        self.fields.append( PartFieldInfo(8,  "VendorPartNo",  "Vendor Part #",  "TEXT",                True) )
        self.fields.append( PartFieldInfo(9,  "VendorBarcode", "Vendor Barcode", "TEXT",                True) )
        self.fields.append( PartFieldInfo(10, "VendorWebsite", "Vendor Website", "TEXT",                True) )
        self.fields.append( PartFieldInfo(11, "Quantity",      "Quantity",       "TEXT",                True) )
        self.fields.append( PartFieldInfo(12, "Title",         "Title",          "TEXT",                True) )
        self.fields.append( PartFieldInfo(13, "Description",   "Description",    "TEXT",                True) )
        self.fields.append( PartFieldInfo(14, "Catagory",      "Catagory",       "TEXT",                True) )
        self.fields.append( PartFieldInfo(15, "Package",       "Package",        "TEXT",                True) )
        self.fields.append( PartFieldInfo(16, "Location",      "Location",       "TEXT",                True) )
        self.fields.append( PartFieldInfo(17, "Notes",         "Notes",          "TEXT",                True) )
    #


    ###################################################################
    # Get number of fields in database
    ###################################################################
    def getNumFields(self):
        return len(self.fields)
    #


    ###################################################################
    # Get list of all fields
    ###################################################################
    def getFields(self):
        return self.fields
    #


    ###################################################################
    # Does the field name exist
    ###################################################################
    def exists(self, fld):
        for field in self.fields:
            if (fld == field.SqlName) or (fld == field.HumanName):
                return True
            #
        #
        return False
    #
#

    

#######################################################################
#
#######################################################################
if __name__ == '__main__':
    f = Fields()
    print f.getFields()
    print f.exists("aaa")
    print f.exists("Part #")
    print f.exists("PartNo")


