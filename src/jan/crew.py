from typing import Type
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

import litellm

litellm.set_verbose=True

class HumanInputInput(BaseModel):
    """Input schema for HumanInput."""
    question: str = Field(..., description="Question to ask to the human.")

class HumanInput(BaseTool):
    name: str = "Human input"
    description: str = "This tool can be used to as a human a question. Either for a clarification, getting addional info, veryfying unlikely information or confirmation"
    args_schema: Type[BaseModel] = HumanInputInput

    def _run(self, question: str) -> str:        
        return input(question)


@CrewBase
class Jan():
	"""Jan crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	
	@agent
	def meal_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['meal_analyst'],
			verbose=True,			
		)
	@agent
	def meal_interviewer(self) -> Agent:
		return Agent(
			config=self.agents_config['meal_interviewer'],
			verbose=True,
			allow_delegation=True
		)
	
	@task
	def analyze_food_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_food_task'],		
			output_file='report.md'	
		)
	@task
	def gather_food_journal(self) -> Task:
		return Task(
			config=self.tasks_config['gather_food_journal'],		
			tools=[HumanInput()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Jan crew"""
		return Crew(
			agents=[self.meal_interviewer(), self.meal_analyst()], 
			tasks=[self.gather_food_journal(), self.analyze_food_task()], 
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
