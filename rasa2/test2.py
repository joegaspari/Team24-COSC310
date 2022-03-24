import itertools
import json

# f = open('rasa2/resources/airports.json')

# data = json.load(f)


# city = 'Vancouver'
# listObj = []

# for e in data['airport']:
#     # if(e['city'].strip() == city):
#         # print(e['city'] + ' : ' + e['code'])
#     listObj.append({
#         'city': e['city'],
#         'code': e['code']
#     })

# print(listObj)




# grouped_items = {}
# for item in data['airport']:
#         city = item["city"]
#         if city in grouped_items:
#                 grouped_items[city].append(item)
#         else:
#                 grouped_items[city] = [item]

# print(grouped_items)
# print(json.dumps(grouped_items, indent=2))

# for e in grouped_items:
    # print(e)


# unique = {each['city'] : each for each in listObj}.values()

# print(unique)


# with open('rasa2/resources/airports_rmDuplicates.json', 'w') as outfile:
    # json.dump(list(unique), outfile)


# for key in grouped_items:
    # print(key)
    # if any(obj['city'] == key for obj in listObj):
    #     print(key + ' not yet appended')
    # else:
    #     listObj.append({
    #     'city': key['city'],
    #     'Code': key['code'],
    #     "Email": "33@gmail.com"
    #     })
    # print(key, ":", grouped_items[key])



f1 = open('resources/airports_rmDuplicates.json')

data = json.load(f1)

depart_code = 'Not found'
arrival_code = 'Not found'
departC = 'Vancouver'
arrivalC = 'Toronto'

for e in data:
    response = 'e["city"]: {}, arrivalC {} departCC {}'.format(e['city'], arrivalC, departC)
    if(e['city'] == arrivalC):
        arrival_code = e['code']
    if(e['city'] == departC):
        depart_code = e['code']

response = 'Arrival code: {}, depature code {}'.format(arrival_code, depart_code)
print(response)

# print(data)