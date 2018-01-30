
import sqlite3
import doctest
import time
import types
import Part
import Category
import Project

import sys
import os



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
            p = self.templatePart
            n = p.sqlNames[i] # field name
            t = p.sqlTypes[i] # field type
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

        # Create the Parts2Project table (Joins parts and projects)
        cmd = "CREATE    TABLE Part2Project("\
              "Id        INTEGER PRIMARY KEY,"\
	      "PartId    INTEGER,"\
	      "ProjectId INTEGER,"\
	      "FOREIGN KEY(partId)    REFERENCES part(PartId),"\
	      "FOREIGN KEY(projectId) REFERENCES project(ProjectId))"

        self.c.execute(cmd)
        self.conn.commit()

        # Create the Part2Category table (Joins parts and categories)
        cmd = "CREATE     TABLE Part2Category("\
              "Id         INTEGER PRIMARY KEY,"\
	      "PartId     INTEGER,"\
	      "CategoryId INTEGER,"\
	      "FOREIGN KEY(partId)     REFERENCES PartTbl(PartId),"\
	      "FOREIGN KEY(categoryId) REFERENCES CategoryTbl(CategoryId))"

        self.c.execute(cmd)
        self.conn.commit()
    #
  
    ###################################################################
    # Close the database
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
    # Start a transaction
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
    # Close a transaction
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
    # Abort a transaction
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
    # Get a list of all parts
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
            print __name__, e.args[0]
        #

        return rows  
    #
  
    ###################################################################
    # Get a part by a given field name and its value
    ###################################################################
    def GetPartByFieldValue(self, field, value):

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
            print __name__, e.args[0]
        #

        return rows  
    #
  
    ###################################################################
    # Add a new part
    # Return the id of this new part
    ###################################################################
    def AddPart(self, part, commit=True):
        retval = 0

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
            retval = self.c.lastrowid
            
        except sqlite3.Error as e:
            print __name__, e.args[0]
            retval = 0
        #

        return retval

    #
  
    ###################################################################
    # Delete a part
    ###################################################################
    def DelPart(self, myPartNum, commit=True):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #
        cmd = "DELETE FROM PartsTbl WHERE PartId=%s" % (myPartNum)
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
    # Update a part from a full list
    ###################################################################
    def UpdatePart(self, myPartNum, lst, commit=True):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #

        # Create command
        setStr = "SET "
        part = self.GetPartTemplate()
        for iFld in range(self.numPartFields):
            if (type(lst[iFld]) is types.IntType):
                setStr = setStr + "%s=%d," %(part.sqlNames[iFld],lst[iFld])
            else:                
                setStr = setStr + '%s="%s",' %(part.sqlNames[iFld],lst[iFld])
            #
        #
        setStr = setStr[:-1]
        cmd = "UPDATE PartsTbl %s WHERE PartId=%s" % (setStr,myPartNum)

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
    def GetPartTemplate(self):  
        return self.templatePart
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
            print __name__, e.args[0]
        #

        return rows  
    #
  
    ###################################################################
    #
    ###################################################################
    def GetCategoryByFieldValue(self, field, value):

        if (not self.dbOpen):
            print "DB is not open"
            return
        #

        cmd = "SELECT * FROM CategoryTbl WHERE %s == '%s'" % (field, str(value))
        try:
            rows = []
            for row in self.c.execute(cmd):
                rows.append(row)
            #
        except sqlite3.Error as e:
            print __name__, e.args[0]
        #

        return rows  
    #
  
    ###################################################################
    # Get a Category ID by its name
    ###################################################################
    def GetCategoryIdByName(self, name):

        retval = 0

        if (not self.dbOpen):
            print "DB is not open"
            return
        #

        cmd = "SELECT CategoryId FROM CategoryTbl WHERE name == '%s'" % (name)
        try:
            rows = []
            result = self.c.execute(cmd)
            for row in result:
                rows.append(row)
            #
        except sqlite3.Error as e:
            print __name__, e.args[0]
            retval = 0
        #

        # Insure we only got one and only one answer
        if (len(rows) == 0):
            print "Category", name, "not found"
            retval = 0
        elif (len(rows) > 1):
            print "Category", name, "found more than once"
            retval = 0
        else:
            retval = rows[0][0]
        #

        return retval  
    #
  
    ###################################################################
    # Add a new category
    # Return new ID
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
            retval = self.c.lastrowid
            
        except sqlite3.Error as e:
            print __name__, e.args[0]
            retval = 0
        #

        return retval
    #
  
    ###################################################################
    # Delete a category by id
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
    # Update a category with a full list
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
    # Get a list of all projects
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
            print __name__, e.args[0]
        #

        return rows  
    #
  
    ###################################################################
    # Get a project by a filed and value
    ###################################################################
    def GetProjectByFieldValue(self, field, value):

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
            print __name__, e.args[0]
        #

        return rows  
    #
  
  
    ###################################################################
    #
    ###################################################################
    def GetProjectIdByName(self, name):

        retval = 0

        if (not self.dbOpen):
            print "DB is not open"
            return
        #

        cmd = "SELECT ProjectId FROM ProjectTbl WHERE name == '%s'" % (name)
        try:
            rows = []
            result = self.c.execute(cmd)
            for row in result:
                rows.append(row)
            #
        except sqlite3.Error as e:
            print __name__, e.args[0]
            retval = 0
        #

        # Insure we only got one and only one answer
        if (len(rows) == 0):
            retval = 0
        elif (len(rows) > 1):
            retval = 0
        else:
            retval = rows[0][0]
        #

        return retval  
    #
  
    ###################################################################
    # Add a project
    # Return the new ID
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
            retval = self.c.lastrowid
            
        except sqlite3.Error as e:
            print __name__, e.args[0]
            retval = 0
        #
        return retval
    #
  
    ###################################################################
    # Delete a project
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
    # Update a project from a full list
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





    ###################################################################
    # Add a project ID to a part
    # Return the entry ID or 0 for error
    ###################################################################
    def AddProjectToPart(self, partId, projectId):

        if (not self.dbOpen):
            print "DB is not open"
            return 0
        #

        if (projectId == 0):
            print "Project ID is invalid"
            return 0

        else:

            # Create command
            cmd = "INSERT INTO Part2Project (Id,PartId,ProjectId) VALUES (null, %d, %d)" % (partId, projectId)

            # Execute the command
            try:
                self.c.execute(cmd)
                self.conn.commit()
            except sqlite3.Error as e:
                print __name__, e.args[0]
            #
            return self.c.lastrowid
        #
    #


    ###################################################################
    #
    # Return the entry ID or 0 for error
    ###################################################################
    def AddCategoryToPart(self, partId, categoryId):

        if (not self.dbOpen):
            print "DB is not open"
            return 0
        #

        if (categoryId == 0):
            print "Category ID is invalid"
            return 0

        else:

            # Create command
            cmd = "INSERT INTO Part2Category (Id,PartId,CategoryId) VALUES (null, %d, %d)" % (partId, categoryId)

            # Execute the command
            try:
                self.c.execute(cmd)
                self.conn.commit()
            except sqlite3.Error as e:
                print __name__, e.args[0]
            #
            return self.c.lastrowid
        #
    #


    ###################################################################
    #
    ###################################################################
    def DeleteProjectFromPart(self, partId, ProjectId):
        pass
    #


    ###################################################################
    #
    ###################################################################
    def DeleteCategoryFromPart(self, partId, CategoryId):
        pass
    #


    ###################################################################
    #
    ###################################################################
    def GetPartCategories(self, partId):
        pass
    #


    ###################################################################
    #
    ###################################################################
    def GetPartProjects(self, partId):
        pass
    #
  
#



if __name__ == "__main__":

    # Delete the SQlite database file if it exists
    try:
        os.remove("parts.db")
    except:
        pass
    #

    # Open the database
    db = Database()
    db.OpenDataBase("Parts.db")  


    ###############################
    # Add some Categories to the DB
    ###############################

    # Create a blank category
    category = Category.Category()
    category.setFromList([0,"Opto","Optical","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"N-FET","Field Effect Transistors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"P-FET","Field Effect Transistors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"NPN Transistor","Transistors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"PNP Transistor","Transistors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Sensor","Sensor","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Resistor","Resistor","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Capacitor","Capacitor","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Small Signal Diode","Diodes","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Power Diode","Diodes","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Processor","Processor","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Memory","Memory","Notes"])
    db.AddCategory(category)


    #############################
    # Add some Projects to the DB
    #############################

    # Create a blank project
    project = Project.Project()
    project.setFromList([0,"Sail Timer","Desc-0",""])
    db.AddProject(project)
    project.setFromList([0,"Power Monitor","Desc-1",""])
    db.AddProject(project)
    project.setFromList([0,"GE Clock","Pitch augmentation computer clock",""])
    db.AddProject(project)
    project.setFromList([0,"Lightning Detector","",""])
    db.AddProject(project)
    project.setFromList([0,"Field Mill","",""])
    db.AddProject(project)
    project.setFromList([0,"Workout Buddy","",""])
    db.AddProject(project)
    project.setFromList([0,"PID Demo","",""])
    db.AddProject(project)

    ################################
    # Add some parts to the database
    ################################

    # Create a blank part
    part = Part.Part()

    # 2N2222A
    part.setFromList((0,
                     "2N2222A",
                     "NPN transistor",
                     33,
                     5,
                     "Blue bin",
                     "Fairchild",
                     "2N2222A",
                     "www.fairchild.com/ddd",
                     "digikey",
                     "2N2222A-ND",
                     "www.digikey.com/kdkdkdk",
                     "//file:/masterdocs/skye/datasheets/transistors/2N2222A.pdf",
                     "None"))
    partId = db.AddPart(part, commit=False)
    print "new part", partId

    # Add Category(s)
    db.AddCategoryToPart(partId, db.GetCategoryIdByName("NPN Transistor"))

    # Add Project(s)
    db.AddProjectToPart(partId, db.GetProjectIdByName("Sail Timer"))

    # Arduino Uno
    part.setFromList((0,
                     "Arduino Uno",
                     "Arduino Uno",
                     4,
                     1,
                     "Blue bin",
                     "Arduino Company",
                     "Arduino Uno",
                     "www.arduino.cc",
                     "Spakfun",
                     "P-0032",
                     "www.sparkfun.com/kdkdkdk",
                     "//file:/masterdocs/skye/datasheets/transistors/2N2222A.pdf",
                     "None"))
    partId = db.AddPart(part, commit=False)
    print "new part", partId

    # Add Category(s)
    db.AddCategoryToPart(partId, db.GetCategoryIdByName("Processor"))

    # Add Project(s)
    db.AddProjectToPart(partId, db.GetProjectIdByName("Power Monitor"))
    db.AddProjectToPart(partId, db.GetProjectIdByName("Field Mill"))


    # Close the database
    db.CloseDataBase()  

    print "Done"

