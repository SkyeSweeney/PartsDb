
import sqlite3
import doctest
import time
import types
import Part
import Category



#######################################################################
#
#######################################################################
class Database():


    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self):
        self.templatePart      = Part.Part()
        self.templateCategory  = Category.Category()
        self.numPartFields     = self.templatePart.getNumFields()
        self.numCategoryFields = self.templateCategory.getNumFields()
        self.dbOpen = False
    #
  
  
    ###################################################################
    # Open the database file
    ###################################################################
    def OpenDataBase(self, name):  

        if (self.dbOpen):
            print "DB already open"
            return
        #
  
        # Connect the database
        self.conn = sqlite3.connect(name, isolation_level="EXCLUSIVE")
  
        # Create the 'cursor' for access
        self.c = self.conn.cursor()
  
        # Determine if PartsTbl exists
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PartsTbl'")
        exists = self.c.fetchone()
    
        # If it does not, create it
        if (not exists):
            print "Could not find db file. Creating new one"
            self.CreateDataBase()
        #

        self.dbOpen = True
    #
  
    ###################################################################
    # Create a blank database
    ###################################################################
    def CreateDataBase(self):  

        cmd = "CREATE TABLE PartsTbl("

        for i in range(self.numPartFields):
            fld = self.templatePart.getFieldInfo(i)
            n = fld.SqlName # field name
            t = fld.SqlType # field type
            cmd = cmd + "%s %s," % (n, t)
        #
        cmd = cmd[:-1] + ")"

        self.c.execute(cmd)
        self.conn.commit()
  
        # Create the Category table (FET, Sensor, ...)
        cmd = "CREATE TABLE CategoryTbl("

        for i in range(self.numCategoryFields):
            fld = self.templateCategory.getFieldInfo(i)
            n = fld.SqlName # field name
            t = fld.SqlType # field type
            cmd = cmd + "%s %s," % (n, t)
        #
        cmd = cmd[:-1] + ")"

        self.c.execute(cmd)
        self.conn.commit()
  
        # Create the Project table (Sailboat timer, Energy monitor, ...)
        cmd = "CREATE TABLE ProjectTbl(ProjectID INTEGER PRIMARY KEY, " +\
                                       "Project   text)"
        self.c.execute(cmd)
        self.conn.commit()
    #
  
    ###################################################################
    #
    ###################################################################
    def CloseDataBase(self):  
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        self.conn.close()
        self.dbOpen = False
    #
  
    ###################################################################
    #
    ###################################################################
    def StartTransaction(self):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "BEGIN TRANSACTION"
        try:
            self.c.execute(cmd)
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #
  
    ###################################################################
    #
    ###################################################################
    def EndTransaction(self):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "COMMIT"
        try:
            self.c.execute(cmd)
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #
  
  
    ###################################################################
    #
    ###################################################################
    def AbortTransaction(self):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "ROLLBACK"
        try:
            self.c.execute(cmd)
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #




  
    ###################################################################
    #
    ###################################################################
    def GetAllParts(self):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "SELECT * FROM PartsTbl;"
        try:
            rows = []
            for row in self.c.execute(cmd):
                rows.append(row)
            #
        except sqlite3.Error as e:
            print e.args[0]
        #

        return rows  
    #
  
    ###################################################################
    #
    ###################################################################
    def GetPartBy(self, field, value):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "SELECT * FROM PartsTbl WHERE %s == %s" % (field, str(value))
        try:
            rows = []
            for row in self.c.execute(cmd):
                rows.append(row)
            #
        except sqlite3.Error as e:
            print e.args[0]
        #

        return rows  
    #
  
    ###################################################################
    #
    ###################################################################
    def AddPart(self, part, commit=True):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "INSERT INTO PartsTbl VALUES (%s)" % (part.makeRecord())
        try:
            self.c.execute(cmd)
            if commit:
                self.conn.commit()
            #
            
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #
  
    ###################################################################
    #
    ###################################################################
    def DelPart(self, myPartNum, commit=True):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "DELETE FROM PartsTbl WHERE PartNo=%s" % (myPartNum)
        try:
            self.c.execute(cmd)
            if commit:
                self.conn.commit()
            #
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #
  
    ###################################################################
    #
    ###################################################################
    def UpdatePart(self, myPartNum, lst, commit=True):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #

        # Create command
        setStr = "SET "
        flds = self.GetPartAllFieldInfo()
        for iFld in range(len(flds)):
            if (type(lst[iFld]) is types.IntType):
                setStr = setStr + "%s=%d," %(flds[iFld].SqlName,lst[iFld])
            else:                
                setStr = setStr + '%s="%s",' %(flds[iFld].SqlName,lst[iFld])
            #
        #
        setStr = setStr[:-1]
        cmd = "UPDATE PartsTbl %s WHERE PartNo=%s" % (setStr,myPartNum)

        # Execute the command
        try:
            self.c.execute(cmd)
            if commit:
                self.conn.commit()
            #
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #


    ###################################################################
    # 
    ###################################################################
    def GetNumPartFields(self):  
        return self.numPartFields
    #

    ###################################################################
    # Get all a list of field info for all parts
    ###################################################################
    def GetPartAllFieldInfo(self):  
        return self.templatePart.getAllFieldInfo()
    #

    ###################################################################
    # Get field info for a given field
    ###################################################################
    def GetPartFieldInfo(self, i):  
        return self.templatePart.getFieldInfo(i)
    #




  
    ###################################################################
    #
    ###################################################################
    def GetAllCategorys(self):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "SELECT * FROM CategoryTbl;"
        try:
            rows = []
            for row in self.c.execute(cmd):
                rows.append(row)
            #
        except sqlite3.Error as e:
            print e.args[0]
        #

        return rows  
    #
  
    ###################################################################
    #
    ###################################################################
    def GetCategoryBy(self, field, value):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "SELECT * FROM CategoryTbl WHERE %s == %s" % (field, str(value))
        try:
            rows = []
            for row in self.c.execute(cmd):
                rows.append(row)
            #
        except sqlite3.Error as e:
            print e.args[0]
        #

        return rows  
    #
  
    ###################################################################
    #
    ###################################################################
    def AddCategory(self, category, commit=True):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "INSERT INTO CategoryTbl VALUES (%s)" % (category.makeRecord())
        try:
            self.c.execute(cmd)
            if commit:
                self.conn.commit()
            #
            
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #
  
    ###################################################################
    #
    ###################################################################
    def DelCategory(self, myCategoryNo, commit=True):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "DELETE FROM CategoryTbl WHERE CategoryNo=%s" % (myCategoryNo)
        try:
            self.c.execute(cmd)
            if commit:
                self.conn.commit()
            #
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #
  
    ###################################################################
    #
    ###################################################################
    def UpdateCategory(self, myCategoryNo, lst, commit=True):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #

        # Create command
        setStr = "SET "
        flds = self.GetCategoryAllFieldInfo()
        for iFld in range(len(flds)):
            if (type(lst[iFld]) is types.IntType):
                setStr = setStr + "%s=%d," %(flds[iFld].SqlName,lst[iFld])
            else:                
                setStr = setStr + '%s="%s",' %(flds[iFld].SqlName,lst[iFld])
            #
        #
        setStr = setStr[:-1]
        cmd = "UPDATE CategoryTbl %s WHERE CategoryNo=%s" % (setStr,myCategoryNo)

        # Execute the command
        try:
            self.c.execute(cmd)
            if commit:
                self.conn.commit()
            #
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #


    ###################################################################
    # 
    ###################################################################
    def GetNumCategoryFields(self):  
        return self.numCategoryFields
    #

    ###################################################################
    # Get all a list of field info for all parts
    ###################################################################
    def GetCategoryAllFieldInfo(self):  
        return self.templateCategory.getAllFieldInfo()
    #

    ###################################################################
    # Get field info for a given field
    ###################################################################
    def GetCategoryFieldInfo(self, i):  
        return self.templateCategory.getFieldInfo(i)
    #
  
#
