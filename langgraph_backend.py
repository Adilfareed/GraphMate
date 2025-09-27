from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3 
from dotenv import load_dotenv

load_dotenv()

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
def chat_node(state:ChatState):

    messages=state['messages']
    response=llm.invoke(messages)


    return {"messages": [response]}

db=sqlite3.connect("graphMate.db", check_same_thread=False)

check_pointer=SqliteSaver(conn=db) 
graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=check_pointer) 

def retreve_all_threads():
    all_threads = set()
    for checkpont in  check_pointer.list(None):
        all_threads.add(checkpont.config['configurable']['thread_id'])

        
    return(list(all_threads))



# thead_id= '1'

# while True:

#     user_message= input('type here :')

#     print("User :",user_message)

#     if user_message.strip().lower() in ["exit , quit , by ,bye"]:
#         break
    
#     Config ={'configurable':{"thread_id":thead_id}}
#     response=chatbot.invoke({'messages':[HumanMessage(content=user_message)]}, config=Config)

#     print ("Ai:",response['messages'][-1].content)  