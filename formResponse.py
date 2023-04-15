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
    
    def hospital_det_response(self,data):
        #print("DDDD",data)
        data = [{ "H_No": record[0], "Hospital_Name": record[1],"Place":record[2],"Total_Doctors":record[3],"Total_Beds":record[4],"MortalityRate":record[5],"CleanlinessScore":record[6],"Specialties_Present":record[7],"Total_Specialties":record[8],"Stars":record[9],} for record in data]
            
        return data



    
