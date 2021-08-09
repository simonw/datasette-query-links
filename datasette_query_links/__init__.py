from datasette import hookimpl
from datasette.utils.sqlite import sqlite3
import markupsafe
import re
import urllib.parse


async def is_valid_select(db, sql):
    sql = sql.strip().rstrip(";")
    outer_sql = "explain {}".format(sql)
    try:
        await db.execute(outer_sql)
        return True
    except sqlite3.DatabaseError:
        return False


starts_with_select_re = re.compile(r"^\s*select\s")


@hookimpl
def render_cell(value, database, datasette):
    async def inner():
        if value and isinstance(value, str) and starts_with_select_re.match(value):
            db = datasette.get_database(database)
            if await is_valid_select(db, value):
                path = (
                    datasette.urls.database(database)
                    + "?"
                    + urllib.parse.urlencode(
                        {
                            "sql": value,
                        }
                    )
                )
                return markupsafe.Markup(
                    '<a href="{}">{}</a>'.format(
                        markupsafe.escape(path), markupsafe.escape(value)
                    )
                )

    return inner
