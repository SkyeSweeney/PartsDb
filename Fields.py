

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
        self.fields.append( (0,  "PartNo",        "Part #",         "s") )
        self.fields.append( (1,  "Barcode",       "Barcode",        "s") )
        self.fields.append( (2,  "Website",       "Website",        "s") )
        self.fields.append( (3,  "Mfg",           "Mfg",            "s") )
        self.fields.append( (4,  "MfgPartNo",     "Mfg Part #",     "s") )
        self.fields.append( (5,  "MfgBarcode",    "Mfg Barcode",    "s") )
        self.fields.append( (6,  "MfgWebsite",    "Mfg Website",    "s") )
        self.fields.append( (7,  "Vendor",        "Vendor",         "s") )
        self.fields.append( (8,  "VendorPartNo",  "Vendor Part #",  "s") )
        self.fields.append( (9,  "VendorBarcode", "Vendor Barcode", "s") )
        self.fields.append( (10, "VendorWebsite", "Vendor Website", "s") )
        self.fields.append( (11, "Quantity",      "Quantity",       "s") )
        self.fields.append( (12, "Title",         "Title",          "s") )
        self.fields.append( (13, "Description",   "Description",    "s") )
        self.fields.append( (14, "Catagory",      "Catagory",       "s") )
        self.fields.append( (15, "Package",       "Package",        "s") )
        self.fields.append( (16, "Location",      "Location",       "s") )
        self.fields.append( (17, "Notes",         "Notes",          "s") )
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


