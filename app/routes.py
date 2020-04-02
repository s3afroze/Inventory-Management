"""
Author: Shahzeb Afroze
This script will be used as the core for redirecting websites

"""
from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Entry, Customer, Product, Transaction, Inventory, Procurement
from datetime import datetime
import lasio
import argparse
import os
import re
import pandas as pd
import pathlib
from plotly import tools
import plotly.graph_objs as go
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import sqlite3
import time

# https://docs.sqlalchemy.org/en/13/core/dml.html - Documentation
# ---------------------- DASH ---------------------
db_file = "app/app.db"
myConnection = sqlite3.connect(db_file)


re = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dash/'
)

re.css.config.serve_locally = True
re.scripts.config.serve_locally = True

server = re.server



df = pd.read_csv('demo.cscv', index_col=[0])
def generate_frontpage():
    print(df)
    # global df
    # df = pd.read_csv('demo.cscv', index_col=[0])
    return html.Div(
        id="las-header",
        children=[
            html.Div(
                id="las-header-text",
                children=[
                    html.H1("Interactive Report"),
                    html.Div(
                        id="las-file-info",
                        children=[
                            html.Span(children="SQLAlchemy Database"),
                        ],
                    ),
                ],
            ),
        ],
    )


def generate_table(df):
    cols = df.columns
    df = df[cols]
    return dt.DataTable(
        id="table",
        sort_action="native",
        filter_action="native",
        row_deletable=True,

        style_data={"whiteSpace": "normal"},
        style_cell={
            "padding": "15px",
            "midWidth": "0px",
            "width": "25%",
            "textAlign": "center",
            "border": "white",
        },

        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
    )


re.layout = html.Div(
    [
        html.Div(id="controls", children=[html.Button("Print", id="las-print")]),
        html.Div(id="frontpage", className="page", children=generate_frontpage()),
        html.Div(
            className="section",
            children=[
                html.Div(className="section-title", children="Generated Report"),
                html.Div(
                    className="page",
                    children=[
                        html.Div(id="las-table", children=generate_table(df)),
                        html.Div(id="las-table-print"),
                    ],
                ),
            ],
        ),

    ]
)


@re.callback(Output("las-table-print", "children"), [Input("table", "data")])
def update_table_print(data):
    # id     title description are columns for the current db

    
    tables_list = []
    num_tables = int(len(data) / 34) + 1  # 34 rows max per page
    for i in range(num_tables):
        table_rows = []
        for j in range(34):
            if i * 34 + j >= len(data):
                break
            table_rows.append(
                html.Tr([html.Td(data[i * 34 + j][key]) for key in data[0].keys()])
            )
        table_rows.insert(
            0,
            html.Tr(
                [
                    html.Th(key.title())
                    for key in data[0].keys()
                ]
            ),
        )
        tables_list.append(
            html.Div(className="tablepage", children=html.Table(table_rows))
        )
    return tables_list

# ----------------- FLASK KICKS IN HERE -----------------
@app.route('/print_ent', methods=['POST', 'GET'])
def print_ent():
    if request.method == 'POST':
        form = request.form
        option_selected = form.get('carlist')
        
        if option_selected == "Customer":
            print('customer chosen')
            return redirect(url_for('print_Customer'))

        elif option_selected == "Transaction":
            print('Transaction chosen')
            return redirect(url_for('print_Transaction'))

        elif option_selected == "Product":
            print('Product chosen')
            return redirect(url_for('print_Product'))

        elif option_selected == "Inventory":
            print('Inventory chosen')
            return redirect(url_for('print_Inventory'))

        elif option_selected == "Procurement":
            print('Procurement chosen')
            return redirect(url_for('print_Procurement'))

    return render_template('test.html')

# @app.route('/print_transaction')
# def print_transaction():
#     db_file = "app/app.db"
#     myConnection = sqlite3.connect(db_file)
#     df = pd.read_sql("SELECT * FROM 'Transaction'", myConnection)
#     df.to_csv('demo.cscv')
#     return redirect(url_for('/dash/'))

@app.route('/print_Customer')
def print_Customer():
    global df
    db_file = "app/app.db"
    myConnection = sqlite3.connect(db_file)
    df = pd.read_sql("SELECT * FROM 'Customer'", myConnection)
    df.to_csv('demo.cscv')
    return redirect(url_for('/dash/'))

@app.route('/print_Product')
def print_Product():
    global df
    db_file = "app/app.db"
    myConnection = sqlite3.connect(db_file)
    df = pd.read_sql("SELECT * FROM 'Product'", myConnection)
    df.to_csv('demo.cscv')
    return redirect(url_for('/dash/'))

@app.route('/print_Transaction')
def print_Transaction():
    global df
    db_file = "app/app.db"
    myConnection = sqlite3.connect(db_file)
    df = pd.read_sql("SELECT * FROM 'Transaction'", myConnection)
    df.to_csv('demo.cscv')
    return redirect(url_for('/dash/'))

@app.route('/print_Inventory')
def print_Inventory():
    global df
    db_file = "app/app.db"
    myConnection = sqlite3.connect(db_file)
    df = pd.read_sql("SELECT * FROM 'Inventory'", myConnection)
    df.to_csv('demo.cscv')
    return redirect(url_for('/dash/'))

@app.route('/print_Procurement')
def print_Procurement():
    global df
    db_file = "app/app.db"
    myConnection = sqlite3.connect(db_file)
    df = pd.read_sql("SELECT * FROM 'Procurement'", myConnection)
    df.to_csv('demo.cscv')
    return redirect(url_for('/dash/'))
   
# Print function ends


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# # initial settings
# @app.route('/index')
# def index():
#     entries = Entry.query.all()
#     return render_template('index.html', entries=entries)

# @app.route('/add', methods=['POST'])
# def add():

#     if request.method == 'POST':
#         form = request.form
#         title = form.get('title')
#         description = form.get('description')
#         if not title or description:
#             entry = Entry(title = title, description = description)
#             db.session.add(entry)
#             db.session.commit()
#             return redirect(url_for('index'))

#     return "Database Updated"


# @app.route('/update/<int:id>')
# def updateRoute(id):
#     # send back the entry after extraction
#     if not id or id != 0:
#         entry = Entry.query.get(id)
#         return render_template('update.html', entry=entry)

#     return "Database Entry Extracted"


# @app.route('/update_entry/<int:id>', methods=['POST'])
# def update(id):
#     if not id or id != 0:
#         entry = Entry.query.get(id)
#         if entry:
#             # update title and description from the forms
#             entry.title = request.form["title"]
#             entry.description = request.form["description"]
#             db.session.commit()
#         return redirect(url_for('index'))

#     return "Entry Extracted"

# @app.route('/delete/<int:id>')
# def delete(id):
#     if not id or id != 0:
#         entry = Entry.query.get(id)
#         if entry:
#             db.session.delete(entry)
#             db.session.commit()
#         return redirect(url_for('index'))

#     return "Entry Deleted"

# INVENTORY ADJUSTMENT

def inventory_create(productid):
    inventory = Inventory(productid=productid, quanity_left=0)
    db.session.add(inventory)
    db.session.commit()

# postitve quantity variable will mean add, and negative will mean reduce
def inventory_adjust(productid, quantity_adjust):
    inventory = Inventory.query.get(productid)
    quanity_orig = inventory.quanity_left
    quanity_left = quanity_orig+quantity_adjust
    inventory.quanity_left = quanity_left

    if quanity_left<0:
        return quanity_orig
    else:
        print(inventory)
        print(f"inventory added {quantity_adjust}")
        db.session.commit()
        return "completed"


def inventory_delete(productid):
    inventory = Inventory.query.get(productid)
    db.session.delete(inventory)
    db.session.commit()

# ------------------------ merchandising settings --------------------------------

@app.route('/merchandising')
def merchandising():
    products = Product.query.all()
    print(products)
    return render_template('merchandising.html', products=products)

@app.route('/merchandising_add', methods=['POST'])
def merchandising_add():
    if request.method == 'POST':
        form = request.form
        prod_name = form.get('prod_name')
        unit_cost = form.get('unit_cost')
        sale_price = form.get('unit_price')

        print(form)
        # if not prod_name:
        # create the product first
        product = Product(name = prod_name, sale_price = sale_price, unit_cost = unit_cost)
        db.session.add(product)
        db.session.commit()

        # create inventory with 0 item
        item = Product.query.filter_by(name=prod_name).all()[-1]
        productid = item.id

        # create inventory item
        inventory_create(productid)


        return redirect(url_for('merchandising'))

    # return "Database Updated"


@app.route('/merchandising_update/<int:id>')
def merchandising_updateRoute(id):
    # send back the entry after extraction
    if not id or id != 0:
        product = Product.query.get(id)
        return render_template('merchandising_update.html', product=product)

    return "Database merchandising Extracted"


@app.route('/merchandising_update_entry/<int:id>', methods=['POST'])
def merchandising_update(id):
    if not id or id != 0:
        product = Product.query.get(id)
        if product:
            # update title and description from the forms
            product.name = request.form["prod_name"]
            product.sale_price = request.form["sale_price"]
            product.unit_cost = request.form["unit_cost"]
            db.session.commit()

            inventory_delete(id) # delete inv

        return redirect(url_for('merchandising'))

    return "merchandising Extracted"

@app.route('/merchandising_delete/<int:id>')
def merchandising_delete(id):
    if not id or id != 0:
        product = Product.query.get(id)
        

        if product:
            db.session.delete(product)
            db.session.commit()


        return redirect(url_for('merchandising'))

    return "merchandising Deleted"


# ------------------------ Procurement settings --------------------------------
from random import random

@app.route('/procurement')
def procurement():
    products = Product.query.all()
    procurements = Procurement.query.all()
    date_today = datetime.datetime.now()
    return render_template('procurement.html', products=products, procurements = procurements, date_today=date_today)

import datetime
@app.route('/procurement_add', methods=['POST'])
def procurement_add():
    if request.method == 'POST':
        form = request.form
        print(form)
        proc_date = datetime.datetime.strptime(form.get('proc_date'), "%Y-%m-%d")
        rand_sec = random() # in order to avoid issues of pushing multiple actions within a second
        proc_date_time = datetime.datetime.now() + datetime.timedelta(microseconds=rand_sec)                         
        proc_date_time_rounded_off = proc_date_time - datetime.timedelta(microseconds=proc_date_time.microsecond)

        print(proc_date_time_rounded_off)

        quantity_purchased = int(form.get('qty_purchased'))
        product_name = form.get('product_name')
        item = Product.query.filter_by(name=product_name).first()
        unit_cost = item.unit_cost
        productid = item.id
        total_cost = unit_cost*quantity_purchased

        procurement = Procurement(productid=productid, date = proc_date_time_rounded_off, quantity_purchased = quantity_purchased, total_cost=total_cost)

        db.session.add(procurement)
        db.session.commit()

        # adjust inv
        # pull avaible
        inventory_adjust(productid, quantity_purchased)

        return redirect(url_for('procurement'))

    # return "Database Updated"


@app.route('/procurement_update/<listOfObjects>')
def procurement_updateRoute(listOfObjects):

    # send back the entry after extraction
    res = listOfObjects.strip('][').split(', ') 
    productid = res[0]
    datetime_el = res[1]
    proc_date_time = datetime.datetime.strptime(datetime_el, "%Y-%m-%d %H:%M:%S")
    date_today=datetime.datetime.now()

    print(proc_date_time)

    procurement = Procurement.query.get((productid, proc_date_time))
    product = Product.query.get(productid)

    if not productid or productid != 0:
        return render_template('procurement_update.html', product=product, procurement=procurement, date_today=date_today)


    return redirect(url_for('procurement'))


@app.route('/procurement_update_entry/<listOfObjects>', methods=['POST'])
def procurement_update(listOfObjects):
    form = request.form
    res = listOfObjects.strip('][').split(', ') 
    productid = res[0]
    datetime_el = res[1]
    proc_date_time = datetime.datetime.strptime(datetime_el, "%Y-%m-%d %H:%M:%S")
    procurement = Procurement.query.get((productid, proc_date_time))

    # inventory adjustment needed, add or deduct (NEW - CURRENT)
    adjustment_required = int(form.get('qty_purchased')) - procurement.quantity_purchased
    inventory_adjust(productid, adjustment_required)

    if productid:
        proc_date = datetime.datetime.strptime(form.get('proc_date'), "%Y-%m-%d")
        proc_date_time = datetime.datetime.combine(proc_date, datetime.datetime.now().time())                          
        proc_date_time_rounded_off = proc_date_time - datetime.timedelta(microseconds=proc_date_time.microsecond)
        procurement.quantity_purchased = int(form.get('qty_purchased'))
        
        item = Product.query.filter_by(id=productid).first()
        unit_cost = item.unit_cost
        total_cost = unit_cost * procurement.quantity_purchased
        procurement.total_cost = total_cost

        db.session.commit()
        return redirect(url_for('procurement'))

    return "procurement Extracted"

@app.route('/procurement_delete/<listOfObjects>')
def procurement_delete(listOfObjects):
    res = listOfObjects.strip('][').split(', ') 
    productid = res[0]
    datetime_el = res[1]
    proc_date_time = datetime.datetime.strptime(datetime_el, "%Y-%m-%d %H:%M:%S")
    procurement = Procurement.query.get((productid, proc_date_time))
    
    # adjust inventory
    adjustment_required = -(procurement.quantity_purchased)  # add negative to remove
    inventory_adjust(productid, adjustment_required)

    if procurement:
        db.session.delete(procurement)
        db.session.commit()
    return redirect(url_for('procurement'))

    return "procurement Deleted"

# ------------------------ Customer Registeration settings --------------------------------

@app.route('/customer')
def customer():
    customers = Customer.query.all()
    
    return render_template('customer.html', customers=customers)

import datetime
@app.route('/customer_add', methods=['POST'])
def customer_add():
    if request.method == 'POST':
        form = request.form
        firstname = form["firstname"].title()
        lastname = form["lastname"].title()
        street = form["street"]
        city = form["city"].title()
        province = form["province"].upper()
        zipcode = form["zipcode"].upper()

        customer = Customer(firstname=firstname, lastname = lastname, street = street, city=city, province=province, zipcode=zipcode)

        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('customer'))

    # return "Database Updated"


@app.route('/customer_update/<int:id>')
def customer_updateRoute(id):
    customer = Customer.query.get(id)

    if not customer or customer != 0:
        return render_template('customer_update.html', customer=customer)


    return redirect(url_for('customer'))


@app.route('/customer_update_entry/<int:id>', methods=['POST'])
def customer_update(id):
    form = request.form

    if not id or id != 0:
        customer = Customer.query.get(id)
        if customer:
            # update title and description from the forms
            customer.firstname = request.form["firstname"].title()
            customer.lastname = request.form["lastname"].title()
            customer.city = request.form["city"].title()
            customer.street = request.form["street"]
            customer.province = request.form['province'].upper()
            customer.zipcode = request.form['zipcode'].upper()

            db.session.commit()

        return redirect(url_for('customer'))

    return "procurement Extracted"

@app.route('/customer_delete/<int:id>')
def customer_delete(id):
    if not id or id != 0:
        customer = Customer.query.get(id)
    if procurement:
        db.session.delete(customer)
        db.session.commit()
    return redirect(url_for('customer'))

    return "procurement Deleted"



# ------------------------ Transaction settings --------------------------------

@app.route('/transaction')
def transaction():
    products = Product.query.all()
    customers = Customer.query.all()
    transactions = Transaction.query.all()
    date_today = datetime.datetime.now()
    inventory = Inventory.query.all()
    print(inventory)
    return render_template('transaction.html', products=products, customers = customers, 
        transactions=transactions, date_today=date_today, inventory=inventory)

import datetime
@app.route('/transaction_add', methods=['POST'])
def transaction_add():
    if request.method == 'POST':
        form = request.form
        rand_sec = random() # in order to avoid issues of pushing multiple actions within a second
        tran_date_time = datetime.datetime.now() + datetime.timedelta(microseconds=rand_sec)
        tran_date_time_rounded_off = tran_date_time - datetime.timedelta(microseconds=tran_date_time.microsecond)
        
        quantity_sold = int(form.get('qty_sold'))

        prodid = form.get('product_name')
        item = Product.query.get(prodid)
        unit_price = item.sale_price
        productid = item.id
        print(productid)
        total_sales = unit_price*quantity_sold

        customerid = form.get('customer_name')
       
        # adjustment inventory required
        adjustment_required = -quantity_sold
        inv_available = inventory_adjust(productid, adjustment_required)

        if inv_available!="completed":
            return f"We only have {inv_available} of the product available. Your current order cannot be met - I am sorry."
       
        else:
            transaction = Transaction(productid = productid, date = tran_date_time_rounded_off, 
                                customerid = customerid, total_sales = total_sales, quantity_sold=quantity_sold)
        # what if inventory runs out

        print(transaction)
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transaction'))

    # return "Database Updated"


@app.route('/transaction_update/<listOfObjects>')
def transaction_updateRoute(listOfObjects):
    # send back the entry after extraction
    res = listOfObjects.strip('][').split(', ') 
    customerid = res[0]
    productid = res[1]
    trans_date = res[2]
    customer = Customer.query.get(customerid)

    trans_date_time = datetime.datetime.strptime(trans_date, "%Y-%m-%d %H:%M:%S")

    transaction = Transaction.query.get((customerid, productid, trans_date_time))
    
    product = Product.query.get(productid)

    if not productid or productid != 0:
        return render_template('transaction_update.html', product=product, transaction=transaction, customer=customer)


    return redirect(url_for('transaction'))


@app.route('/transaction_update_entry/<listOfObjects>', methods=['POST'])
def transaction_update(listOfObjects):
    form = request.form
    # send back the entry after extraction
    res = listOfObjects.strip('][').split(', ') 
    print(res)
    print(res)
    print(res)
    print(res)
    customerid = res[0]
    productid = res[1]
    trans_date = res[2]



    print(trans_date)
    trans_date_time = datetime.datetime.strptime(trans_date, "%Y-%m-%d %H:%M:%S")

    transaction = Transaction.query.get((customerid, productid, trans_date_time))
    

    if productid:
        trans_date = datetime.datetime.strptime(form.get('selling_date'), "%Y-%m-%d")
        trans_date_time = datetime.datetime.combine(trans_date, datetime.datetime.now().time())                          
        trans_date_time_rounded_off = trans_date_time - datetime.timedelta(microseconds=trans_date_time.microsecond)
        transaction.quantity_sold = int(form.get('quantity_sold'))
        
        item = Product.query.filter_by(id=productid).first()
        unit_price = item.sale_price
        total_sales = unit_price * transaction.quantity_sold
        transaction.total_sales = total_sales

        # inventory adjust 
        # adjustment inventory required
        adjustment_required = -int(form.get('quantity_sold'))
        inv_available = inventory_adjust(productid, adjustment_required)

        if inv_available!="completed":
            return f"We only have {inv_available} of the product available. Your current order cannot be met - I am sorry."
        
        else:
            db.session.commit()
            return redirect(url_for('transaction'))

    return "procurement Extracted"

@app.route('/transaction_delete/<listOfObjects>')
def transaction_delete(listOfObjects):
    res = listOfObjects.strip('][').split(', ') 
    customerid = res[0]
    productid = res[1]
    trans_date = res[2]

    trans_date_time = datetime.datetime.strptime(trans_date, "%Y-%m-%d %H:%M:%S")
    transaction = Transaction.query.get((customerid, productid, trans_date_time))
    
    # add back to inventory
    # inventory adjustment needed, add or deduct (NEW - CURRENT)
    adjustment_required = transaction.quantity_sold
    inventory_adjust(productid, adjustment_required)

    if transaction:
        db.session.delete(transaction)
        db.session.commit()
    return redirect(url_for('transaction'))

    return "transaction Deleted"

@app.route('/test')
def test():
    return render_template('test.html')



