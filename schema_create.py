#Running this file deletes all data in this current schema
import os
import weaviate
import json

auth_config = weaviate.auth.AuthApiKey(
    api_key='MhqYc1yL0oCEbnLwd2LdPCkm0sAYLqWQWk5F')
client = weaviate.Client(
    url="https://hackathon-6mwt235n.weaviate.network",
    auth_client_secret=auth_config,
    additional_headers={
        #"X-Cohere-Api-Key": os.getenv("COHERE_API_KEY"),
        "X-OpenAI-Api-Key": "",
    })
client.is_ready()

article_schema = {
    "class":
    "Courses",
    "description":
    "Random Course",
    "vectorizer":
    "text2vec-openai",  #multi-lingual
    "moduleConfig": {
        "text2vec-openai": {},
        "generative-openai": {},
    },
    "vectorIndexConfig": {
        "distance": "dot"
    },
    "properties": [
        {
            "name": "des",
            "dataType": ["text"],
            "description": "Course body",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": False,
                    "vectorizePropertyName": False
                }
            }
        },
        {
            "name": "title",
            "dataType": ["string"],
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": False,
                    "vectorizePropertyName": False
                }
            }
        },
        {
            "name": "url",
            "dataType": ["string"],
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True
                }
            }
        },
        {
            "name": "author",
            "dataType": ["string"],
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": False,
                    "vectorizePropertyName": False
                }
            }
        },
        {
            "name": "rating",
            "dataType": ["number"],
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True
                }
            }
        },
    ]
}

# add the schema
client.schema.delete_all()
client.schema.create_class(article_schema)

print("The schema has been created")
