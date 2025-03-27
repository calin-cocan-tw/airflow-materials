# from airflow import DAG
# from airflow.operators.python import PythonOperator
#
# dag = DAG()
#
# ta = PythonOperator(task_id='ta', dag=dag)
# tb = PythonOperator(task_id='ta', dag=dag)
# tc = PythonOperator(task_id='ta', dag=dag)

# from airflow import DAG
# from airflow.operators.python import PythonOperator
#
# with DAG(...):
#     ta = PythonOperator(task_id='ta')
#     tb = PythonOperator(task_id='ta')
#     tc = PythonOperator(task_id='ta')


from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, duration

from include.datasets import DATASET_COCKTAIL


@dag(
    start_date=datetime(2025,1,1),
    schedule=[DATASET_COCKTAIL],
    catchup=True,
    description='This DAG processes ecommerce data',
    tags = ["team_a", "ecom", "pii"],
    default_args={'retries': 2},
    dagrun_timeout=duration(minutes=20),
    max_consecutive_failed_dag_runs=2,
    # max_active_runs=1,

     )
def ecom():
    ta = EmptyOperator(
        task_id='ta',
    )

ecom()



# @dag()
# def retail():
#     extract_sales = SQLExecuteQueryOperator(
#         task_id = "extract_sales",
#         sql= f"""
#             SELECT *
#             FROM sales
#             WHERE DATE(ts) = DATE({{}date_interval_env}} - INTERVAL '1 day')
#             """
#     )
#
# retail()