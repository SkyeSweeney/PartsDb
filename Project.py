import doctest
import time
import collections



#######################################################################
# This class handles the definition of one project entry
#######################################################################
class Project():

    
    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self):

        self.humanNames = ["ProjectId", "Name", "Description", "Notes"]

        self.sqlNames = ["ProjectId", "Name", "Description", "Notes"]

        self.sqlTypes = ["INTEGER PRIMARY KEY", "TEXT", "TEXT", "TEXT"]

        self.editables = [False, True, True, True]

        self.defaults = [0, "*", "*", "*"]

        self.values = []

        self.numFields = len(self.humanNames)

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

        retval="Project("

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
            elif ("TEXT" in self.sqlTypes[iFld]):
                retval = retval + '"%s"' % self.values[iFld] + ","
            elif ("INTEGER" in fld.SqlType):
                retval = retval + '%d' % self.values[iFld] + ","
            else:
                pass
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
            print "Invalid index in getValueByIndex"
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

    # Create a blank project
    p = Project()
    print p

    p.setValueByIndex(0, 33)
    print p

    # Set all fields to defaults
    p.setDefaults()
    print p

    # Print as an SQL cmd
    print "make record"
    print p.makeRecord()

    # Populate the project from a list
    l = [0, "Title", "Description", "Notes"]
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

    print p.getFieldInfo(3)
    print p.getAllFieldInfo()
    try:
        print p.getFieldInfo(99) 
    except:
        print "Bad index"
    #

    #print p.exists("aaa")
    #print p.exists("Project #")
    #print p.exists("ProjectNo")

