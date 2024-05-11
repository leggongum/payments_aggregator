from pymongo import MongoClient

from datetime import datetime
import json

from services.utils import generate_date_range
from services.schemas import AggregationRequest
from config import settings

def get_database():
 
   client = MongoClient(settings.MONGODB_URL)

   return client['Payment']


def get_aggregated_data(dt_from: datetime, dt_upto: datetime, group_type):
    dt_from, dt_upto = dt_from.isoformat(), dt_upto.isoformat()
    date_pattern = {'year': "$date.year", 'month': "$date.month"}

    date_format = {'date': "$dt"}

    match group_type:
        case 'week':
            date_pattern = {'year': '$date.isoWeekYear', 'week': "$date.isoWeek"}
            date_format['iso8601'] = True

        case 'day':
            date_pattern['day'] = "$date.day"

        case 'hour':
            date_pattern['day'] = "$date.day"
            date_pattern['hour'] = "$date.hour"

    dbname = get_database()

    collection_name = dbname["Payments"]


    return collection_name.aggregate(
        [
            {
                "$match": {"$and": [{"dt": {'$gte': datetime.fromisoformat(dt_from)}}, {"dt": {'$lte': datetime.fromisoformat(dt_upto)}}]}
            },
            {
                '$project': {
                    'date': {
                        '$dateToParts': date_format
                    },
                    'value': '$value',
                    'dt': {'$dateTrunc': {
                            'date': "$dt",
                            'unit': group_type
                    }},
                }
            },
            {
                "$group": {
                    '_id': 
                    {
                        'date': date_pattern
                    },
                    "amount": {"$sum": "$value"},
                    'date': {'$first': "$dt"},
                }
            },
            { '$unset': ["_id"] },
            {'$sort': {'date': 1}}
        ])


def form_aggregation(case: AggregationRequest) -> str:
    date_list = list(generate_date_range(*case.values()))

    res = get_aggregated_data(**case)
    
    dataset = []
    labels = []
    current = 0
    for row in res:
        while row['date'] != date_list[current]:
            labels.append(date_list[current].isoformat())
            dataset.append(0)
            current += 1
        labels.append(row['date'].isoformat())
        dataset.append(row['amount'])
        current += 1
    
    for date_index in range(current, len(date_list)):
        labels.append(date_list[current].isoformat())
        dataset.append(0)
    
    return json.dumps({'dataset': dataset, 'labels': labels})