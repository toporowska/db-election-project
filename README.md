# election
This is the final project of Data Bases course I took.

The task was to write a program to manage student council elections. 
There were to be two types of users: election commitee and voters. Voters are students so they have their index numbers.

The task didn't include secure user authentication so it's very trivial. There are some students already registered in the database created by db.py file (the list of their fake names is in the included files). They able to log in using their index number as a username. The password for each student is 'voter'. Commitee's username and password are 'commitee'.

The voters can vote, nominate new candidates and see election results. Commitee can register new voters and elections and publish results, as well as see candidates, voters, elections and results lists.

The program connects to the remote database available only for my univeristies students so I also included a verision of if running locally.
