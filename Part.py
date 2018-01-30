import doctest
import time
import collections



#######################################################################
# This class handles the definition of one part entry
#######################################################################
class Part():

    
    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self):


        self.ids        = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]

        self.sqlNames   = ["PartId",
                           "Name",
                           "Description",
                           "Quantity",
                           "Min",
                           "Location",
                           "Mfg",
                           "MfgPartNo",
                           "MfgWebsite",
                           "Vendor",
                           "VendorPartNo",
                           "VendorWebsite",
                           "Datasheet",
                           "Notes"]

        self.humanNames = ["PartId",
                           "Name",
                           "Description",
                           "Quantity",
                           "Min",
                           "Location",
                           "Mfg",
                           "MfgPartNo",
                           "MfgWebsite",
                           "Vendor",
                           "VendorPartNo",
                           "VendorWebsite",
                           "Datasheet",
                           "Notes"]

        self.sqlTypes   = ["INTEGER PRIMARY KEY",
                           "TEXT",
                           "TEXT",
                           "INTEGER",
                           "INTEGER",
                           "TEXT",
                           "TEXT",
                           "TEXT",
                           "TEXT",
                           "TEXT",
                           "TEXT",
                           "TEXT",
                           "TEXT",
                           "TEXT"]

        self.editables   = [False,
                            True,
                            True,
                            True,
                            True,
                            True,
                            True,
                            True,
                            True,
                            True,
                            True,
                            True,
                            True,
                            True]

        self.defaults    = [0,
                            "*",
                            "*",
                            0,
                            0,
                            "*",
                            "*",
                            "*",
                            "*",
                            "*",
                            "*",
                            "*",
                            "*",
                            "*"]

        self.values      = [0,
                            "",
                            "",
                            0,
                            0,
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""]

        # Determine number of fields
        self.numFields = 14

        # Set default values
        self.setDefaults()

    #

    ###################################################################
    # Set all fields to default value
    ###################################################################
    def setDefaults(self):

        # For each field
        for i in range(self.numFields):
            self.values[i] = self.defaults[i]
        #

    #


    ###################################################################
    # Populate field names from a list
    ###################################################################
    def setFromList(self, lst):

        # For each field
        for iFld in range(self.numFields):
            self.values[iFld] = lst[iFld]
        #

    #

    ###################################################################
    # Create representation
    ###################################################################
    def __repr__(self):

        retval="Part("

        # For each field
        for iFld in range(self.numFields):
            if ("TEXT" in self.sqlTypes[iFld]):
                retval = retval + '"%s"' % self.values[iFld] + ","
            elif ("INTEGER" in self.sqlTypes[iFld]):
                retval = retval + '%d' % self.values[iFld] + ","
            else:
                pass
        #
        retval = retval[:-1] + ")"
        return retval
    #

    ###################################################################
    # Create a record entry in SqLite form
    ###################################################################
    def makeRecord(self):

        retval=""

        # For each field
        for iFld in range(self.numFields):
            if ("KEY" in self.sqlTypes[iFld]):
                retval = retval + 'null' + ","
            if ("TEXT" in self.sqlTypes[iFld]):
                retval = retval + '"%s"' % self.values[iFld] + ","
            elif ("INTEGER" in self.sqlTypes[iFld]):
                retval = retval + '%d' % self.values[iFld] + ","
            else:
                pass
            #
        #
        retval = retval[:-1]
        return retval
    #

    ###################################################################
    # Create a VALUE entry in SqLite form
    ###################################################################
    def makeValue(self):

        retval=""

        # For each field
        for iFld in range(self.numFields):
            if ("PRIMARY" not in self.sqlTypes[iFld]):
                if ("TEXT" in self.sqlTypes[iFld]):
                    retval = retval + '"%s"' % self.values[iFld] + ","
                elif ("INTEGER" in self.sqlTypes[iFld]):
                    retval = retval + '%d' % self.values[iFld] + ","
                else:
                    pass
                #
            #
        #
        retval = retval[:-1]
        return retval
    #

    ###################################################################
    # Create a SELECT string in SqLite form
    ###################################################################
    def makeSelect(self):

        retval=""

        # For each field
        for iFld in range(self.numFields):
            if ("PRIMARY" not in self.sqlTypes[iFld]):
                retval = retval + '%s' % self.sqlNames[iFld] + ","
            #
        #
        retval = retval[:-1]
        return retval
    #


    ###################################################################
    # Get value by index
    ###################################################################
    def getValueByIndex(self,n):
        try:
            v = self.values[n]
        except:
            print "Invalid index"
            raise IndexError()
        #
        return v
    #

    ###################################################################
    # Set value by index
    ###################################################################
    def setValueByIndex(self, n, val):
        try:
            self.values[n] = val
        except:
            print "Invalid index in setValueByIndex"
            raise IndexError()
        #
    #

    ###################################################################
    # Get number of fields
    ###################################################################
    def getNumFields(self):
        return self.numFields
    #

#

    

#######################################################################
#
#######################################################################
if __name__ == "__main__":

    # Create a blank part
    p = Part()
    print p

    p.setValueByIndex(0, 33)
    print p

    # Set all fields to defaults
    p.setDefaults()
    print p

    # Print as an SQL cmd
    print p.makeRecord()

    # Populate the part from a list
    l   = [0,
           "Name",
           "Description",
           10,
           5,
           "Location",
           "Mfg",
           "MfgPartNo",
           "MfgWebsite",
           "Vendor",
           "VendorPartNo",
           "VendorWebsite",
           "Datasheet",
           "Notes"]

    print l
    p.setFromList(l)
    print "SetFromList", p

    print p.getValueByIndex(1)
    print p.getValueByIndex(2)
    print p.getValueByIndex(3)
    try:
        print p.getValueByIndex(99)
    except:
        print "Bad index"
    #

    print p.makeValue()
    print p.makeSelect()

    #print p.exists("aaa")
    #print p.exists("Part #")
    #print p.exists("PartNo")

