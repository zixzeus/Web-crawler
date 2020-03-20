class Crawler(object):
    def __init__(self):
        self.headers ={
            "Referer":"http://10.8.165.15:8180/TransferFlight/index.do",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
            "Host": "10.8.165.15:8180",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.session = requests.Session()
        self.post_url = "http://10.8.165.15:8180/TransferFlight/login.do"
        self.logined_url = "http://10.8.165.15:8180/TransferFlight/transfer/passenger/list.do"
        self.LOGIN = False
    def login(self,name,password):
        post_data ={"username":name,
                    "password":password}
        response = self.session.post(self.post_url,data=post_data,headers=self.headers)
        if response.json()['state'] == 1:
            self.LOGIN = True
            response2 = self.session.get(self.logined_url)
            print('login seccessful')
            return self.session
        else :
            print('login failed')
    
    def crawler(self,flight_in_date,flight_out_date):
        data1 = {
                    "flightInDate": flight_in_date,
                    "flightOutDate": flight_out_date,
                    "flightNo":"" ,
                    "flightTime_from": "00:00",
                    "flightTime_to": "24:00",
                    "in_out": "in",
                    "flowTo":"", 
                    "inCarrier":"" ,
                    "outCarrier":"", 
                    "psgname":"" ,
                    "pnrno":"", 
                    "luggageNo":"", 
                    "ticketNo":"", 
                    "pdocNo":"" ,
                    "inSeatNo":"",
                    "outSeatNo":"", 
                    "cabin":"", 
                    "transferCabin":"", 
                    "transferTime": "<75",
                    "transferTime": "75-150",
                    "transferTime": ">150",
                    "ctl": "",
                    "lugType":"", 
                    "process":"" ,
                    "psgtype":"", 
                    "special":"", 
                }
        headers1 ={
                    'Referer': 'http://10.8.165.15:8180/TransferFlight/transfer/passenger/transferPassengers.do',
                    'Host':'10.8.165.15:8180',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                }
        if self.LOGIN==True:
            response=self.session.post(self.logined_url,data=data1,headers=headers1)
            passenger = response.json()['transferInfoList']
            self.passenger=pd.DataFrame(passenger)
            return self.passenger
        elif self.LOGIN == False:
            print('please login first')
    def write_to_excel(self,file_name):
        writer = pd.ExcelWriter(file_name)
        self.passenger.to_excel(writer,encoding='utf-8')
        writer.save()
        
