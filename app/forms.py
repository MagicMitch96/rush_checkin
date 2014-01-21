from flask_wtf import Form
from wtforms import HiddenField, TextField, SelectField
from wtforms.validators import DataRequired

class RusheeForm(Form):
    name = TextField('Name', validators=[DataRequired()])
    computing_id = TextField('Computing ID', 
                             validators=[DataRequired()])
    year = SelectField('Year', choices=[('1', 'First (2017)'),
                                        ('2', 'Second (2016)'),
                                        ('3', 'Third (2015)'),
                                        ('4', 'Fourth (2014)')],
                                validators=[DataRequired()])
    dorm = TextField('Address', validators=[DataRequired()])
    pic = HiddenField('Picture', validators=[DataRequired()])

