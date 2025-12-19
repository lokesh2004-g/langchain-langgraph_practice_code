from langgraph.graph import StateGraph,START,END
from typing import TypedDict
#state 
class bmistate(TypedDict):
    weight_kg:float
    height_m: float
    bmi:float
def bmi_calculator(state:bmistate)->bmistate:
    h=state['height_m']
    w=state['weight_kg']
    bmi=w/(h**2)
    state['bmi']=bmi
    return state

#graph
graph=StateGraph(bmistate)
#node of graph
graph.add_node('bmi_cal',bmi_calculator)
#adding edge
graph.add_edge(START,'bmi_cal')
graph.add_edge('bmi_cal',END)
#compile graph 
workflow=graph.compile()
#exicution 
intial_state={'weight_kg':80,'height_m':1.73}
final_state=workflow.invoke(intial_state)
print(final_state)