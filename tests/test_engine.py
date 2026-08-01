import unittest
from workflow.engine import Job, WorkflowEngine
class Tests(unittest.TestCase):
 def test_external_action_stops(self):
  j=WorkflowEngine({"a":lambda j:"artifact"}).run(Job("x",["a","external_action"]))
  self.assertEqual(j.state,"waiting_for_approval"); self.assertEqual(j.artifacts["a"],"artifact")
if __name__=="__main__": unittest.main()
