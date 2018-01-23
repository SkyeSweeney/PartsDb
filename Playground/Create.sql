
-- Create the parts table
CREATE TABLE IF NOT EXISTS part (
	id          INTEGER PRIMARY KEY,
	name        TEXT NOT NULL,
	description TEXT NOT NULL,
	category    INTEGER
        );

-- Create the Categorys table
CREATE TABLE if NOT EXISTS category (
	id INTEGER PRIMARY KEY,
	name       TEXT NOT NULL
        );

-- Create projects
CREATE TABLE if NOT EXISTS project (
	id INTEGER PRIMARY KEY,
	name       TEXT NOT NULL
        );

-- Create table to link parts to projects
CREATE TABLE if NOT EXISTS partProject (
	id     INTEGER PRIMARY KEY,
	partId INTEGER,
	projectId INTEGER,
	FOREIGN KEY(partId)    REFERENCES part(id),
	FOREIGN KEY(projectId) REFERENCES project(id)
        );

-- Clear the tables
DELETE FROM category;
DELETE FROM project;
DELETE FROM part;
DELETE FROM partProject;


-- Add some categories
INSERT INTO category (id,name) VALUES (null, "None");
INSERT INTO category (id,name) VALUES (null, "NPN Transistor");
INSERT INTO category (id,name) VALUES (null, "PNP Transistor");
INSERT INTO category (id,name) VALUES (null, "FET Transistor");
INSERT INTO category (id,name) VALUES (null, "Sensor");
INSERT INTO category (id,name) VALUES (null, "Processor");
INSERT INTO category (id,name) VALUES (null, "Diode");
INSERT INTO category (id,name) VALUES (null, "Resistor");
INSERT INTO category (id,name) VALUES (null, "Capacitor");
.print
.print category table
SELECT * from category;


-- Add some projects
INSERT INTO project (id,name) VALUES (null, "None");
INSERT INTO project (id,name) VALUES (null, "SailTimer");
INSERT INTO project (id,name) VALUES (null, "Clock");
INSERT INTO project (id,name) VALUES (null, "HealthBuddy");
INSERT INTO project (id,name) VALUES (null, "PowerMonitor");
INSERT INTO project (id,name) VALUES (null, "None");
INSERT INTO project (id,name) VALUES (null, "FurnaceMonitor");
.print
.print Project table
SELECT * from project;


--------------------------------------------------------------
-- Add some parts with links to categories
--------------------------------------------------------------


-- ADE7763 (is a sensor ond used by PowerMonitor)
INSERT INTO part (id,name,description) VALUES (null, "ADE7763", "RMS Power Monitor");
UPDATE part set category=(select id from category where name="Sensor") where name="ADE7763";
INSERT into partProject (id) VALUES (1);
UPDATE partProject set projectId=(select id from project where name="PowerMonitor") where id=1;
UPDATE partProject set partId=(select id from part where name="ADE7763") where id=1;

-- 10K resistor (is a resister and used by many projects)
INSERT INTO part (id,name,description) VALUES (null, "10K", "10K resistor 5%");
UPDATE part set category=(select id from category where name="Resistor") where name="10K";
INSERT into partProject (id) VALUES (2);
UPDATE partProject set projectId=(select id from project where name="PowerMonitor") where id=2;
UPDATE partProject set partId=(select id from part where name="10K") where id=2;
INSERT into partProject (id) VALUES (3);
UPDATE partProject set projectId=(select id from project where name="SailTimer") where id=3;
UPDATE partProject set partId=(select id from part where name="10K") where id=3;
INSERT into partProject (id) VALUES (4);
UPDATE partProject set projectId=(select id from project where name="FurnaceMonitor") where id=4;
UPDATE partProject set partId=(select id from part where name="10K") where id=4;


-- 2N2222A
INSERT INTO part (id,name,description) VALUES (null, "2N2222A", "Transistor");
UPDATE part set category=(select id from category where name="NPN Transistor") where name="2N2222A";
INSERT into partProject (id) VALUES (5);
UPDATE partProject set projectId=(select id from project where name="SailTimer") where id=5;
UPDATE partProject set partId=(select id from part where name="2N2222A") where id=5;

-- Simple selects
.print
.print part table
SELECT * from part;
.print
.print partProject table
SELECT * from partProject;


-- Complex selects
.print
.print Part with text category
SELECT part.name, part.description FROM part INNER JOIN category on category.id = part.category;


.print
.print AAAA
SELECT part.name, category.name FROM part, category WHERE part.id = category.id;



.print
.print BBBB
SELECT part.name, project.name, category.name 
FROM part, project, partProject, category 
WHERE partProject.partId=part.id AND 
      partProject.projectId=project.id AND 
      part.category=category.id;

