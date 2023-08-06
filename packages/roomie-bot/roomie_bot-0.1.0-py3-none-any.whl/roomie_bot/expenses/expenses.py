#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from roomie_bot.database.database import Database

DBNAME = "room.sqlite"


def is_number(text: str):
    try:
        float(text)
        return True
    except ValueError:
        return False


def get_debts(chat_id: int, dbname: str = DBNAME):
    reply = ''
    db = Database(dbname)

    debts = db.get_debts(chat_id)
    for debt in debts:
        reply += '{}: {}€\n'.format(db.get_username(debt[0]), debt[1])

    db.close()

    return reply


def get_payments(chat_id: int, dbname: str = DBNAME):
    reply = ''
    db = Database(dbname)

    payments = db.get_payments(chat_id)
    for payment in payments:
        reply += '{} payed {} for {}\n'.format(db.get_username(payment[0]), payment[1], payment[2])

    db.close()

    return reply


def new_payment(payer_id: int, chat_id: int, money: float, debtors_id, debtors_username, round_dec: int = 2, dbname: str = DBNAME):
    db = Database(dbname)

    # Update payer debt
    debt = db.get_debt(payer_id, chat_id)

    if debt is None:
        db.add_debt(payer_id, chat_id, round(money, round_dec))
    else:
        db.update_debt(payer_id, chat_id, round(debt + money, round_dec))

    # Update debtors debt
    extra_debt = money / len(debtors_id)

    for user_id in debtors_id:
        debt = db.get_debt(user_id, chat_id)

        if debt is None:
            db.add_debt(user_id, chat_id, round(-extra_debt, round_dec))
        else:
            db.update_debt(user_id, chat_id, round(debt - extra_debt, round_dec))

    # Add payment to history
    desc = ' '

    db.add_payment(payer_id, chat_id, money, desc.join(debtors_username))

    db.close()
