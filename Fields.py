

#######################################################################
#
#######################################################################
class Fields():

    ###################################################################
    #
    ###################################################################
    def __init__(self):

        self.fields = []

        #                    id, fieldName        HumanName,     type
        self.fields.append( (0,  "PartNo",        "Part #",         "INTEGER PRIMARY KEY") )
        self.fields.append( (1,  "Barcode",       "Barcode",        "TEXT") )
        self.fields.append( (2,  "Website",       "Website",        "TEXT") )
        self.fields.append( (3,  "Mfg",           "Mfg",            "TEXT") )
        self.fields.append( (4,  "MfgPartNo",     "Mfg Part #",     "TEXT") )
        self.fields.append( (5,  "MfgBarcode",    "Mfg Barcode",    "TEXT") )
        self.fields.append( (6,  "MfgWebsite",    "Mfg Website",    "TEXT") )
        self.fields.append( (7,  "Vendor",        "Vendor",         "TEXT") )
        self.fields.append( (8,  "VendorPartNo",  "Vendor Part #",  "TEXT") )
        self.fields.append( (9,  "VendorBarcode", "Vendor Barcode", "TEXT") )
        self.fields.append( (10, "VendorWebsite", "Vendor Website", "TEXT") )
        self.fields.append( (11, "Quantity",      "Quantity",       "TEXT") )
        self.fields.append( (12, "Title",         "Title",          "TEXT") )
        self.fields.append( (13, "Description",   "Description",    "TEXT") )
        self.fields.append( (14, "Catagory",      "Catagory",       "TEXT") )
        self.fields.append( (15, "Package",       "Package",        "TEXT") )
        self.fields.append( (16, "Location",      "Location",       "TEXT") )
        self.fields.append( (17, "Notes",         "Notes",          "TEXT") )
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
            if (fld == field[1]):
                return field
            #
        #
        return None
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


