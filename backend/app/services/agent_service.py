from app.services.kosh_service import kosh
from agents.graph import brahma_app

def run_agent(task):
    knowledge=kosh.retrieve(task.prompt)
    state={"task_id":str(task.id),"trace_id":f"task-{task.id}","intent":task.prompt,"knowledge":knowledge,"current_agent":"KARMA","errors":[],"plan":None,"risk_report":None,"policy_verdict":None,"execution_result":None}
    return brahma_app.invoke(state)
