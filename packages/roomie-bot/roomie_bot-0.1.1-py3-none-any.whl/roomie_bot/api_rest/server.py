#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify

from roomie_bot.database.database import Database

app = Flask(__name__)
app.config["DATABASE"] = "room.sqlite"


@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    db = Database(app.config["DATABASE"])
    username = db.get_username(user_id)
    db.close()

    if username is None:
        return jsonify({})
    else:
        return jsonify({'user_id': user_id,
                        'username': username})


@app.route('/api/debts/<int:user_id>/<int:chat_id>')
def get_debt(user_id, chat_id):
    db = Database(app.config["DATABASE"])
    debt = db.get_debt(user_id, chat_id)
    db.close()

    if debt is None:
        return jsonify({})
    else:
        return jsonify({'user_id': user_id,
                        'chat_id': chat_id,
                        'debt': debt})


@app.route('/api/payments/<int:payment_id>')
def get_payment(payment_id):
    db = Database(app.config["DATABASE"])
    payment = db.get_payment(payment_id)
    db.close()

    if payment is None:
        return jsonify({})
    else:
        return jsonify({'user_id': payment[0],
                        'chat_id': payment[1],
                        'money': payment[2],
                        'desc': payment[3]})
