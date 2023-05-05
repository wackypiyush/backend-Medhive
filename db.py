import pypyodbc as odbc
#import requests
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
            #off=(page-1)*10
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
   
    # TO give the data about hospital which is clicked
    def get_hospital_details(self,ID:str):
        try:
            cursor = self.conn.cursor()
            query1="USE Minor;"
            query2 = f"""SELECT * from Hospital_Info where H_No=\'{ID}\'"""
            cursor.execute(query1)
            cursor.execute(query2)
            print(query2)

            # Fetch the results of the query
            results = cursor.fetchall()
            print(results)

            # return the results
            return results
        
        except Exception as e:
            print("Exception occured:{}".format(e))
            raise Exception(e)
            # success = False
    
    def get_specialHosp_details(self,ID:str):
        try:
            cursor = self.conn.cursor()
            query1="USE Minor;"
            query2 = f"""

            SELECT h.*, STRING_AGG(s.Specialty, ',') WITHIN GROUP (ORDER BY s.Specialty) AS Specialties
            FROM Hospital_Info h
            INNER JOIN (
            SELECT value AS SpecialtyID 
            FROM STRING_SPLIT( \'{ID}\', ',')
            ) sp ON CHARINDEX(sp.SpecialtyID, h.Specialties_Present) > 0
            INNER JOIN Specialties s ON CHARINDEX(s.SpecialtyID, h.Specialties_Present) > 0
            GROUP BY h.H_No, h.Hospital_Name, h.Place, h.Total_Doctors, h.Total_Beds, h.MortailityRate, 
            h.Cleanliness_Score, h.Specialties_Present, h.Total_Specialties_Present, h.Stars;"""
            #print("Qry",query2)
            cursor.execute(query1)
            cursor.execute(query2)

            # Fetch the results of the query
            results = cursor.fetchall()

            # return the results
            return results
        
        except Exception as e:
            print("Exception occured:{}".format(e))
            raise Exception(e)
            # success = False

    # Search Hospital or Disease
    def get_suggestions(self,keyword:str):
        try:
            cursor = self.conn.cursor()
            #print("Hello")
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
            print("Exception occured:{}".format(e))
            raise Exception(e)
            # success = False

    # Get room details as per Hospital Id for form
    def get_rooms(self,ID:str):
        try:
            cursor = self.conn.cursor()
            query1="USE Minor;"
            query2 = f"""select H_No,RoomID,CASE
                        when RoomID='R1' Then 'General'
                        when RoomID='R2' Then 'Semi-Private'
                        when RoomID='R3' Then 'Private'
                        End as 'Room_Type',Room_Cost, Available_Rooms
                        from Rooms_Info
                        where H_No=\'{ID}\'"""
            cursor.execute(query1)
            cursor.execute(query2)
           
            results = cursor.fetchall()
            return results
        
        except Exception as e:
            print("Exception occured:{}".format(e))
            raise Exception(e)
            
    def insert_data(self,patient_data):
        try:
            print("outjfdnejf",patient_data)
            h_name = patient_data["hospitalName"]
            patient_name = patient_data["patName"]
            room_type = patient_data["roomType"]
            appointment_date = patient_data["date"]
            payment_mode = patient_data["MOP"]
            H_No=patient_data["hospitalId"]
            RoomID=patient_data["roomId"]

            # insert the data into the new_Patients table
            cursor = self.conn.cursor()
            query1="USE Minor;"  
            query2 = f"""INSERT INTO new_Patients (H_Name, Patient_Name, Room_Type, Appointment, Payment_Mode)
                VALUES (\'{h_name}\', \'{patient_name}\',\'{room_type}\' , CAST('{appointment_date}' AS DATE), \'{payment_mode}\');"""
            query3=f"""UPDATE Rooms_Info
                SET Beds_Occupied = Beds_Occupied + 1,
                Available_Rooms = Available_Rooms - 1
                WHERE H_No = \'{H_No}\' AND RoomID = \'{RoomID}\';"""
            
            cursor.execute(query1)
            cursor.execute(query2)
            cursor.execute(query3)
            self.conn.commit()
            
        except Exception as e:
            print("Exeception occured:{}".format(e))
            raise Exception(e)


    def __del__(self):
            self.conn.close()