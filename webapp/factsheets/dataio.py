import os
import json
from pymongo import MongoClient

FACTSHEETS_FS = os['FACTSHEETS_FS']

mongo_client = MongoClient(
    host=os.environ['FS_MONGO_HOST'],
    port=int(os.environ['FS_MONGO_PORT']))


def dump_collection(collection, path):
    data = mongo_client['factsheets'][collection] \
        .find({}, {'_id': 0})
    with open(path, 'w') as f:
        json.dump(list(data), f)


def load_collection(collection, path):
    with open(path, 'r') as f:
        data = json.load(f)

    for record in data:
        meta_load = mongo_client['factsheets'][collection] \
            .insert_one(record)

##########################
# FUND
##########################
def create_fund(fund_name, data):
    pass
    # mongo_connection['factsheets']['funds'] \
    #     .insert()

def read_fund(fund_name):
    data = mongo_client['factsheets']['funds'] \
        .find({'fund_name': fund_name})
    return list(data)[0]

def update_fund(fund_name, updates):
    mongo_client['factsheets']['funds'] \
        .update_one(
            { 'fund_name': fund_name },
            { '$set': updates })

def delete_fund(fund_name):
    pass


##########################
# FUNDS
##########################
def read_funds():
    data = mongo_client['factsheets']['funds'] \
        .find({}, {'_id': 0, 'fund_name': 1})
    data = list(data)
    data = [e['fund_name'] for e in data]
    return data

##########################
# PLOTS
##########################
def create_investment_growth_plot(fund_name, fig):
    path = FACTSHEETS_FS + '/funds/%s/plots/investment_growth.png' % fund_name
    fig.write_image(path)