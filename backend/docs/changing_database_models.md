How to make changes in database models?
---------------------------------------

For SQL database models we are using SQLAlchemy with Alembic as engine for all migrations.

### Create new migration

Once you've prepared a change in your database models, now it's time to create a migration file.
To do so, you can use Alembic's autogeneration feature:

```bash
$ . ./devenv.sh
(venv) $ alembic revision --autogenerate -m "Your short description message"
```

Then you can check what's happened inside of your generated migration inside of `alembic/versions`
directory.

**Important!** Always check if Alembic generated your migration properly! It may not work if you've
changed significant part of the whole database! What's more, keep in mind that you've got to
manually write data migration code (eg. moving data from one table to a separate table).

### Running your migration

Once you've prepared a database schema migration file, it's time to run it on your database. Use
below command to do so:

```bash
(venv) $ alembic upgrade head
```

This will upgrade your database to the newest version of the schema. But you can always move only
one step into the future by:

```bash
(venv) $ alembic upgrade +1
```

And the same goes if you want to go one step back:

```bash
(venv) $ alembic downgrade -1
```

### Where am I?

You can always check which version of the schema you're using by:

```bash
(venv) $ alembic current
```

And keep in mind that you can check all available migrations with:

```bash
(venv) $ alembic history
```
