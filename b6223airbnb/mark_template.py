import json

i = __import__('20085272G_import_airbnb')
j = __import__('20085272G_airbnb_webapi')

i.start()

test_app = j.app
#uncomment the following line to launch the flask app
# test_app.run()

test_app.config['TESTING'] = True
tclient= test_app.test_client()
response = tclient.get('/mystudentID/')
print(response.status_code == 200)
print(response.mimetype == 'application/json')
print(json.loads(response.data) == {'studentID':'20085272G'})


response = tclient.get('/airbnb/reviews/')
print(response.status_code == 200)
print(response.mimetype == 'application/json')
print(json.loads(response.data))
print(json.loads(response.data)['Count'] == 1354)