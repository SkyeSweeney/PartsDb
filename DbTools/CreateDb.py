
import sys
sys.path.insert(0, '..')
import sqlite3
import doctest
import time
import os

import Part
import Category
import Project
import Database





if __name__ == "__main__":

    # Delete the SQlite database file if it exists
    try:
        os.remove("parts.db")
    except:
        pass

    # Open the database
    db = Database.Database()
    db.OpenDataBase("Parts.db")  

    # Create a blank part
    part = Part.Part()

    # Start a transaction
    db.StartTransaction()

    # add a few sample records
    for iRow in range(30):

        # for each field in part
        for iFld in range(part.getNumFields()):

            t = part.getFieldInfo(iFld).SqlType   # Type
            n = part.getFieldInfo(iFld).SqlName   # Sql Name

            if ("TEXT" in t):
                part.setValueByIndex(iFld, "F-%s-%d"%(n,iRow))
            elif ("INTEGER" in t):
                part.setValueByIndex(iFld, iRow)
            else:
                pass
            #

        #
        db.AddPart(part, commit=False)
    #

    db.EndTransaction()



    # Add some Categories to the DB

    # Create a blank category
    category = Category.Category()
    category.setFromList([0,"Opto-0","Desc-0","Notes-0"])
    db.AddCategory(category)
    category.setFromList([1,"FETS-1","Desc-1","Notes-1"])
    db.AddCategory(category)


    # Add some Projects to the DB

    # Create a blank project
    project = Project.Project()
    project.setFromList([0,"SailTimer","Desc-0","Notes-0"])
    db.AddProject(project)
    project.setFromList([1,"PowerMonitor","Desc-1","Notes-1"])
    db.AddProject(project)


    # Close the database
    db.CloseDataBase()  

    print "Done"
