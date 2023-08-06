# -*- coding: utf-8 -*-
from os import sep
from numpy.core.multiarray import datetime_as_string
import requests
import math
import pandas as pd
import json
from datetime import datetime as dt
from datetime import timedelta
import urllib.parse
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class Client():
    def __init__(self, parameters = None):
        """
        Make client for z-info extract. 
        You can provide a parameter file name.
        If no parameter file name is supplied it will generate a template

        Parameters
        ----------
        parameters: str
            Parameter file name
        """
        if parameters:
            self.parameters = parameters
        else: 
            self.parameters = {
                "username":"",
                "password":"",
                "file_name":"",
                "file_format":".csv or .feather",
                "seperate_files":"True or False"
                "input_file":"csv file for tagNr's",
                "startdate":"YYYY-MM-DD",
                "enddate":"YYYY-MM-DD",
                "periode":"1m",
                "interval":"10",
                "waterschapnummer":"38"}

    def set_parameters(self, parameters):
        """
        Set parameters for client

        Parameters
        ----------
        parameters: dict
            Parameters for client

        """
    def get_credentials(self, ):
        """
        Get credentials for Azure Key Vault.

        Returns
        -------
        username: str
            Username for z-info
        password: str
            Password for z-info
        """
        KVUri = f"https://kvvwam.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        username = client.get_secret("z-info-username")
        password = client.get_secret("z-info-password")
        return username.value, password.value

    def __get_zinfo_token(self, username, password):
        """
        Get bearer token for access to the Z-info webservice

        Parameters
        ----------
        username: str
            Username for Z-info (no need for admin rights)
        password: str
            Password for Z-info

        Returns
        -------
        result: str
            Access token in string format
        """

        token_url = "https://webservice.z-info.nl/WSR/zi_wsr.svc/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
                'grant_type': 'password',
                'username': username,
                'password': password
                }
        
        r=requests.post(token_url, headers = headers, data = data)

        r.encoding = "utf-8"
        access_token = r.text # Dictionary in text format

        bearer = json.loads(access_token)['access_token']
        
        return bearer

    def __get_zinfo_data(self, my_token, my_url):
        """
        Retrieve data for a single URL using the Z-info webservice and save it locally

        Parameters
        ----------
        my_token: str
            Access token for Z-info webservice, retrieved using get_bearer_token
        my_url: str
            URL for Z-info web-service
            
        Returns
        -------
        df: pd df
            Data in pandas dataframe
        """
        my_string = {'Authorization': 'Bearer ' + my_token}

        r = requests.get(my_url, headers = my_string)

        df = r.json()
        df = df["waarden"]
        return df

    def __date_range(self, start, end, interval):
        #TODO check same day
        """
        Split a date range specified by a start date (start) and an end date (end). Splits the date range
        in intervals of interval

        Parameters
        ----------
        start: str
            startdate (yyyy-mm-dd)
        end: str
            enddate (yyyy-mm-dd)
        intv: num
            Number of intervals
            
        Returns
        -------
        dates_splits: list of lists
            A list with intv number of date ranges. Date range specified in str format, in separate list.
        """
        min_difference = timedelta(days=interval)
        start = dt.strptime(start,"%Y-%m-%d")
        end = dt.strptime(end,"%Y-%m-%d") 
        difference = end-start
        intv = 1
        for intv in range(1,math.ceil(difference.days/10)):
            if difference/intv < min_difference:
                break
        diff = (end  - start ) / intv

        ranges = [(start + diff * i).strftime("%Y-%m-%d") for i in range(intv)]
        ranges.append(end.strftime("%Y-%m-%d"))
        date_splits = [[ranges[i],ranges[i+1]] for i in range(intv)]
            
        return date_splits

    def __make_url(self, waterschapnummer, spcid, startdate, enddate, tagnr, wbm, periode):
        """ 
        Create a URL for z-info 
        
        Parameters
        ----------
        waterschapnummer: str
            id number waterschap
        startdate: str
            startdate (yyyy-mm-dd)
        enddate: str
            enddate (yyyy-mm-dd)
        tagnr: str
            tag number for sensor
        wbm: str
            aggregate function
        periode: 
            aggregate time unit

        Returns
        -------
        URL: str
            endpoint for z-info api
        """
        return rf'https://webservice.z-info.nl/WSR/zi_wsr.svc/JSON/NL.{waterschapnummer}/?spcid={spcid}&vraag=$begindatum$={startdate};$einddatum$={enddate};$tagnr$={urllib.parse.quote(tagnr, safe="")};$wbm$={wbm};$periode$={periode}'

    def __construct_dataframe(self, parameters):
        """
        construct a dataframe for given parameters

        Parameters
        ----------
        parameters: dict
            dictionary containing all the necessary parameters
        
        Returns
        -------
        export_dataframe: DataFrame
            Dataframe containing z-info data
        """ 
        username = parameters["username"]
        password = parameters["password"]
        file_name = parameters["file_name"]
        file_format = parameters["file_format"]
        input_file_name = parameters["input_file"]
        seperate_files = parameters["seperate_files"]
        startdate = parameters["startdate"]
        enddate = parameters["enddate"]
        periode = parameters["periode"]
        interval = int(parameters["interval"])
        waterschapnummer = parameters["waterschapnummer"]
        spcid = parameters["spcid"]
        input_file = pd.read_csv(f'{input_file_name}.csv', sep=',')
        export_dataframe = pd.DataFrame()
        date_splits = self.__date_range(startdate, enddate, interval)
        for i,tagnr in enumerate(input_file['tagnr']):
            name = input_file.loc[i,'name']
            print(f'Getting data for {name}')
            tag_dataframe = pd.DataFrame()
            for date_split in date_splits:
                print('...')
                token = self.__get_zinfo_token(username, password)
                URL = self.__make_url(waterschapnummer, spcid, date_split[0], date_split[1], tagnr, input_file.loc[i,'wbm'], periode)
                tag_dataframe = tag_dataframe.append(self.__get_zinfo_data(token, URL), ignore_index=True)
            if seperate_files == "True":
                tag_dataframe.to_csv(f'{name}.csv', index=False)
            else:
                if i == 0:
                    tag_dataframe = tag_dataframe.iloc[:,[0,2]].rename(columns={"dem":"tijdstip", "hstWaarde":name})
                    export_dataframe = tag_dataframe
                else:
                    export_dataframe[name] = tag_dataframe.loc[:,["hstWaarde"]].values
        return export_dataframe

    def run(self):
        with open(f'{self.parameters}.json') as file:
            parameters = json.load(file)
        export_dataframe = self.__construct_dataframe(parameters)
