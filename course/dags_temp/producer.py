from airflow.decorators import dag, task
from airflow.datasets import Dataset

file = Dataset("/tmp/data.txt")


@dag(...)
def my_producer_dag():
    @task
    def task_a(outlets: [file]):
        with open(file.uri, "a") as f:
            f.write("producer update")
