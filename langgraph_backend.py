from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv

load_dotenv()

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
def chat_node(state:ChatState):

    messages=state['messages']
    response=llm.invoke(messages)


    return {"messages": [response]}



check_pointer= MemorySaver()
graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=check_pointer) 

# initial_state = {
#     'messages': [HumanMessage(content='What is the capital of india')]
# }

# response=chatbot.invoke(initial_state)['messages'][-1].content

# print(response)

# thead_id= '1'

# while True:

#     user_message= input('type here :')

#     print("User :",user_message)

#     if user_message.strip().lower() in ["exit , quit , by ,bye"]:
#         break
    
#     Config ={'configurable':{"thread_id":thead_id}}
#     response=chatbot.invoke({'messages':[HumanMessage(content=user_message)]}, config=Config)

#     print ("Ai:",response['messages'][-1].content)  