version = 1.87

class FormResponse:
    def __init__(self):
        self.response = {
            "data":{},
            "is_success": False
        }
    def hospital_response(self,data):
        data = {i+1:{ "H_No": record[0], "Hospital_Name": record[1],"Place":record[2],"Total_Doctors":record[3],"Total_Beds":record[4],"MortalityRate":record[5],"CleanlinessScore":record[6],"Specialties_Present":record[7],"Total_Specialties":record[8],"Stars":record[9],"Image":record[10]} for i,record in enumerate(data)} 
        self.response["data"]= data
        if data:
            self.response["is_success"] = True
        else:
            self.response["is_success"] = False
            
        return self.response
    def hospital_home_response(self,data):
        data = [{ "H_No": record[0], "Hospital_Name": record[1],"Place":record[2],"Total_Doctors":record[3],"Total_Beds":record[4],"MortalityRate":record[5],"CleanlinessScore":record[6],"Specialties_Present":record[7],"Total_Specialties":record[8],"Stars":record[9]} for record in data] 
       
       
            
        return data
    
    def hospital_det_response(self,data):
        #print("DDDD",data)
        data = [{ "H_No": record[0], "Hospital_Name": record[1],"Place":record[2],"Total_Doctors":record[3],"Total_Beds":record[4],"MortalityRate":record[5],"CleanlinessScore":record[6],"Total_Specialties":record[8],"Stars":record[9],"Specialities":record[10]} for record in data] 
        return data

    def suggest_response(self,data):
        data = [{ "Source": record[0], "Hospital_Id": record[1], "Hospital_Name":record[2],"Specialty_Id":record[3],"Specialty":record[4]} for record in data]
        return data
    
    def form_response(self,data):
        data = [{ "Hospital_ID": record[0], "Room_ID": record[1],"Room_Type":record[2], "Room_Cost":record[3],"Available_rooms":record[4]} for record in data]
        return data

    
