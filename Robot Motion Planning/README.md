# PRM 

See `report.md` for the full write up on this project. For testing on the kinematics and robot arm drawing, run `robot.py`. For testing on the full PRM, see `PRM.py`. 

At the bottom of the `PRM.py` file, you can choose from a few obstacle sets that I've created, as well as a few robot sample problems. Comment and uncomment these to see the PRM in action. Also note that it takes parameters for sampling density, dimensionality of the robot arm, etc. Change these and rerun if you'd like. 

**NOTE**: Make sure to delete the import statement for the nearest neighbors library if you don't have it installed. The program isn't set to use this library by default, but I did leave the import statement for my own convinience. This will just cause an error message if you don't have it, which will make running the code more of a pain. In this case, just delete it. 