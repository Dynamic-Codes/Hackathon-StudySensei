

import os
import weaviate
#from wcs_key import wcs_token
import json
import time
import openai
from notion_tools_commands import add_heading, add_to_do
import tools.parser as parserTool


while True:
  os.system('clear')
  userchoice = int(input('Welcome to StudySensei v1.0\n\n\n This is an early alpha demo. There are multiple issues and bugs that are to fixed in upcoming releases.\nThanks for your support! <3 Happy Hacking\n\n[1] AI schedule Generator\n[2] Course Finder\n[3] Exit\n\n> '))
  if userchoice == 1:
    openai.api_key = os.environ['openai_apikey']
    user_sched_imp = ''
    user_sched = ''
    while user_sched_imp != "x":
        os.system('clear') #Clears the console after each input
        user_sched_imp = input('Please input your course! Type x when done!\n> ')
        user_sched += "\n" +  user_sched_imp
    user_hours_day = input('How many hours a day would you like to study\n> ')
    user_end_date = input('In how many days would you like to finish the course?\n> ')
    
    
    prompt_load = open('./tools/content/prompt1.txt', 'r')
    prompt = eval(prompt_load.read())
    prompt_load.close()
    
    prompt_load = open('./tools/content/prompt2.txt', 'r')
    checking_prompt = eval(prompt_load.read())
    prompt_load.close()
    
    os.system('clear')
    print('Please wait... [Development Models can take around 2 minutes!]')
    
    history = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_sched}
      ]
    
    response1 = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-16k",
      messages = history,
    )
    
    print(response1.choices[0].message.content)
    responseOneArray = parserTool.parseResponse(str(response1.choices[0].message.content))
    #if (len(responseOneArray) == 0):
      #responseOneArray = False
    
    history.append({"role": "assistant", "content": response1.choices[0].message.content})
    history.append({"role": "system", "content": checking_prompt})
    
    os.system('clear')
    print('Please wait... we are almost there!')
    
    response2 = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo-16k",
      messages=history
    )
    
    responseTwoArray = parserTool.parseResponse(str(response2.choices[0].message.content))
    #if (len(responseTwoArray) == 0):
      #responseTwoArray = False
    
    print(response2.choices[0].message.content)
    
    
    
    #notion stuff 
    arrayToUse = []
    if responseTwoArray:
      arrayToUse = responseTwoArray
    elif responseOneArray:
      arrayToUse = responseOneArray
    else:
      add_heading("We're sorry. We could not process this response! Please try again!")
    
    print(arrayToUse)
    for item in arrayToUse:
      add_heading(f"Day {item[0]}, Total Time: {str(item[2])}1")
      for task in item[1]:
        add_to_do(task)

    input('enter to continue')

  elif userchoice == 2:
    #search
    auth_config = weaviate.auth.AuthApiKey(os.environ['weaviate_apikey'])
    client = weaviate.Client(
        url="https://hackathon-6mwt235n.weaviate.network",
        auth_client_secret=auth_config,
        additional_headers={
            #"X-Cohere-Api-Key": os.getenv("COHERE_API_KEY"),
            "X-OpenAI-Api-Key": os.environ['xopen_apikey'], 
        }
    )
    client.is_ready()
    
    def semantic_search(query):
        nearText = {
            "concepts": [query], # example from earlier -> 'kitten'
    #         "distance": -139.0,
        }
    
        properties = [
            "des", "title", "url", "rating",
            "_additional {distance}"
        ]
    
        response = (
            client.query
            .get("Courses", properties)
            .with_near_text(nearText)
            .with_limit(5)
            .do()
        )
        #print(response)
        result = response['data']['Get']['Courses']
        
        return result
        
    def print_result(result):
        for item in result:
            print(f"\033[95m{item['title']} ({item['rating']})\033[0m")
            print(f"\033[4m{item['url']}\033[0m")
            print(item['des'])
            print()
    
    
    search_query = input('What courses would you like to search for today?')
    print_result(semantic_search(search_query))
    input('enter to continue')

  elif userchoice == 3:
    exit('Thanks for testing StudySensei!')
  else:
    pass