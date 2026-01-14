import numpy as np
import threading
from queue import Queue
from typing import Dict, List

# Define the Job Class
class Job:
    def __init__(self, id: int, name: str, reward: int, duration: int):
        self.id = id
        self.name = name
        self.reward = reward
        self.duration = duration

# Define the Agent Class
class Agent:
    def __init__(self, id: int, name: str, level: int):
        self.id = id
        self.name = name
        self.level = level
        self.jobs = []

    def assign_job(self, job: Job):
        self.jobs.append(job)

    def update_level(self, level: int):
        self.level = level

# Define the Job System Class
class JobSystem:
    def __init__(self):
        self.agents: Dict[int, Agent] = {}
        self.jobs: Dict[int, Job] = {}
        self.queue = Queue()
        self.lock = threading.Lock()

    def add_agent(self, agent: Agent):
        with self.lock:
            self.agents[agent.id] = agent

    def add_job(self, job: Job):
        with self.lock:
            self.jobs[job.id] = job

    def assign_job_to_agent(self, agent_id: int, job_id: int):
        with self.lock:
            if agent_id in self.agents and job_id in self.jobs:
                self.agents[agent_id].assign_job(self.jobs[job_id])

    def update_agent_level(self, agent_id: int, level: int):
        with self.lock:
            if agent_id in self.agents:
                self.agents[agent_id].update_level(level)

    def process_queue(self):
        while True:
            agent_id, job_id = self.queue.get()
            self.assign_job_to_agent(agent_id, job_id)
            self.queue.task_done()

    def start_processing(self):
        for _ in range(10):
            threading.Thread(target=self.process_queue, daemon=True).start()

# Initialize the Job System
job_system = JobSystem()

# Create 100 Agents
for i in range(1, 101):
    agent = Agent(i, f"Agent {i}", 1)
    job_system.add_agent(agent)

# Create Jobs
jobs = [
    Job(1, "Job 1", 100, 10),
    Job(2, "Job 2", 200, 20),
    Job(3, "Job 3", 300, 30),
]

# Add Jobs to the Job System
for job in jobs:
    job_system.add_job(job)

# Assign Jobs to Agents
for i in range(1, 101):
    job_system.queue.put((i, np.random.randint(1, 4)))

# Start processing the queue
job_system.start_processing()

# Wait for all tasks to be completed
job_system.queue.join()