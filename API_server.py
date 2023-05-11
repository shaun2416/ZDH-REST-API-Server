import json
#import ssl
import xmltodict

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
def get_resource1():
    access_token = request.headers.get('Authorization')[7:]
    if not validate_token_scope(access_token=access_token, endpoint="resource1_json"):
        return json.dumps({
      'error': 'Invalid token: Token with read scope is required.'
      })

    xml_data = "<root> <employees>  <employee>  <name>Shaunak</name>  <isActive>false</isActive>  <dob>1999/09/01 07:10:00</dob>    </employee>   </employees>  </root>"
    
    post_data = xmltodict.parse(xml_data)
    print(post_data)
    myResponse = make_response(request.get_data())
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.mimetype = 'application/xml'

    return myResponse




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
        "COL_BOOLEAN": "false", 
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




if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  app.run(port = 5002, debug = True)
