import sqlite3

from flask import render_template
from app import app
from app.forms import PatentSearchForm


conn = sqlite3.connect('./app/db/final.db')

symbols = [('A', 'Human Necessities'),
('B', 'Operations and Transport'),
('C', 'Chemistry and Metallurgy'),
('D', 'Textiles'),
('E', 'Fixed Constructions'),
('F', 'Mechanical Engineering'),
('G', 'Physics'),
('H', 'Electricity'),
('Y', 'Emerging Cross-Sectional Technologies')]


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PatentSearchForm()
    if form.validate_on_submit():
        group = str(form.group.data).upper()
        print(group)
        conn = sqlite3.connect('./app/db/final.db')
        c = conn.cursor()
        c.execute("SELECT country, count(*) AS counter FROM searchable WHERE p_group='%s' GROUP BY country ORDER BY counter DESC" % group)
        patents = c.fetchall()
        conn.close()

        return render_template('index.html', title='Patent search', form=form, patents=patents)
    return render_template('index.html', title='Patent search', form=form)
