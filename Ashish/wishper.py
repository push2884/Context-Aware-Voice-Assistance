from langchain_openai import ChatOpenAI  
import os  
import httpx  
client = httpx.Client(verify=False) 
llm = ChatOpenAI( 
base_url="https://genailab.tcs.in" ,
model = "azure/genailab-maas-whisper ", 
api_key="sk-LUN1OjfXBHi9IwljISMkag", # Will be provided during event.  And this key is for 

http_client = client 
) 
llm.invoke("Hi") 