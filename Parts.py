
import sqlite3
import doctest
import time
import Part



#######################################################################
#
#######################################################################
class Parts():


    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self):
        pass
    #
  
  
    ###################################################################
    # Open the database file
    ###################################################################
    def OpenDataBase(self):  
  
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
    #
  
    ###################################################################
    # Create a blank database
    ###################################################################
    def CreateDataBase(self):  

        part = Part.Part()
        n = part.getSqlFieldName(0)
        cmd = "CREATE TABLE PartsTbl("

        for i in range(part.getNumFields()):
            n = part.getSqlFieldName(i)   # field name
            t = part.getFields(i)[3]      # field type
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
        self.conn.close()
    #
  
    ###################################################################
    #
    ###################################################################
    def GetAllRecords(self):
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
        cmd = "SELECT * FROM PartsTbl WHERE %s == %s" % (field, str(value))
        print cmd
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
        cmd = "INSERT INTO PartsTbl VALUES (%s)" % (part.makeRecord())
        print cmd
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
        cmd = "DELETE FROM PartsTbl WHERE MyPartNum=%s" % (myPartNum)
        try:
          self.c.execute(cmd)
          if commit:
            self.conn.commit()
        except sqlite3.Error as e:
          print __name__, e.args[0]
    #
  
    ###################################################################
    #
    ###################################################################
    def StartTransaction(self):
        cmd = "BEGIN TRANSACTION"
        try:
            self.c.execute(cmd)
        except sqlite3.Error as e:
            print __name__, e.args[0]
    #
  
    ###################################################################
    #
    ###################################################################
    def EndTransaction(self):
        cmd = "COMMIT"
        try:
            self.c.execute(cmd)
        except sqlite3.Error as e:
            print __name__, e.args[0]
    #
  
  
    ###################################################################
    #
    ###################################################################
    def AbortTransaction(self):
        cmd = "ROLLBACK"
        try:
            self.c.execute(cmd)
        except sqlite3.Error as e:
            print __name__, e.args[0]
    #
  
    ###################################################################
    #
    ###################################################################
    def AddCategory(self, name):
        cmd = 'INSERT INTO CategoryTbl(Class) VALUES ("%s")' % (name)
        print cmd
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
        cmd = "DELETE FROM CategoryTbl WHERE Class=%s" % (name)
        try:
            self.c.execute(cmd)
            self.conn.commit()
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #
    #
  
#
