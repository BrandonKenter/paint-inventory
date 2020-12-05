# Paint-Inventory
When I worked as a sprayer at an interior millwork company, one of the biggest time wasters we encountered was the lack of a paint management system. The two main issues this caused was us constantly not being able to find paint as well as finding out too late that we didn't have enough paint for a job. This desktop application solves these two problems by keeping track of paint location details and the quantity of the paint. Additional searching functionality, as described below, allows a user of the application to quickly see which paints are in need of immediate restocking. 

# Getting Started
To run the application, start by downloading PaintManager.rar. Extract the files and open the PaintManager folder. Then launch PaintManager.exe. 

# Using the App
General details:
- The data for each paint is stored in an embedded database using SQLite. 
- Starting data is pre-loaded into the database

Inventory Details Tab:
- Click 'Refresh' to load the database with the inventory of paints
- Click 'Search' to search for paints under a certain gallon amount

Inventory Statistics Tab:
- Click 'Check' to show the 3 highest and lowest volume paints

Edit Inventory Tab:
- Use the arrows to navigate the database of paints
- Edit the fields and click 'Update' to update an existing entry
- Edit the fields and click 'Add' to add a new entry
- Click 'Delete' to delete an entry

# Preview
![alt text](https://i.gyazo.com/c5c76121acebc454c417d6b3c81bcd8e.png)
