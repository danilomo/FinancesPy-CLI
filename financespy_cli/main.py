#!/usr/bin/env python

import sys
import os
import datetime
import itertools
import financespy_cli.clutil as clutil
from financespy_cli.clutil import Command
import financespy_cli.sh as sh

from financespy import Account
from financespy import XLSXBackend
import financespy.categories as categories


def current_year():
    return datetime.datetime.now().year

def backend(folder):
    cats = [
        "misc",
        "uncategorized",
        ("food", [ ("groceries", ["lidl", "aldi", "edeka", "rewe"]), "restaurant", "street_food"]),
        ("utilities", ["internet", "electricity", "cellphone_balance"]),
        ("travel", ["plane_ticket", "hotel_reservation", "train_ticket"]),
        ("tax", ["tv_tax"]),
        ("shopping", ["electronics", "clothing", "sports", "home_goods", "furniture", "shopping_misc", "shoes", "purses", "jewlery"]),
        ("education", [("course_fee", ["german_course"]), "textbook", "school_supplies"]),
        ("body_and_hygiene", ["perfume", "hair_product", "hairdresser", "nails", "müller"]),
        ("commuting", ["monthly_ticket", "day_ticket", "single_ticket"]),
        ("clothing", ["h_&_m", "zara"])
    ]

    cats = categories.categories_from_list(cats)

    return XLSXBackend(folder, cats)

@Command
def import_csv( args, workspace = "./ws/", year = current_year() ):
    month = args[0]
    file_name = args[1]

    account = Account( backend(workspace) )

    with open( file_name, "r" ) as file_:

        for line in file_:
            columns = [line.strip() for line in line.split(",") if line.strip() ]
            day = int(columns[0])
            transaction = parse_transaction(columns[1:])

            if not transaction.value.is_zero():            
                account.day( day, month, year ).insert_record( transaction )
                
@Command
def review_month( args, workspace = "./ws/", year = current_year() ):
    month = args[0]
    account = Account( backend(workspace) )

    for day in account.month( month, year ).days():
        os.system('clear')
        print( "Day: " + str(day.date) )

        records = list( day.records() )

        if not records:
            print("No expenses.")
            input()
            continue

        records_as_str = [ str(r) for r in records ]
        maxlen         = len(max( records_as_str, key=len)) if records else 0
        hr             = maxlen * "_"

        print(hr + "\n")
        print( "\n".join(records_as_str) )
        print(hr)

        values = [ r.value for r in records ]
        total = sum(values)
        print("\nTotal: " + str(total) )

        input()


@Command
def edit_day( args,  editor = "emacs", workspace = "./ws/", year = current_year() ):
    day = int(args[0])
    month = args[1]
    year = int(year)

    account = Account( backend(workspace) )

    day = account.day( day, month, year )

    file_name = day.backend.file( day.date )

    if not os.path.exists(file_name):
        sh.touch(file_name)

    sh.emacs(file_name, _bg = True)

def main():
    clutil.execute()

if __name__ == "__main__":
    main()
