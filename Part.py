import doctest
import time
import Fields



#######################################################################
# This class handles the definition of one part entry
#######################################################################
class Part():

    
    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self):

        # Get list of all fields
        self.flds = Fields.Fields().getFields()

        self.setAll("")

    #

    ###################################################################
    # Set all to a given string
    ###################################################################
    def setAll(self, s):

        # For each field
        for fld in self.flds:

            # Create a default value
            exec("self.%s='%s'" % (fld[1],s))
        #


    ###################################################################
    # Create from list
    ###################################################################
    def setFromList(self, lst):

        # For each field
        for fld in self.flds:
            exec("self.%s=lst[%d]" % (fld[1],fld[0]))
        #

    #

    ###################################################################
    # Create representation
    ###################################################################
    def __repr__(self):

        retval="Part("

        # For each field
        for fld in self.flds:
            exec("v=self.%s" % (fld[1]))
            retval = retval + v + ","
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
        for fld in self.flds:
            exec("v=self.%s" % (fld[1]))
            if ("TEXT" in fld[3]):
                retval = retval + '"%s"' % v + ","
            elif ("INTEGER" in fld[3]):
                retval = retval + '%d' % v + ","
            else:
                pass
        #
        retval = retval[:-1]
        return retval
    #

    ###################################################################
    # Get list of fields
    ###################################################################
    def getFields(self, n):
        return self.flds[n]
    #

    ###################################################################
    # Get the nth field name
    ###################################################################
    def getSqlFieldName(self,n):
        return self.flds[n][1]
    #

    ###################################################################
    # Get value by index
    ###################################################################
    def getValueByIndex(self,n):
        exec("v=self.%s" % (self.flds[n][1]))
        return v
    #

    ###################################################################
    # Set value by index
    ###################################################################
    def setValueByIndex(self, n, val):
        if (isinstance(val, str)):
            exec('self.%s="%s"' % (self.flds[n][1],val))
        elif (isinstance(val, int)):
            exec("self.%s=%s" % (self.flds[n][1],val))
        else:
            print "Invalid type", type(val)
        #
    #

    ###################################################################
    # Get number of fields
    ###################################################################
    def getNumFields(self):
        return len(self.flds)
    #
#

if __name__ == "__main__":

    p = Part()
    print p

    p.setAll("kdkdkd")
    print p
    print p.makeRecord()

    l = ["a", "b", "c", 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r']
    p.setFromList(l)
    print p
    print p.getValueByIndex(1)

