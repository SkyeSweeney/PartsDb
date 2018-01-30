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



        # SQL names for fields
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

        # Human names for fields
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

        # SQL types for each field
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

        # Is the field editable
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

        # Default values for a new part
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

        self.values      = []

        # Determine number of fields
        self.numFields = len(self.sqlNames)

        # Set default values
        self.setDefaults()

    #

    ###################################################################
    # Set all fields to default value
    ###################################################################
    def setDefaults(self):

        # Do a deep copy
        self.values = self.defaults[:]

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

        retval = ""

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
            print "Invalid index in GetValueByIndex"
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

