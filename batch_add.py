import os
import weaviate
#from wcs_key import wcs_token
import json
import time
import pickle

auth_config = weaviate.auth.AuthApiKey(api_key='MhqYc1yL0oCEbnLwd2LdPCkm0sAYLqWQWk5F')
client = weaviate.Client(
    url="https://hackathon-6mwt235n.weaviate.network",
    auth_client_secret=auth_config,
    additional_headers={
        #"X-Cohere-Api-Key": os.getenv("COHERE_API_KEY"),
        "X-OpenAI-Api-Key": os.environ['xopen_apikey'], 
    }
)
client.is_ready()


#taking data


# Load the list from the pickle file
loaded_list = []
with open('tools/content/265_UltraExpensive_VeryDeep_DataSet_2023-08-21 09_02_00.745073.pkl', 'rb') as file:
    loaded_list = pickle.load(file)

#


data = loaded_list

client.batch.configure(
    batch_size=200,
    dynamic=True,
    timeout_retries=3,
)

counter=0
#python batch_add.py
with client.batch as batch:
    for idx, item in enumerate(data[34:37]):
        
        
        # print update message every 100 objects        
        if (counter %100 == 0):
            print(f"Import {counter} / {len(data)} ", end="\r")

        properties = {
        "des": item[2],
        "title": item[1],
        "url": item[5],
        "rating": float(item[3]),
        "author": item[0]
        }

        
        batch.add_data_object(data_object=properties,
            class_name="Courses")
        counter = counter+1
    print(f"Import {counter} / {len(data)}")
        
print("Import complete")


# Test that all data has loaded – get object count
result = (
    client.query.aggregate("Courses")
    .with_fields("meta { count }")
    .do()
)
print("Object count: ", result["data"]["Aggregate"]["Courses"])