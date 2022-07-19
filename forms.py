from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

##WTForm

class CreateBill(FlaskForm):
    scno = StringField('Service Number', validators=[DataRequired()])
    uscno = StringField('Unique Service Number', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    addr = StringField('Address', validators=[DataRequired()])
    present_reading = StringField('Present Reading', validators=[DataRequired()])
    month = StringField('Month', validators=[DataRequired()])
    staus = StringField('Status', validators=[DataRequired()])
    units = StringField('Units', validators=[DataRequired()])
    energycharges = StringField('Energy Charges', validators=[DataRequired()])
    othercharges = StringField('Other Charges', validators=[DataRequired()])
    duecharges = StringField('Due Charges', validators=[DataRequired()])
    submit = SubmitField("Submit")