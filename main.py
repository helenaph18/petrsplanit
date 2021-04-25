# Python Library Imports

#Flask App
from flask import Flask, request, render_template, redirect, url_for


# Creating Flask App object
app = Flask(__name__, template_folder="templates")
events = {"Sunday": [], "Monday" : [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": []}


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/add-item')
def add_page():
    return render_template('add.html')


@app.route('/view-items')
def view_page():
    return render_template('view.html', category="All", data=events)


@app.route('/view-cat', methods=['POST'])
def change_category():
    category = request.form['cat']
    return redirect('/view/' + category)


@app.route('/view-delete/<string:item_description>', methods=['POST'])
def delete_item(item_description):
    desc = item_description
    global events
    new_events = {"Sunday": [], "Monday" : [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": []}
    for day, value in events.items():
        for dictionary in value:
            if dictionary["description"] != desc:
                new_events[day].append(dictionary)
    events = new_events
    return redirect(url_for('view'))
    

@app.route('/view/<category>')
def view(category):
    global events
    if category == 'All':
        data = events
    else:
        data = {"Sunday": [], "Monday" : [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": []}
        for day_name, day_lists in events.items():
            for dictionary in day_lists:
                if dictionary['category'] == category:
                    data[day_name].append(dictionary)
    
    return render_template('view.html', category=category, data=data)


@app.route('/add', methods=['POST'])
def add_item():
    item = {
        'description': request.form['description'], 
        'category': request.form['category'], 
        'day': request.form['day']
    }
    global events
    events[item["day"]].append(item)
    return redirect('view/All')


if __name__ == "__main__":
    app.debug = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()