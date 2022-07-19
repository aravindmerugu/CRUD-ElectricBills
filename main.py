import smtplib
import ssl
from datetime import datetime, timedelta
import gunicorn
import psycopg2
from psycopg2 import Binary

import bleach
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from forms import CreateBill

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# ckeditor = CKEditor(app)
Bootstrap(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///electricbills.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLES

class CreateBills(db.Model):
    __tablename__ = "all_bills"
    id = db.Column(db.Integer, primary_key=True)
    scno = db.Column(db.String(250), nullable=False)
    uscno = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    addr = db.Column(db.String(250), nullable=False)
    present_reading = db.Column(db.String(250), nullable=False)
    month = db.Column(db.String(250), nullable=False)
    staus = db.Column(db.String(250), nullable=False)
    units = db.Column(db.String(250),  nullable=False)
    energycharges = db.Column(db.String(250), nullable=False)
    othercharges = db.Column(db.String(250), nullable=False)
    duecharges = db.Column(db.String(250), nullable=False)
    issuedate = db.Column(db.String(250), nullable=False)
    dueforpayment = db.Column(db.String(250), nullable=False)
    totalpayment = db.Column(db.String(250), nullable=False)

db.create_all()

@app.route('/')
def get_all_bills():
    page = request.args.get('page', 1, type=int)
    bills = CreateBills.query.order_by(CreateBills.energycharges.desc()).paginate(
        page, per_page=9)

    return render_template("index.html", all_bills=bills)

@app.route("/addBIll", methods=["GET", "POST"])
def add_new_bill():
    new_bill = CreateBill()
    issuedate = datetime.now().strftime("%m-%d")
    duedate = (datetime.now() + timedelta(days=20)).strftime("%m-%d")
    if new_bill.validate_on_submit():
        add_bill = CreateBills(
            scno=new_bill.scno.data,
            uscno=new_bill.uscno.data,
            name = new_bill.name.data,
            addr=new_bill.addr.data,
            present_reading=new_bill.present_reading.data,
            month=new_bill.month.data,
            staus=new_bill.staus.data,
            units=new_bill.units.data,
            energycharges=new_bill.energycharges.data,
            othercharges=new_bill.othercharges.data,
            duecharges=new_bill.duecharges.data,
            issuedate = str(issuedate),
            dueforpayment=str(duedate),
            totalpayment = str(float(new_bill.energycharges.data)+float(new_bill.othercharges.data)+float(new_bill.duecharges.data))
        )
        db.session.add(add_bill)
        db.session.commit()
        return redirect(url_for("get_all_bills"))
    return render_template("addBill.html", form=new_bill)

@app.route("/bill/<int:bill_id>", methods=["GET", "POST"])
def show_bill(bill_id):
    bill = CreateBills.query.get(bill_id)
    return render_template('show_bill.html',bill=bill)



@app.route("/edit-bill/<int:bill_id>", methods=["GET", "POST"])
def edit_bill(bill_id):
    # print(bill_id)
    bill = CreateBills.query.get(bill_id)
    # print(bill.scno)
    edit_form = CreateBill(
        scno=bill.scno,
        uscno=bill.uscno,
        name=bill.name,
        addr=bill.addr,
        present_reading=bill.present_reading,
        month=bill.month,
        staus=bill.staus,
        units=bill.units,
        energycharges=bill.energycharges,
        othercharges=bill.othercharges,
        duecharges=bill.duecharges
    )
    if edit_form.validate_on_submit():
        bill.scno = edit_form.scno.data
        # print((bill.scno))
        bill.uscno = edit_form.uscno.data
        bill.name = edit_form.name.data
        bill.addr = edit_form.addr.data
        bill.present_reading = edit_form.present_reading.data
        bill.month = edit_form.month.data
        bill.staus = edit_form.staus.data
        bill.units = edit_form.units.data
        bill.energycharges = edit_form.energycharges.data
        bill.othercharges = edit_form.othercharges.data
        bill.duecharges = edit_form.duecharges.data
        bill.issuedate = bill.issuedate
        bill.dueforpayment = bill.dueforpayment
        bill.totalpayment = str(
            float(edit_form.energycharges.data) + float(edit_form.othercharges.data) + float(edit_form.duecharges.data))
        db.session.commit()
        return redirect(url_for("show_bill",bill_id=bill.id))
    return render_template("addBill.html", form=edit_form)
#
#
@app.route("/delete/<int:bill_id>")
def delete_bill(bill_id):
    post_to_delete = CreateBills.query.get(bill_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_bills'))


if __name__ == "__main__":
    app.run(debug=True)
