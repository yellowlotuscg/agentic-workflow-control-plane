from dataclasses import dataclass, field
@dataclass
class Job:
    goal: str
    steps: list[str]
    state: str = "planned"
    artifacts: dict = field(default_factory=dict)
    events: list[str] = field(default_factory=list)
class WorkflowEngine:
    def __init__(self, actions): self.actions=actions
    def run(self, job):
        job.state="running"; job.events.append("started")
        for step in job.steps:
            if step == "external_action": job.state="waiting_for_approval"; job.events.append("approval_required"); return job
            if step not in self.actions: job.state="failed"; job.events.append(f"unknown_step:{step}"); return job
            job.artifacts[step]=self.actions[step](job); job.events.append(f"completed:{step}")
        job.state="completed"; job.events.append("completed"); return job
