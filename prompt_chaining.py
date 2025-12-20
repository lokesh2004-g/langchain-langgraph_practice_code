from langchain_huggingface import ChatHuggingFace ,HuggingFaceEndpoint
from typing import TypedDict
from langgraph.graph  import StateGraph,START,END
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = ""
llm=HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-0528",
    task="text-generation"
)
model=ChatHuggingFace(llm=llm)
class llmstate(TypedDict):
    question:str
    outline:str
    answer:str
def llm_node_1(state:llmstate)->llmstate:
    question=state['question']
    prompt=f'make a outline on this topic for blog {question}'
    state['outline']=model.invoke(prompt).content
    return state
def llm_node_2(state:llmstate)->llmstate:
    outline=state['outline']
    prompt=f'make a blog for this outline{outline}'
    state['answer']=model.invoke(prompt).content
    return state
#graph
graph=StateGraph(llmstate)
#adding node
graph.add_node("llm1",llm_node_1)
graph.add_node("llm2",llm_node_2)
#adding edge 
graph.add_edge(START,'llm1')
graph.add_edge('llm1','llm2') 
graph.add_edge('llm2',END)
#compile graph 
workflow=graph.compile()
#invoking 
intial_state={'question': "tajmahal"}
final_state=workflow.invoke(intial_state)
print(final_state['answer'])