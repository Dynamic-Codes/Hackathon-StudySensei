import os
import notion_client

notion = notion_client.Client(auth=os.environ['notion_apikey'])

page = "513c10744a5945c6bd760ad66c46bd1f"

def add_to_do(to_do):
  
  task = to_do
  
    #{ "page_id": "270425552049459baa156dc63bcf5db0" });
  notion.blocks.children.append(block_id=page, children=[{
      "to_do": {
        "rich_text": [
              {
                "text": {
                  "content": task,
                },
              
              }
            ]
      }
    }]) 
  
def add_heading(heading):
  notion.blocks.children.append(block_id=page, children=[{
      "heading_3": {
        "rich_text": [
              {
                "text": {
                  "content": heading,
                },
              
              }
            ]
      }
    }]) 
  
#pageurl
#page = client.get_block("https://www.notion.so/Biology-Course-270425552049459baa156dc63bcf5db0?pvs=4")
#https://www.notion.so/Biology-Course-513c10744a5945c6bd760ad66c46bd1f?pvs=4