
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
    #

    # Open the database
    db = Database.Database()
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
    category.setFromList([0,"N-BJT","Transistors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"P-BJT","Transistors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Sensor","Sensors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Resistors","Resistors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Capacitors","Capacitors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Small Signal Diodes","Diodes","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Power Diodes","Diodes","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Processors","Processors","Notes"])
    db.AddCategory(category)
    category.setFromList([0,"Memory","Memory","Notes"])
    db.AddCategory(category)


    #############################
    # Add some Projects to the DB
    #############################

    # Create a blank project
    project = Project.Project()
    project.setFromList([0,"SailTimer","Desc-0",""])
    db.AddProject(project)
    project.setFromList([0,"PowerMonitor","Desc-1",""])
    db.AddProject(project)
    project.setFromList([0,"GE-Clock","Pitch augmentation computer clock",""])
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
    part.setFromList(0,
                     "//file:/masterdocs/skye/datasheets/transistors/2N2222A.pdf",
                     "Fairchild",
                     "2N2222A",
                     "www.fairchild.com/ddd",
                     "digikey",
                     "2N2222A-ND",
                     "www.digikey.com/kdkdkdk",
                     "33",
                     "5",
                     "2N2222A",
                     "NPN transistor",
                     "Blue bin",
                     "None")
    id = db.AddPart(part, commit=False)
    # Add Category(s)
    db.AddCategory(id, "NPN transistor")
    # Add Project(s)
    db.AddProject(id, "Sail Timer")


    # Close the database
    db.CloseDataBase()  

    print "Done"
