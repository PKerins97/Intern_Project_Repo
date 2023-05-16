# TERMINAL REQUIRED

Go inside `<project>` folder to simplify commands (once you have environment running, you wont need to use outside folder).
To start server, run `py manage.py runserver`

To add new app
`py manage.py startapp <new app name>`

Once you add new app (new folder in project), go to `<project(same name)>/settings.py` and add
`<new app name>` to the list of `INSTALLED_APPS`.

Now run `py manage.py migrate`.

New Models - database tables are added in `<app>/models.py`.
Once you add new class (database), run
`py manage.py makemigrations <class name>`
`py manage.py migrate`

As a side-note: you can view the SQL statement that were executed from the migration above. All you have to do is to run this command, with the migration number:
`py manage.py sqlmigrate <appname> 0001`


To open python shell and work with database:
`py manage.py shell`
`>>> from <app name>.models import <tablename>`

To see records in the database:
`>>> <Class.objects.all().values()>`

To add records to the database:
`>>> newobject = <Class>( <...> )`
`>>> newobject.save()`

Update Records:
`>>> x = <Class>.objects.all()[<index>]`
`... update`
`>>> x.save()`

Delete Records:
`>>> x = <Class.objects.all()[<index>]>`
`>>> x.delete()`

Update Model
`...update models.py` (allow null values for better override)
`py manage.py makemigrations <app-name>`
`py manage.py migrate`