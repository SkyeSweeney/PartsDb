
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

        # Populate part
        part.setValueByIndex(i, str(i))
    #

    # Add the record
    print "111"
    db.AddRecord(part, commit=True)
    print "222"

    db.EndTransaction()
    print "333"

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
    time.sleep(2.00)
