#!/usr/bin/python3
# a simple library of database routines to power a payments application.

import os
import pprint
import sqlite3
from collections import namedtuple


def open_databases(path="bank.db"):
    new = not os.path.exists(path)  # 如果存在 new 为 F
    db = sqlite3.connect(path)
    if new:
        print("in this")
        c = db.cursor()
        c.execute(
            """CREATE TABLE payment (id INTEGER PRIMARY KEY, debit TEXT, credit TEXT,dollars INTEGER,memo TEXT)""")

        add_payment(db, 'brandon', 'psf', 125, 'Registration for PyCon')
        add_payment(db, 'brandon', 'liz', 200, 'Payment for writing that code')
        add_payment(db, 'sam', 'brandon', 25, 'Gas money-thanks for the ride!')
        db.commit()
    return db


def add_payment(db, debit, credit, dollars, memo):
    db.cursor().execute(""" INSERT INTO payment (debit, credit, dollars, memo) VALUES (?, ?, ?, ?) """,
                        (debit, credit, dollars, memo))


def get_payments_of(db, account):
    c = db.cursor()
    c.execute('SELECT * FROM payment WHERE credit = ? OR debit = ? ORDER BY id', (account, account))
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    return [Row(*row) for row in c.fetchall()]


if __name__ == '__main__':
    db = open_databases()
    pprint.pprint(get_payments_of(db, "brandon"))
