
from fastapi import FastAPI, Request, Response, status
from typing import Dict, Any
import uvicorn
import json
from db import queries
import formResponse as respMapper
import requests
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}

res=respMapper.FormResponse()
db_conn=queries()
@app.get("/search", status_code=200)
async def handle(response: Response, request: Request = Dict[Any, Any]):
    query_params = dict(request.query_params)
    data= db_conn.get_home_hospitals(int(query_params.get('page', '1')))
    return res.hospital_response(data)

#@app.get("/news", status_code=200)
#async def handle(response: Response, request: Request = Dict[Any, Any]):
#    data= db_conn.get_home_news()
#    data_dict = {i+1: record for i, record in enumerate(data)}
#    return data_dict

@app.get("/Hospitaldetails", status_code=200)
async def handle(response: Response, request: Request = Dict[Any, Any]):
    query_params = dict(request.query_params)
    data= db_conn.get_hospital_details(query_params.get('ID', ''))
    return res.hospital_det_response(data)

    #return res.hospital_det_response(data)
####
@app.get("/SpecHospitals", status_code=200)
async def handle(response: Response, request: Request = Dict[Any, Any]):
    query_params = dict(request.query_params)
    data= db_conn.get_specialHosp_details(query_params.get('ID', ''))
    return res.hospital_response(data)

@app.get("/suggestions", status_code=200)
async def handle(response: Response, request: Request = Dict[Any, Any]):
    query_params = dict(request.query_params)
    data= db_conn.get_suggestions(query_params.get('keyword',''))
    data = [{ "Source": record[0], "Hospital_Id": record[1], "Hospital_Name":record[2],"Specialty_Id":record[3],"Specialty":record[4]} for record in data]
    #data_dict = {i+1: record for i, record in enumerate(data)}
    return data

@app.get("/form_details", status_code=200)
async def handle(response: Response, request: Request = Dict[Any, Any]):
    query_params = dict(request.query_params)
    data= db_conn.get_rooms(query_params.get('ID', ''))
    data = [{ "Hospital_ID": record[0], "Room_ID": record[1],"Room_Type":record[2], "Room_Cost":record[3],"Available_rooms":record[4]} for record in data]
    return data

 #define the API endpoint that fetches the data from the website
@app.post("/fetch-data", status_code=200)
async def fetch_data(request: Request):
    #print("hwjjw",request.method, request.body)
    #print("jhhhhhh")
    data = await request.json()
    #print("DDDDDDDDDDDD",data)
    db_conn.insert_data(data)
    return {"message": "Appointment Done!"}

    
    


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="info")
    