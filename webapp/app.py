import os
import logging
from pymongo import MongoClient
from flask import Flask
from flask import request
from flask import jsonify
from flask import url_for
from flask import render_template, send_from_directory, send_file

from factsheets import dataio, create_pdf


mongo_client = MongoClient(
    host=os.environ['FS_MONGO_HOST'],
    port=int(os.environ['FS_MONGO_PORT']))

app = Flask(__name__,
    template_folder='./templates',
    static_folder='./static')



#######################
# API
#######################
@app.route('/api/fund', methods=['GET', 'PUT'])
def fund():
    if request.method == 'GET':
        data = request.args
        fund_name = data['fund_name']

        fund = dataio.read_fund(fund_name=fund_name)
        fund.pop('_id')
        print(fund)
        return jsonify(fund)

    if request.method == 'PUT':
        data = request.json
        fund_name = data['fund_name']
        fund_overview = data.get('fund_overview', '')
        returns = data.get('returns', [])

        dataio.update_fund(
            fund_name=fund_name,
            updates={
                'fund_overview': fund_overview,
                'returns': returns
            })

        return(jsonify({'success': True}))


@app.route('/api/funds', methods=['GET'])
def get_funds():
    if request.method == 'GET':
        funds = dataio.read_funds()
        return jsonify(funds)


@app.route('/api/fact_sheet', methods=['GET', 'POST'])
def get_fact_sheet():
    if request.method == 'POST':
        # get data and assemble pdf props
        data = request.json
        fund_name = data.get('fund_name')
        props = dataio.read_fund(fund_name)
        # props = {
        #     'fund_name': data.get('fund_name'),
        #     'fund_overview': data.get('fund_overview')
        # }
        # print(props)

        # build pdf
        pdf = create_pdf.FactsheetPDF()
        pdf.set_state(props=props)
        pdf.build()

        return jsonify({'success': True})

@app.route('/api/download_fact_sheet', methods=['GET'])
def download_fact_sheet():
    if request.method == 'GET':
        print('downloading factsheet')
        path = os.path.dirname(os.path.realpath(__file__)) + '/static/fact_sheet.pdf'
        return send_file(
            path,
            mimetype='application/pdf',
            as_attachment=True,
            cache_timeout=0)


#######################
# VIEWS
#######################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/funds')
def funds_page():
    funds = mongo_client['factsheets']['funds'] \
        .find({}, {'_id': 0, 'fund_name': 1})
    funds = list(funds)
    funds = [e['fund_name'] for e in funds]

    return render_template('funds.html',
        funds=funds)

@app.route('/funds/<fund_name>')
def fund_page(fund_name):
    return render_template('fund.html',
        fund_name=fund_name)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=5000)
