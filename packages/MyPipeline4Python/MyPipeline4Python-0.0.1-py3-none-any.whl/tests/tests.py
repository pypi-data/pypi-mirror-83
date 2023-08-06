from src.programDB import initialize_db, process
import psycopg2
import pytest
# test
@pytest.mark.unit
def test_initialize_DB():
    assert initialize_db() is True, "Error, DB_connection failed"


@pytest.mark.unit
def test_process():
    assert process('n','0empty0','0empty0') is 0, "No more requests, test passed"


@pytest.mark.integtest
def test_makeaquery():
    cons = 's'
    nome = "tiberio"
    cognome = "falsiroli"
    start = initialize_db()
    value = process(cons,nome,cognome)
    assert start is True, "Connection failed, start should be true, but is " + start
    assert value == 1, "In the end value should be 0 but is" + value
