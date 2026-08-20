from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.services.agent_service import run_agent
from app.services.audit_service import audit_service
from agents.nodes.rachit import rachit_node

def _audit(db, task_id, agent, action, status="success", event="", details=""):
    try: audit_service.create(db, task_id, agent, action, status, event, details)
    except Exception as exc: print("Audit error:", exc)

def create_task(db: Session, task: TaskCreate):
    db_task=Task(title=task.title,prompt=task.prompt,status="PENDING",risk_level="LOW",errors=[],trace=[])
    db.add(db_task); db.commit(); db.refresh(db_task)
    try:
        db_task.status="RUNNING"; db_task.current_agent="KARMA"; db.commit(); _audit(db,db_task.id,"KARMA","route","success","Task routed","KARMA accepted task")
        result=run_agent(db_task)
        trace=[]
        if result.get("plan"):
            db_task.plan=result["plan"]; db_task.current_agent="PRAGYA"; trace.append({"agent":"PRAGYA","status":"COMPLETED","description":"Plan generated"}); _audit(db,db_task.id,"PRAGYA","planning","success","Planning complete","Structured plan generated")
        if result.get("risk_report"):
            db_task.risk_report=result["risk_report"]; trace.append({"agent":"MURPHY","status":"COMPLETED","description":"Risk analysis completed"}); _audit(db,db_task.id,"MURPHY","risk_analysis","success","Risk analysis complete",result["risk_report"].get("recommendation", ""))
        if result.get("policy_verdict"):
            db_task.policy_verdict=result["policy_verdict"]; db_task.risk_level=result["policy_verdict"].get("risk_tier","LOW"); trace.append({"agent":"MARYADA","status":"COMPLETED","description":"Policy verdict evaluated"}); _audit(db,db_task.id,"MARYADA","policy_check","blocked" if not result["policy_verdict"].get("approved") else "success","Policy verdict",result["policy_verdict"].get("justification",""))
        if result.get("execution_result"):
            ex=result["execution_result"]; db_task.execution_result=ex if isinstance(ex,dict) else {"status":"COMPLETED","message":str(ex),"executed_steps":len((db_task.plan or {}).get("steps",[]))}; trace.append({"agent":"RACHIT","status":"COMPLETED","description":"Approved execution simulated"}); _audit(db,db_task.id,"RACHIT","execute","success","Execution complete",str(db_task.execution_result))
        verdict=result.get("policy_verdict")
        if verdict and not verdict.get("approved"):
            db_task.status="BLOCKED"; db_task.current_agent="MARYADA"; trace.append({"agent":"RACHIT","status":"WAITING","description":"Waiting for human approval"})
        else:
            db_task.status="COMPLETED"; db_task.current_agent="RACHIT" if db_task.execution_result else "MARYADA"
        db_task.errors=result.get("errors",[]); db_task.trace=trace
    except Exception as e:
        db_task.status="FAILED"; db_task.errors=[str(e)]; _audit(db,db_task.id,"SYSTEM","execution","failed","Task failed",str(e))
    db.commit(); db.refresh(db_task); return db_task

def get_all_tasks(db): return db.query(Task).order_by(Task.created_at.desc()).all()
def get_task(db,task_id): return db.query(Task).filter(Task.id==task_id).first()

def approve_task(db,task_id):
    task=get_task(db,task_id)
    if not task: return None
    if task.status!="BLOCKED": return task
    try:
        result=rachit_node({"task_id":str(task.id),"intent":task.prompt,"plan":task.plan or {},"errors":[]})
        ex=result.get("execution_result")
        task.execution_result=ex if isinstance(ex,dict) else {"status":"COMPLETED","message":str(ex),"executed_steps":len((task.plan or {}).get("steps",[]))}
        if task.policy_verdict: task.policy_verdict={**task.policy_verdict,"approved":True,"requires_human":False}
        task.status="COMPLETED"; task.current_agent="RACHIT"
        task.trace=list(task.trace or []) + [{"agent":"MARYADA","status":"APPROVED","description":"Founder approved blocked task"},{"agent":"RACHIT","status":"COMPLETED","description":"Approved execution simulated"}]
        _audit(db,task.id,"FOUNDER","approval","success","Human approval","Task approved by Founder")
        _audit(db,task.id,"RACHIT","execute","success","Execution complete",str(task.execution_result))
    except Exception as e:
        task.status="FAILED"; task.errors=list(task.errors or [])+[str(e)]; _audit(db,task.id,"RACHIT","execute","failed","Execution failed",str(e))
    db.commit(); db.refresh(task); return task

def reject_task(db,task_id):
    task=get_task(db,task_id)
    if not task:return None
    task.status="FAILED"; task.current_agent="MARYADA"; task.trace=list(task.trace or [])+[{"agent":"FOUNDER","status":"REJECTED","description":"Founder rejected task"}]; _audit(db,task.id,"FOUNDER","rejection","blocked","Human rejection","Task rejected by Founder"); db.commit(); db.refresh(task); return task
