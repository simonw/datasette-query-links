from bs4 import BeautifulSoup as Soup
from datasette.app import Datasette
from datasette.database import Database
import pytest
import urllib.parse


@pytest.mark.asyncio
@pytest.fixture()
async def ds():
    datasette = Datasette([], memory=True, pdb=True)
    db = datasette.add_database(Database(datasette, memory_name="d"))
    if not (await db.table_exists("foo")):
        await db.execute_write("create table foo (id integer primary key)", block=True)
        await db.execute_write("insert into foo (id) values (1)", block=True)
    return datasette


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "wrap_it,sql,is_link_expected",
    (
        (False, "select 1", False),
        (True, "select 1", True),
        (True, "select this is bad", False),
        (True, "select * from foo", True),
        (True, "select * from foo2", False),
    ),
)
async def test_query_links(ds, wrap_it, sql, is_link_expected):
    if wrap_it:
        final_sql = "select '{}'".format(sql)
    else:
        final_sql = sql
    response = await ds.client.get("/d?" + urllib.parse.urlencode({"sql": final_sql}))
    assert response.status_code == 200
    soup = Soup(response.text, "html.parser")
    td = soup.select("table.rows-and-columns tbody td")[0]
    a = td.find("a")
    if is_link_expected:
        assert a is not None
        assert a.text == sql
    else:
        assert a is None
        if wrap_it:
            assert td.text == sql
