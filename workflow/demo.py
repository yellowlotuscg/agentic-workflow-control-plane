from .engine import Job, WorkflowEngine
def main():
 e=WorkflowEngine({"research":lambda j:"synthetic business facts","draft":lambda j:"approval-ready brief"})
 j=e.run(Job("qualify a lead",["research","draft","external_action"]))
 print({"state":j.state,"artifacts":j.artifacts,"events":j.events})
if __name__=="__main__": main()
