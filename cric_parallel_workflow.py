from langgraph.graph import StateGraph,START,END
from typing import TypedDict
#state
class batsman(TypedDict):
    run : int 
    ball : int 
    four : int 
    six : int 
    sr: float
    run_boundary_per:float
    ball_per_boundary:float
#sr_calculation 
def cal_sr(state:batsman)->batsman:
    run =state['run']
    ball=state['ball']
    sr=run*100/ball
    return {'sr':sr}
#run boundary_per_calculation 
def cal_rbp(state:batsman)->batsman:
    run =state['run']
    six=state['six']
    four=state['four']
    run_boundary_per=(4*four+six*6)/run*100
    return {'run_boundary_per':run_boundary_per}
def cal_bpb(state:batsman)->batsman:
    ball=state['ball']
    six=state['six']
    four=state['four']
    ball_per_boundary=ball/(four+six)
    return {'ball_per_boundary':ball_per_boundary}
def summary(state:batsman)->batsman:
    print(state)
    return state
#graph 
graph=StateGraph(batsman)
#adding node 
graph.add_node('sr_cal',cal_sr)
graph.add_node('cal_bpb',cal_bpb)
graph.add_node('cal_rbp',cal_rbp)
graph.add_node('summary',summary)

#adding edges 
graph.add_edge(START,'sr_cal')
graph.add_edge(START,'cal_bpb')
graph.add_edge(START,'cal_rbp')
graph.add_edge('sr_cal','summary')
graph.add_edge('cal_bpb','summary')
graph.add_edge('cal_rbp','summary')
graph.add_edge('summary',END)
#grap compile
work_flow=graph.compile()
#invoke 
intial_state={'run':200,'ball':100,'four':10,'six':8}
final_state=work_flow.invoke(intial_state)
