import doctest
import time
import collections



#######################################################################
# This class handles the definition of one category entry
#######################################################################
class Category():

    
    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self):

        # Create a named tuple type
        CategoryFieldInfo = collections.namedtuple("CategoryFieldInfo", ["Id", "SqlName", "HumanName", "SqlType", "Editable", "DefaultVal"])

        # Create a list of information about each field
        self.fields = []

        #                                      Id, SqlName          HumanName,        SqlType                Editable   DefaultVal
        self.fields.append( CategoryFieldInfo (0,  "CategoryNo",    "Category #",     "INTEGER PRIMARY KEY", False,    0) )
        self.fields.append( CategoryFieldInfo (1,  "Title",         "Title",          "TEXT",                True,     "*") )
        self.fields.append( CategoryFieldInfo (2,  "Description",   "Description",    "TEXT",                True,     "*") )
        self.fields.append( CategoryFieldInfo (3,  "Notes",         "Notes",          "TEXT",                True,     "*") )

        self.numFields = len(self.fields)

        self.values = ["" for x in range(self.numFields)]

        self.setDefaults()

    #

    ###################################################################
    # Set all fields to default value
    ###################################################################
    def setDefaults(self):

        # For each field
        for fld in self.fields:
            self.values[fld.Id] = fld.DefaultVal
        #

    #


    ###################################################################
    # Populate field names from a list
    ###################################################################
    def setFromList(self, lst):

        # For each field
        for iFld in range(self.numFields):
            fld = self.fields[iFld]
            self.values[fld.Id] = lst[iFld]
        #

    #

    ###################################################################
    # Create representation
    ###################################################################
    def __repr__(self):

        retval="Category("

        # For each field
        for iFld in range(self.numFields):
            fld = self.fields[iFld]
            if ("TEXT" in fld.SqlType):
                retval = retval + '"%s"' % self.values[iFld] + ","
            elif ("INTEGER" in fld.SqlType):
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
            fld = self.fields[iFld]
            if ("TEXT" in fld.SqlType):
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
    # Get list of field info of nth field
    ###################################################################
    def getFieldInfo(self, n):
        try:
            return self.fields[n]
        except:
            raise IndexError()
        #
    #

    ###################################################################
    # Get list of all fields
    ###################################################################
    def getAllFieldInfo(self):
        return self.fields
    #

    ###################################################################
    # Get value by index
    ###################################################################
    def getValueByIndex(self,n):
        try:
            v = self.values[self.fields[n].Id]
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
            self.values[self.fields[n].Id] = val
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
if __name__ == "__main__":

    # Create a blank category
    p = Category()
    print p

    p.setValueByIndex(0, 33)
    print p

    # Set all fields to defaults
    p.setDefaults()
    print p

    # Print as an SQL cmd
    print p.makeRecord()

    # Populate the category from a list
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
    #print p.exists("Category #")
    #print p.exists("CategoryNo")

