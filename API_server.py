import json
#import ssl
import xmltodict
import dicttoxml

from auth import verify_access_token, get_scope_of_token, validate_token_scope
from flask import Flask, request, make_response

app = Flask(__name__)



@app.before_request
def before_request():
  # Checks if the access token is present and valid. 
  auth_header = request.headers.get('Authorization')
  if 'Bearer' not in auth_header:
    return json.dumps({
      'error': 'Access token does not exist.'
    }), 400
  
  access_token = auth_header[7:]
  print(f"Access token received: {access_token}")

  if access_token and verify_access_token(access_token):
      pass
  else:
    return json.dumps({
      'error': 'Access token is invalid.'
    }), 400


@app.route('/resource1_xml', methods = ['GET'])
def get_resource1_xml():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })

    xml_data = "<root> <employees>  <employee>  <name>Shaunak</name>  <isActive>false</isActive>  <dob>1999/09/01 07:10:00</dob>    </employee>   </employees>  </root>"
    
    post_data = xmltodict.parse(xml_data)
    print(post_data)
    myResponse = make_response(post_data)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/xml'

    return myResponse




@app.route('/resource2_JSON_explode', methods = ['GET'])
def get_resource2_json():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    

    return json.dumps({  

        "int_array" : [1,2,3,4,6], 
        "string_array": ["Notebook", "Pen", "Sharpener", "Rubber", "Stapler"], 
        "decimal_array": [123.123, 232.235, 32.235, 52.235, 253.523, 523.564, 520.523],  
        "double_array" : [3.141592, 2.71828, 1.6108], 
        "timestamp_array": ["2022/01/12 10:41:24", "2023/10/30 20:43:34", "2023/04/11 21:34:32"], 
        "boolean_array": ["true", "false", "false", "true"], 
        "struct_array" : [{"id":5001, "name":"Shaunak Chakraborty", "designation":"QA"},  
                         {"id":5002, "name": "Asif Ahamad", "designation":"Senior QA" }], 
        "array_of_array": [[{"id":1001, "name":"eggs"}, {"id":1002, "name":"milk"}], 
                            [{"id":2001, "name":"tomato"}, {"id":2002, "name":"broccoli"}], 
                            [{"id":3001, "name":"Apple"}, {"id":3002, "name":"Oranges"}]]
     })



@app.route('/resource2_XML_explode', methods = ['GET'])
def get_resource2_xml():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
      
    xml_data_dict = {  

        "int_array" : [1,2,3,4,6], 
        "string_array": ["Notebook", "Pen", "Sharpener", "Rubber", "Stapler"], 
        "decimal_array": [123.123, 232.235, 32.235, 52.235, 253.523, 523.564, 520.523],  
        "double_array" : [3.141592, 2.71828, 1.6108], 
        "timestamp_array": ["2022/01/12 10:41:24", "2023/10/30 20:43:34", "2023/04/11 21:34:32"], 
        "boolean_array": ["true", "false", "false", "true"], 
        "struct_array" : [{"id":5001, "name":"Shaunak Chakraborty", "designation":"QA"},  
                         {"id":5002, "name": "Asif Ahamad", "designation":"Senior QA" }], 
        "array_of_array": [[{"id":1001, "name":"eggs"}, {"id":1002, "name":"milk"}], 
                            [{"id":2001, "name":"tomato"}, {"id":2002, "name":"broccoli"}], 
                            [{"id":3001, "name":"Apple"}, {"id":3002, "name":"Oranges"}]]
     }

    xml_Data = dicttoxml.dicttoxml(xml_data_dict)
    myResponse = make_response(xml_Data.decode())
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/xml'

    return myResponse



@app.route('/resource3_xml_nested_levels', methods = ['GET'])
def get_resource3_xml():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    with open('XmlData_with_nested_structs.xml', 'r') as f:
        xml_data = f.read()

    print(xml_data)
    myResponse = make_response(xml_data)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/xml'

    return myResponse


@app.route('/resource4_json_array_of_records', methods = ['GET'])
def get_resource4_json():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    with open('Json_data_array_of_records.json', 'r') as f:
        array_of_records = f.read()

    print(array_of_records)
    myResponse = make_response(array_of_records)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/json'

    return myResponse


@app.route('/resource5_xml_response_all_data_types', methods = ['GET'])
def get_resource5_xml():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    with open('XML_response_all_data_types.xml', 'r') as f:
        records = f.read()

    print(records)
    myResponse = make_response(records)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/xml'

    return myResponse


@app.route('/resource5_json_response_all_data_types', methods = ['GET'])
def get_resource5_json():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    with open('JSON_response_all_data_types.json', 'r') as f:
        records = f.read()

    print(records)
    myResponse = make_response(records)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/json'

    return myResponse



@app.route('/resource6_xml_data_with_special_characters_in_keys', methods = ['GET'])
def get_resource6_xml():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    with open('XML_data_with_special_characters_in_keys.xml', 'r') as f:
        records = f.read()

    print(records)
    myResponse = make_response(records)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/xml'

    return myResponse

@app.route('/resource6_json_data_with_special_characters_in_keys', methods = ['GET'])
def get_resource6_json():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    with open('JSON_Data_with_special_characters_in_keys.json', 'r') as f:
        records = f.read()

    print(records)
    myResponse = make_response(records)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/json'

    return myResponse



@app.route('/resource3_json_nested_levels', methods = ['GET'])
def get_resource3():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    return json.dumps({
                "response": [{
		                    "addresses":[{ "address": "ABC street", "type": "primary" }, { "address":"DEF street", "type":"secondary" }]
	                    },

                        {
		                    "addresses":[{ "address": "PQR street", "type": "primary" }, { "address":"XYZ street", "type":"secondary" }]
	                    }, 

                        {
		                    "addresses":[{ "address": "LMN street", "type": "primary" }, { "address":"Park street", "type":"secondary" }]
	                    }
	            ]
            })



@app.route('/resource1_json', methods = ['GET'])
def get_resource1():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    return json.dumps({ "res": [
        {"COL_STRING": "jannear27@studiopress.com", 
        "COL_INT" : 12412, 
        "COL_DECIMAL": 241.324, 
        "COL_TIMESTAMP": "2022-06-26 10:01:41", 
        "COL_BOOLEAN": False, 
        "COL_STRUCT": { "Name" : "Martin", "Year of birth" : { "year" : 1955, "month" : 1, "day" : 23 }}  , 
        "COL_ARRAY": [
            {  "Name" : "Martin", "Year of birth" :  1980 },
            {  "Name" : "Margaret", "Year of birth" : 1983 }        
          ]  
        }        
    ]})





@app.route('/users', methods = ['POST'])
def create_user():
    
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="post_users"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    post_data = xmltodict.parse(request.get_data())
    print(post_data)


    myResponse = make_response(request.get_data())
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/xml'

    return myResponse
    

@app.route('/users_json', methods = ['POST'])
def create_user_json():
    
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="post_users_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })
    
    post_data = request.get_data()
    print(post_data)


    myResponse = make_response(request.get_data())
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/json'

    return myResponse


    
    



@app.route('/users', methods = ['GET'])
def get_user():
  # Returns a list of users.
  access_token = request.headers.get('Authorization')[7:]

  if not validate_token_scope(access_token=access_token, endpoint="get_users"):
    return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
    })


  users = [
    { 'username': 'Jane Doe', 'email': 'janedoe@example.com'},
    { 'username': 'John Doe', 'email': 'johndoe@example.com'}
  ]


  """response_containing_array_of_array = {
    "results": [
        {
            "address_components": [
                {
                    "long_name": "1600",
                    "short_name": "1600",
                    "types": [
                        "street_number"
                    ]
                },
                {
                    "long_name": "Amphitheatre Parkway",
                    "short_name": "Amphitheatre Pkwy",
                    "types": [
                        "route"
                    ]
                },
                {
                    "long_name": "Mountain View",
                    "short_name": "Mountain View",
                    "types": [
                        "locality",
                        "political"
                    ]
                },
                {
                    "long_name": "Santa Clara County",
                    "short_name": "Santa Clara County",
                    "types": [
                        "administrative_area_level_2",
                        "political"
                    ]
                },
                {
                    "long_name": "California",
                    "short_name": "CA",
                    "types": [
                        "administrative_area_level_1",
                        "political"
                    ]
                },
                {
                    "long_name": "United States",
                    "short_name": "US",
                    "types": [
                        "country",
                        "political"
                    ]
                },
                {
                    "long_name": "94043",
                    "short_name": "94043",
                    "types": [
                        "postal_code"
                    ]
                }
            ],
            "formatted_address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
            "geometry": {
                "location": {
                    "lat": 37.4224428,
                    "lng": -122.0842467
                },
                "location_type": "ROOFTOP",
                "viewport": {
                    "northeast": {
                        "lat": 37.4239627802915,
                        "lng": -122.0829089197085
                    },
                    "southwest": {
                        "lat": 37.4212648197085,
                        "lng": -122.0856068802915
                    }
                }
            },
            "place_id": "ChIJeRpOeF67j4AR9ydy_PIzPuM",
            "plus_code": {
                "compound_code": "CWC8+X8 Mountain View, CA",
                "global_code": "849VCWC8+X8"
            },
            "types": [
                "street_address"
            ]
        },

        {
            "address_components": [
                {
                    "long_name": "1600",
                    "short_name": "1600",
                    "types": [
                        "street_number"
                    ]
                },
                {
                    "long_name": "Amphitheatre Parkway",
                    "short_name": "Amphitheatre Pkwy",
                    "types": [
                        "route"
                    ]
                },
                {
                    "long_name": "Mountain View",
                    "short_name": "Mountain View",
                    "types": [
                        "locality",
                        "political"
                    ]
                },
                {
                    "long_name": "Santa Clara County",
                    "short_name": "Santa Clara County",
                    "types": [
                        "administrative_area_level_2",
                        "political"
                    ]
                },
                {
                    "long_name": "California",
                    "short_name": "CA",
                    "types": [
                        "administrative_area_level_1",
                        "political"
                    ]
                },
                {
                    "long_name": "United States",
                    "short_name": "US",
                    "types": [
                        "country",
                        "political"
                    ]
                },
                {
                    "long_name": "94043",
                    "short_name": "94043",
                    "types": [
                        "postal_code"
                    ]
                }
            ],
            "formatted_address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
            "geometry": {
                "location": {
                    "lat": 37.4224428,
                    "lng": -122.0842467
                },
                "location_type": "ROOFTOP",
                "viewport": {
                    "northeast": {
                        "lat": 37.4239627802915,
                        "lng": -122.0829089197085
                    },
                    "southwest": {
                        "lat": 37.4212648197085,
                        "lng": -122.0856068802915
                    }
                }
            },
            "place_id": "ChIJeRpOeF67j4AR9ydy_PIzPuM",
            "plus_code": {
                "compound_code": "CWC8+X8 Mountain View, CA",
                "global_code": "849VCWC8+X8"
            },
            "types": [
                "street_address"
            ]
        }

    ],
    "status": "OK"
  }"""

  array_response = [
        {
            "address_components": [
                {
                    "long_name": "1600",
                    "short_name": "1600",
                    "types": [
                        "street_number"
                    ]
                },
                {
                    "long_name": "Amphitheatre Parkway",
                    "short_name": "Amphitheatre Pkwy",
                    "types": [
                        "route"
                    ]
                },
                {
                    "long_name": "Mountain View",
                    "short_name": "Mountain View",
                    "types": [
                        "locality",
                        "political"
                    ]
                },
                {
                    "long_name": "Santa Clara County",
                    "short_name": "Santa Clara County",
                    "types": [
                        "administrative_area_level_2",
                        "political"
                    ]
                },
                {
                    "long_name": "California",
                    "short_name": "CA",
                    "types": [
                        "administrative_area_level_1",
                        "political"
                    ]
                },
                {
                    "long_name": "United States",
                    "short_name": "US",
                    "types": [
                        "country",
                        "political"
                    ]
                },
                {
                    "long_name": "94043",
                    "short_name": "94043",
                    "types": [
                        "postal_code"
                    ]
                }
            ],
            "formatted_address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
            "geometry": {
                "location": {
                    "lat": 37.4224428,
                    "lng": -122.0842467
                },
                "location_type": "ROOFTOP",
                "viewport": {
                    "northeast": {
                        "lat": 37.4239627802915,
                        "lng": -122.0829089197085
                    },
                    "southwest": {
                        "lat": 37.4212648197085,
                        "lng": -122.0856068802915
                    }
                }
            },
            "place_id": "ChIJeRpOeF67j4AR9ydy_PIzPuM",
            "plus_code": {
                "compound_code": "CWC8+X8 Mountain View, CA",
                "global_code": "849VCWC8+X8"
            },
            "types": [
                "street_address"
            ]
        },

        {
            "address_components": [
                {
                    "long_name": "1600",
                    "short_name": "1600",
                    "types": [
                        "street_number"
                    ]
                },
                {
                    "long_name": "Amphitheatre Parkway",
                    "short_name": "Amphitheatre Pkwy",
                    "types": [
                        "route"
                    ]
                },
                {
                    "long_name": "Mountain View",
                    "short_name": "Mountain View",
                    "types": [
                        "locality",
                        "political"
                    ]
                },
                {
                    "long_name": "Santa Clara County",
                    "short_name": "Santa Clara County",
                    "types": [
                        "administrative_area_level_2",
                        "political"
                    ]
                },
                {
                    "long_name": "California",
                    "short_name": "CA",
                    "types": [
                        "administrative_area_level_1",
                        "political"
                    ]
                },
                {
                    "long_name": "United States",
                    "short_name": "US",
                    "types": [
                        "country",
                        "political"
                    ]
                },
                {
                    "long_name": "94043",
                    "short_name": "94043",
                    "types": [
                        "postal_code"
                    ]
                }
            ],
            "formatted_address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
            "geometry": {
                "location": {
                    "lat": 37.4224428,
                    "lng": -122.0842467
                },
                "location_type": "ROOFTOP",
                "viewport": {
                    "northeast": {
                        "lat": 37.4239627802915,
                        "lng": -122.0829089197085
                    },
                    "southwest": {
                        "lat": 37.4212648197085,
                        "lng": -122.0856068802915
                    }
                }
            },
            "place_id": "ChIJeRpOeF67j4AR9ydy_PIzPuM",
            "plus_code": {
                "compound_code": "CWC8+X8 Mountain View, CA",
                "global_code": "849VCWC8+X8"
            },
            "types": [
                "street_address"
            ]
        }

    ]



  return array_response



@app.route('/items', methods = ['GET'])
def get_items():

     # Returns a list of users.
  users = [
    { 'username': 'Jane Doe', 'email': 'janedoe@example.com'},
    { 'username': 'John Doe', 'email': 'johndoe@example.com'}
  ]

  return json.dumps({"data": users})




### Endpoints provided by Arya

##put request make it for xml and json both type
@app.route('/users_json', methods=['PUT'])
def update_user_json_PUT():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="put_users_json"):
        return json.dumps({
            'error': 'Invalid token: Token with write scope is required.'
        })

    put_data = request.get_data()
    print(put_data)

    myResponse = make_response(put_data)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/json'

    return myResponse


@app.route('/users_json', methods=['PATCH'])
def update_user_json_PATCH():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="put_users_json"):
        return json.dumps({
            'error': 'Invalid token: Token with write scope is required.'
        })

    data = request.get_data()
    print(data)

    myResponse = make_response(data)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/json'

    return myResponse




##put request make it for xml and json both type
@app.route('/users_xml', methods=['PUT'])
def update_user_XML_PUT():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="put_users_xml"):
        return json.dumps({
            'error': 'Invalid token: Token with write scope is required.'
        })

    put_data = request.get_data()
    print(put_data)

    myResponse = make_response(put_data)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/xml'

    return myResponse



@app.route('/users_xml', methods=['PATCH'])
def update_user_XML_PATCH():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="put_users_xml"):
        return json.dumps({
            'error': 'Invalid token: Token with write scope is required.'
        })

    data = request.get_data()
    print(data)

    myResponse = make_response(data)
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/xml'

    return myResponse





if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  app.run(port = 5002, debug = True)
