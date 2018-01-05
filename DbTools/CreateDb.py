
import sys
sys.path.insert(0, '..')
import sqlite3
import doctest
import time
import Part
import Database
import os
import Fields





if __name__ == "__main__":

    # Delete the SQlite database file if it exists
    try:
        os.remove("parts.db")
    except:
        pass

    # Open the database
    db = Database.Database()
    db.OpenDataBase()  

    # Create a blank part
    part = Part.Part()

    # Start a transaction
    db.StartTransaction()

    # add a few sample records
    for iRow in range(10):

        # for each field in part
        for iCol in range(part.getNumFields()):

            t = part.getFields(iCol)[3]   # Type
            n = part.getFields(iCol)[1]   # Sql Name

            if ("TEXT" in t):
                part.setValueByIndex(iCol, "F-%s-%d"%(n,iRow))
            elif ("INTEGER" in t):
                part.setValueByIndex(iCol, iRow)
            else:
                pass
            #

        #
        db.AddRecord(part, commit=False)
    #

    db.EndTransaction()

    # Add some classes to the DB
    db.AddCategory("Opto")
    db.AddCategory("Amp")
    db.AddCategory("Regulator")
    db.AddCategory("Passive")
    db.AddCategory("Mechanical")
    db.AddCategory("Transistor")
    db.AddCategory("Micro")
    db.AddCategory("Memory")
    db.AddCategory("Linear")

    # Close the database
    db.CloseDataBase()  

    print "Done"
