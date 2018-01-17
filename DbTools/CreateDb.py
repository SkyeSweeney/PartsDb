
import sys
sys.path.insert(0, '..')
import sqlite3
import doctest
import time
import os

import Part
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
