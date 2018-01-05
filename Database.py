
import sqlite3
import doctest
import time
import Part
import Fields



#######################################################################
#
#######################################################################
class Database():


    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self):
        self.templatePart = Part.Part()
        self.numPartFields = self.templatePart.getNumFields()
        self.dbOpen = False
        self.fields = Fields.Fields()
    #
  
  
    ###################################################################
    # Open the database file
    ###################################################################
    def OpenDataBase(self):  

        if (self.dbOpen):
            print "DB already open"
            return
        #
  
        # Connect the database
        self.conn = sqlite3.connect('parts.db', isolation_level="EXCLUSIVE")
  
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
            n = self.templatePart.getSqlFieldName(i)   # field name
            t = self.templatePart.getFields(i)[3]      # field type
            cmd = cmd + "%s %s," % (n, t)
        #
        cmd = cmd[:-1] + ")"

        self.c.execute(cmd)
        self.conn.commit()
  
        # Create the Category table (FET, Sensor, ...)
        cmd = "CREATE TABLE CategoryTbl(CategoryID INTEGER PRIMARY KEY, " +\
                                        "Class   text)"
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
    def GetAllRecords(self):
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
    def GetRecordBy(self, field, value):
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
    def AddRecord(self, part, commit=True):
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
    def DelRecord(self, myPartNum, commit=True):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "DELETE FROM PartsTbl WHERE MyPartNum=%s" % (myPartNum)
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
    def AddCategory(self, name):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = 'INSERT INTO CategoryTbl(Class) VALUES ("%s")' % (name)
        try:
            self.c.execute(cmd)
            self.conn.commit()
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #
  
    ###################################################################
    #
    ###################################################################
    def GetCategory(self):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "SELECT * FROM CategoryTbl"
        try:
            classes = []
            for row in self.c.execute(cmd):
                classes.append(row)
            #
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
        return classes  
    #
  
    ###################################################################
    #
    ###################################################################
    def DelCategory(self, name):
        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "DELETE FROM CategoryTbl WHERE Class=%s" % (name)
        try:
            self.c.execute(cmd)
            self.conn.commit()
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
    # 
    ###################################################################
    def GetPartFields(self):  
        return self.templatePart.getFields()
    #

    ###################################################################
    # 
    ###################################################################
    def GetPartFieldInfo(self, i):  
        return self.templatePart.getFields(i)
    #
  
#
