from flask import Flask, render_template, request
import forms
app = Flask(__name__)

@app.route('/')
def home():
    title = 'Treasurer Check'
    return render_template('home.html', title=title)

@app.route('/checklist', methods=['POST'])
def checklist():
    title = 'Treasurer Check'
    form_id = request.form['form_id']
    username = request.form['username']
    csv_file = request.form['csv_file']
    venmos = forms.get_venmos(form_id)
    payments = forms.get_payments(username, csv_file)
    return render_template('checklist.html', title=title, venmos=venmos, payments=payments)

@app.route('/unpaid', methods=['POST','GET'])
def unpaid():
    title = 'Treasurer Check'
    unpaidlist = request.form.getlist('unpaidchecks')
    #TODO: add line for to get phone numbers from form to print on unpaid list
    return render_template('unpaid.html', title=title, unpaidlist=unpaidlist)

if __name__ == '__main__':
    app.run(debug=True)