from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langgraph.graph import StateGraph,END,START
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
import os
import operator
from typing import TypedDict,Annotated
from pydantic import BaseModel,Field
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_##############################"
#model loadig
llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-0528",
    task="text-generation"
)    
model=ChatHuggingFace(llm=llm)
#making a output pareser 
class schema(BaseModel):
    feedback:str=Field(description="a feedback of postive and neative point in  essay")
    score:int=Field(description="give a score on 1 to 10 ")

parser=PydanticOutputParser(pydantic_object=schema)
#templat 
templat=PromptTemplate(
    template="give feedback and a score for 1 to 10 according to this 100 word's essay  {topic}\n {format_instruction}",
    input_variables=['topic'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)
#topic of essay
topic="The Taj Mahal is one of the most beautiful monuments in the world." \
" It is located in Agra, India, on the banks of the Yamuna River." \
" Mughal emperor Shah Jahan built the Taj Mahal in memory of his beloved wife Mumtaz Mahal." \
" It is made of white marble and is famous for its fine carvings and precious stone inlay work." \
" The monument looks different at different times of the day due to changing sunlight." \
" The Taj Mahal is a symbol of love and attracts millions of tourists every year from all over the world"
#state
class upsc_state(TypedDict):
    essay:str
    clarity_feedback:str
    analysis_feedback:str
    language_feedback:str
    overall_feedback:str
    indiual_score:Annotated[list[int],operator.add]
    avg_score: float
#function 
#clarity_function 
def llm_calrity(state:upsc_state)->upsc_state:
#template
    topic=state['essay']
    templat1=PromptTemplate(
    template="give feedback in 10 word nd a score for 1 to 10 according to this 100 word's essay on the basies of clarity of thourght  {topic}\n {format_instruction}",
    input_variables=['topic'],
    partial_variables={'format_instruction':parser.get_format_instructions()})
    #chain 
    chain1=templat1|model|parser
    result1=chain1.invoke({'topic': topic })
    return { 'clarity_feedback':result1.feedback,'indiual_score':[result1.score]}
#language_function 
def llm_language(state:upsc_state)->upsc_state:
#template
    topic=state['essay']
    templat2=PromptTemplate(
    template="give feedback in 10 word  and a score for 1 to 10 according to this 100 word's essay on the basies of language use in this essay  {topic}\n {format_instruction}",
    input_variables=['topic'],
    partial_variables={'format_instruction':parser.get_format_instructions()})
    #chain 
    chain2=templat2|model|parser
    result2=chain2.invoke({'topic': topic })
    return { 'language_feedback':result2.feedback,'indiual_score':[result2.score]}   
#analysis_function  
def llm_analysis(state:upsc_state)->upsc_state:
#template
    topic=state['essay']
    templat3=PromptTemplate(
    template="give feedback in 10 word  and a score for 1 to 10 according to this 100 word's essay on the basies of topic analysis and information  use in this essay  {topic}\n {format_instruction}",
    input_variables=['topic'],
    partial_variables={'format_instruction':parser.get_format_instructions()})
    #chain 
    chain3=templat3|model|parser
    result3=chain3.invoke({'topic': topic })
    return { 'analysis_feedback':result3.feedback,'indiual_score':[result3.score],}
#summary 
def summary(state:upsc_state)->upsc_state:
    text1=state['analysis_feedback']
    text2=state['language_feedback']
    text3=state['clarity_feedback']
    result=model.invoke(f'generate a summary on the basis of {text1},{text2},{text3}')
    overall_feedback=result.content
    avg_score=sum(state['indiual_score'])/3
    return {'overall_feedback':overall_feedback,'avg_score':avg_score}
#graph
graph=StateGraph(upsc_state)
#adding nodes
graph.add_node('clarity',llm_calrity)
graph.add_node('analysis',llm_analysis)
graph.add_node('language',llm_language)
graph.add_node('summary',summary)
#connecting edge
graph.add_edge(START,'clarity')
graph.add_edge(START,'analysis')
graph.add_edge(START,'language')

graph.add_edge('clarity','summary')
graph.add_edge('analysis','summary')
graph.add_edge('language','summary')

graph.add_edge('summary',END)
#compiling graph
workflow=graph.compile()
#invoke
intial_state={'essay':topic}
final_state=workflow.invoke(intial_state)
print(final_state['overall_feedback'])



