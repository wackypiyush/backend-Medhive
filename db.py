import pypyodbc as odbc
import requests
import datetime
DRIVER_NAME="SQL SERVER"
SERVER_NAME="BT1000109872\SQLEXPRESS"
DATABASE_NAME="Minor"

connection_string=f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

class queries:
    def __init__(self):
        self.conn=odbc.connect(connection_string)
    def get_home_hospitals(self,page:int):
        try:
            cursor = self.conn.cursor()
            off=(page-1)*10
            query1="USE Minor;"
            query2 = f"SELECT * FROM Top10"
            cursor.execute(query1)
            cursor.execute(query2)

            # Fetch the results of the query
            results = cursor.fetchall()

            # return the results
            return results
        
        except Exception as e:
            print("Exeception occured:{}".format(e))
            raise Exception(e)
            # success = False

    def get_home_news(self):
        try:
            # BBC news api
            # following query parameters are used
            # source, sortBy and apiKey
            query_params = {
                "source": "bbc-news",
                "category" :"health",
                "language" : "en",
                "sortBy": "top",
                "apiKey": "ee60c89cda2549e19dc8c9fe0c249d57"
            }
            main_url = "http://newsapi.org/v2/top-headlines?"

            # fetching data in json format
            res = requests.get(main_url, params=query_params)
            open_bbc_page = res.json()

            # getting all articles in a string article
            article = open_bbc_page["articles"]

            # empty list which will contain all trending news,url,content
            results = []
            url=[]
            content=[]

            for ar in article:
                results.append(ar["title"])
                url.append(ar["url"])
                if ar['content'] is not None:
                    content.append(ar['content'].split('… ')[0])
                else:
                    content.append('')

            news = []
            for i in range(len(results)):
                if results:
                    news_item = {
                        'title': results[i],
                        'content': content[i],
                        'url': url[i]
                    }
                    news.append(news_item)

            return news
        
        except Exception as e:
            print("Exception occurred:{}".format(e))
            raise Exception(e)
        
    # TO give the data about hospital which is clicked
    def get_hospital_details(self,ID:str):
        try:
            cursor = self.conn.cursor()
            query1="USE Minor;"
            query2 = f"SELECT * FROM Hospital_Info where H_No=\'{ID}\';"
            cursor.execute(query1)
            cursor.execute(query2)

            # Fetch the results of the query
            results = cursor.fetchall()

            # return the results
            return results
        
        except Exception as e:
            print("Exeception occured:{}".format(e))
            raise Exception(e)
            # success = False
    
    def get_specialHosp_details(self,ID:str):
        try:
            cursor = self.conn.cursor()
            query1="USE Minor;"
            query2 = f"SELECT * from Hospital_Info where Specialties_Present like '%{ID}%' order by stars desc;"
            print("Qry",query2)
            cursor.execute(query1)
            cursor.execute(query2)

            # Fetch the results of the query
            results = cursor.fetchall()

            # return the results
            return results
        
        except Exception as e:
            print("Exeception occured:{}".format(e))
            raise Exception(e)
            # success = False

    # Search Hospital or Disease
    def get_suggestions(self,keyword:str):
        try:
            cursor = self.conn.cursor()
            print("Hello")
            query1="USE Minor;"
            query2 = f"""select 'Hospital' as Source, H_No as ID, Hospital_Name as Name, Null as Specialty_ID, Null as Specialty 
            from Hospital_Info where Hospital_Name LIke '%{keyword}%'
            union 
            Select 'Specilaty' as Source, Null as ID, Null as Name, SpecialtyID as Specialty_ID, Specialty 
            from Specialties where Diseases Like '%{keyword}%' or Specialty Like '%{keyword}%'"""
            cursor.execute(query1)
            cursor.execute(query2)
            # Fetch the results of the query
            results = cursor.fetchall()

            # return the results
            return results
        
        except Exception as e:
            print("Exeception occured:{}".format(e))
            raise Exception(e)
            # success = False

    # Get room details as per Hospital Id for form
    def get_rooms(self,ID:str):
        try:
            cursor = self.conn.cursor()
            query1="USE Minor;"
            query2 = f"""select H_No,RoomID,CASE
                        when RoomID='R1' Then 'General'
                        when RoomID='R2' Then 'Semi-Priavte'
                        when RoomID='R3' Then 'Private'
                        End as 'Room_Type',Room_Cost, Available_Rooms
                        from Rooms_Info
                        where H_No=\'{ID}\'"""
            cursor.execute(query1)
            cursor.execute(query2)
           
            # Fetch the results of the query
            results = cursor.fetchall()

            # return the results
            return results
        
        except Exception as e:
            print("Exeception occured:{}".format(e))
            raise Exception(e)
            # success = False

    def insert_data(self,patient_data):
        try:
                    
            h_name = patient_data["h_name"]
            patient_name = patient_data["patient_name"]
            #specialty = patient_data["specialty"]
            room_type = patient_data["room_type"]
            appointment_date = patient_data["appointment_date"]
            payment_mode = patient_data["payment_mode"]
            H_No=patient_data["h_no"]
            RoomID=patient_data["room_id"]

            # insert the data into the new_Patients table
            cursor = self.conn.cursor()
            query1="USE Minor;"  
            query2 = f"""INSERT INTO new_Patients (H_Name, Patient_Name, Room_Type, Appointment_Date, Payment_Mode)
                VALUES (\'{h_name}\', \'{patient_name}\',\'{room_type}\' , {appointment_date}, \'{payment_mode}\');"""
            #print("QQQQ",query2)
            query3=f"""UPDATE Rooms_Info
                SET Beds_Occupied = Beds_Occupied + 1,
                Available_Rooms = Available_Rooms - 1
                WHERE H_No = \'{H_No}\' AND RoomID = \'{RoomID}\';"""
            #print("WWWW",query3)
        
            cursor.execute(query1)
            cursor.execute(query2)
            cursor.execute(query3)
            self.conn.commit()
            
        except Exception as e:
            print("Exeception occured:{}".format(e))
            raise Exception(e)
            # success = False


    def __del__(self):
            self.conn.close()