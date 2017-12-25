
import sys
sys.path.insert(0, '..')
import sqlite3
import doctest
import time
import Part
import Parts
import os
import Fields





if __name__ == "__main__":

    # Delete the SQlite database file if it exists
    try:
        os.remove("parts.db")
    except:
        pass

    # Open the database
    db = Parts.Parts()
    db.OpenDataBase()  

    # Create a blank part
    part = Part.Part()

    # Start a transaction
    db.StartTransaction()

    # for each field in part
    for i in range(part.getNumFields()):

        t = part.getFields(i)[3]   # Type
        n = part.getFields(i)[1]   # Sql Name

        if ("TEXT" in t):
            part.setValueByIndex(i, "F-%s-%d"%(n,i))
        elif ("INTEGER" in t):
            part.setValueByIndex(i, i)
        else:
            pass
        #

    #

    # Add the record
    db.AddRecord(part, commit=False)
    part.setValueByIndex(0, 1)
    db.AddRecord(part, commit=False)
    part.setValueByIndex(0, 2)
    db.AddRecord(part, commit=False)
    part.setValueByIndex(0, 3)
    db.AddRecord(part, commit=False)
    part.setValueByIndex(0, 4)
    db.AddRecord(part, commit=False)

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
