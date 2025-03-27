from datetime import datetime
from airflow.decorators import dag, task
import random


@dag(
    dag_id='random_number_checker_task',
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    description="A simple DAG to generate and check random number using task API",
    tags=["task_api_v2"],
    catchup=False
)
def task_flow():
    @task
    def generate_random_number_task():
        number = random.randint(1, 100)
        print(f"Generated random number:{number} ")
        return number

    @task
    def check_even_odd_task(value):
        number = value
        result = "even" if number % 2 == 0 else "odd"
        print(f"The number {number} is {result}.")

    check_even_odd_task(generate_random_number_task())

task_flow()
