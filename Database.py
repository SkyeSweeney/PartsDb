
import sqlite3
import doctest
import time
import types
import Part
import Category
import Project



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
        self.templateProject   = Project.Project()
        self.numPartFields     = self.templatePart.getNumFields()
        self.numCategoryFields = self.templateCategory.getNumFields()
        self.numProjectFields  = self.templateProject.getNumFields()
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

        # Create the Parts tabel (2N2222A, ADE7763, ...)
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
  
        # Create the Project table (SailboatTimer, PowerMonitor, ...)
        cmd = "CREATE TABLE ProjectTbl("

        for i in range(self.numProjectFields):
            fld = self.templateProject.getFieldInfo(i)
            n = fld.SqlName # field name
            t = fld.SqlType # field type
            cmd = cmd + "%s %s," % (n, t)
        #
        cmd = cmd[:-1] + ")"

        self.c.execute(cmd)
        self.conn.commit()

        # Create the PartsProject table (Joins parts and projects)
        cmd = "CREATE    TABLE Parts2Projects("\
              "id        INTEGER PRIMARY KEY,"\
	      "partId    INTEGER,"\
	      "projectId INTEGER,"\
	      "FOREIGN KEY(partId)    REFERENCES part(id),"\
	      "FOREIGN KEY(projectId) REFERENCES project(id))"

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
        cmd = "INSERT INTO PartsTbl (%s) VALUES (%s)" % (part.makeSelect(), part.makeValue())
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




  
    ###################################################################
    #
    ###################################################################
    def GetAllProjects(self):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "SELECT * FROM ProjectTbl;"
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
    def GetProjectBy(self, field, value):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "SELECT * FROM ProjectTbl WHERE %s == %s" % (field, str(value))
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
    def AddProject(self, project, commit=True):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "INSERT INTO ProjectTbl VALUES (%s)" % (project.makeRecord())
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
    def DelProject(self, myProjectNo, commit=True):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "DELETE FROM ProjectTbl WHERE ProjectNo=%s" % (myProjectNo)
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
    def UpdateProject(self, myProjectNo, lst, commit=True):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #

        # Create command
        setStr = "SET "
        flds = self.GetProjectAllFieldInfo()
        for iFld in range(len(flds)):
            if (type(lst[iFld]) is types.IntType):
                setStr = setStr + "%s=%d," %(flds[iFld].SqlName,lst[iFld])
            else:                
                setStr = setStr + '%s="%s",' %(flds[iFld].SqlName,lst[iFld])
            #
        #
        setStr = setStr[:-1]
        cmd = "UPDATE ProjectTbl %s WHERE ProjectNo=%s" % (setStr,myProjectNo)

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
    def GetNumProjectFields(self):  
        return self.numProjectFields
    #

    ###################################################################
    # Get all a list of field info for all parts
    ###################################################################
    def GetProjectAllFieldInfo(self):  
        return self.templateProject.getAllFieldInfo()
    #

    ###################################################################
    # Get field info for a given field
    ###################################################################
    def GetProjectFieldInfo(self, i):  
        return self.templateProject.getFieldInfo(i)
    #
  
#
