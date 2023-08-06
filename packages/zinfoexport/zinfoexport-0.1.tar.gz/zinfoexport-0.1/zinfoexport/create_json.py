import json
def create_json():
    json_dict = {
        "username":"",
        "password":"",
        "file_name":"",
        "file_format":".csv or .feather",
        "input_file":"csv file for tagNr's",
        "startdate":"YYYY-MM-DD",
        "enddate":"YYYY-MM-DD",
        "periode":"1m",
        "interval":10,
        "waterschapnummer":38}
    
    with open('parameters.json', 'w') as fp:
        json.dump(json_dict, fp)