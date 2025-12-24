#library import 
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langgraph.graph import START,END,StateGraph
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import add_messages
import os 
from langgraph.checkpoint.memory import MemorySaver

#loading model
os.environ["HUGGINGFACEHUB_API_TOKEN"] = ""


llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-0528",
    task="text-generation"
)    
model=ChatHuggingFace(llm=llm)

#SATAE
class chatstate(TypedDict):
    message:Annotated[list[BaseMessage],add_messages]

#graph
graph=StateGraph(chatstate)


#FUNCTION 
#llm_function 
def llm_function(state:chatstate):
    message=state["message"]
    responce=model.invoke(message)
    return {'message' :[responce]}

#add_nodes
graph.add_node('llm_function',llm_function)

#add_edges
graph.add_edge(START,'llm_function')
graph.add_edge('llm_function',END)

#making checkpointer 
checkpointer=MemorySaver()
thread_id=1

#compile
chatbot=graph.compile(checkpointer=checkpointer)

#while loop 
while True :
    user_input=input('write message:')
    print('you:',user_input)
    if user_input =="exit":
        break
    #config
    config={'configurable':{'thread_id':thread_id}}
    #invoke mode
    initial_state={
    'message' :[HumanMessage(content= f'give straight forward answer of {user_input} answer must be small and do not explain what you are thinking ')]}
    final_state=chatbot.invoke(initial_state,config=config)
    responce=final_state['message'][-1].content
    print('AI:',responce)



    