import sqlite3

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

conn = sqlite3.connect('./app/db/final.db')
c = conn.cursor()
c.execute("SELECT DISTINCT(p_group) FROM searchable ORDER BY p_group ASC")
groups = c.fetchall()
conn.close()

symbols = [('A', 'A - Human Necessities'),
('B', 'B - Operations and Transport'),
('C', 'C - Chemistry and Metallurgy'),
('D', 'D - Textiles'),
('E', 'E - Fixed Constructions'),
('F', 'F - Mechanical Engineering'),
('G', 'H - Physics'),
('H', 'H - Electricity'),
('Y', 'Y - Emerging Cross-Sectional Technologies')]

form_groups = []
for group in groups:
    form_groups.append((str(group[0]).upper(), str(group[0]).upper()))

#test = [(str(group[0]).lower(), str(group[0]).upper()) for group in groups if group[0].startswith('A')]


class PatentSearchForm(FlaskForm):
    symbol = SelectField('Symbol', choices=symbols)
    group = SelectField('Group')
    submit = SubmitField('Search!')


    def get_group_values():
        print(self.symbol.data)

    def __init__(self, *args, **kwargs):
        super(PatentSearchForm, self).__init__(*args, **kwargs)
        self.group.choices = [(str(group[0]).upper(), str(group[0]).upper()) for group in groups if group[0].startswith(self.symbol.data)]
