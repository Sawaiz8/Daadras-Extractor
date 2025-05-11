The following folder has a main.py file which currently is based on user-terminal interaction
It can changed aftwerward by simply adding some sort of user interface to get values
currently, these are the only functions it can do:
- insertions to each table
- migrations using alembic
  - add new email column to students
  - delete the mid name column from students
  - change the data type of phonenumber in volunters, from string to bigint
  - (these migrations can be altered as per new requirements)
