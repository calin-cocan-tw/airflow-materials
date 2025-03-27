from airflow.decorators import dag, task
from airflow.datasets import Dataset

file = Dataset("/tmp/data.txt")

@dag(schedule=[file])
def my_consumer_dag():
    @task
    def do_something():
        print("I'm running")
