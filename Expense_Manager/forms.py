from flask_wtf import FlaskForm
from wtforms import SubmitField,DateField,FloatField,StringField,SelectField
from wtforms.validators import DataRequired


choiceType=['Expense','Income']
class expenseForm(FlaskForm):
    expense=SelectField("Expense/Income",choices=choiceType)
    date=DateField("Date",validators=[DataRequired()])
    description=StringField("Description",validators=[DataRequired()])
    category=SelectField(label='State', choices=[('value1', 'Bills'), ('value2', 'Food'), ('value3', 'Shopping'),('value4','Transport'),
                                                 ('value5','Medical'),('value6','Rent'),('value7','Money Transfer')])
    submit = SubmitField("Save")
