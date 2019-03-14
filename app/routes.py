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


conn = sqlite3.connect('./app/db/final.db')
c = conn.cursor()
c.execute("SELECT DISTINCT(p_group) FROM searchable ORDER BY p_group ASC")
groups = c.fetchall()
conn.close()


symbols = {
"A" : "A - Human Necessities",
"B" : "B - Operations and Transport",
"C" : "C - Chemistry and Metallurgy",
"D" : "D - Textiles",
"E" : "E - Fixed Constructions",
"F" : "F - Mechanical Engineering",
"G" : "G - Physics",
"H" : "H - Electricity",
"Y" : "Y - Emerging Cross-Sectional Technologies"
}


all_groups = []
current_sym = 'A'
current_group = []
current_group.append(symbols[current_sym])
for group in groups:
    group = str(group[0])
    if group.startswith(current_sym):
        current_group.append(group)
    else:
        all_groups.append(current_group)
        current_group = []
        current_sym = group[0]
        print(current_sym)
        current_group.append(symbols[current_sym])
        current_group.append(group)

print(all_groups)

cpc_groups_dict = {}

with open("./app/cpc_group.tsv", 'rU') as f:
    for line_terminated in f:
        try:
            line = line_terminated.rstrip('\n')
            line = line.split("\t")
            if line[0] == "id":
                continue
            cpc_groups_dict[line[0]] = line[1]
        except(ValueError, IndexError):
            continue

print(cpc_groups_dict)

form_groups = []
for group in groups:
    form_groups.append((str(group[0]).upper(), str(group[0]).upper()))


@app.route('/', methods=['GET'])
def index():
    form = PatentSearchForm()
    return render_template('index.html', title='Patent search', all_groups=all_groups, cpc_groups_dict=cpc_groups_dict)


@app.route('/group/<code>', methods=['GET'])
def daily_post(code):
    #do your code here

    conn = sqlite3.connect('./app/db/final.db')
    c = conn.cursor()
    c.execute("SELECT country, count(*) AS counter FROM searchable WHERE p_group='%s' GROUP BY country ORDER BY counter DESC" % code)
    patents = c.fetchall()
    conn.close()


    return render_template('patents.html', title='Patent search', group=code, patents=patents, code_description=cpc_groups_dict[code])
