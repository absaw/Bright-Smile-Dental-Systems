# Set of Important Commands

## Git

`git add . git commit -m "" git pull`

`git push origin`

`git push origin branch-1`

`git branch -a`

Create and switch to a new branch:
`git checkout -b new-feature-branch`

Merging steps
`git checkout main`
`git merge branch-1`
`git push origin main`

## PLSQL

To open a particular database belonging to a particular user

`psql postgres://postgres@localhost:5432/postgres`

For info about session:

`\conninfo`

For quitting

`\q`

For list of databases

`\l`

From next time, just use

`psql`

`CREATE DATABASE bright_smile_dental;`

## Django

Querying the database

`python manage.py shell`

`from clinic.models import Clinic`
