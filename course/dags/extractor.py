import json
import os.path

from airflow.decorators import dag, task_group, task
from airflow.operators.python import PythonOperator
from pendulum import datetime, duration

from include.datasets import DATASET_COCKTAIL
from include.extractor.extractor import _handle_failed_dag_run, _handle_check_size_failure
from include.tasks import _get_cocktail, _check_size, _validate_cocktail_fields
from airflow.utils.trigger_rule import TriggerRule


@dag(
    start_date=datetime(2025,1,1),
    schedule="@daily",
    catchup=False,
    # on_success_callback="",
    default_args={
        "retries": 2,
        "retry_delay": duration(seconds=2),
        'max_retry_delay': duration(hours=1)
    },
    tags=['ecom'],
    on_failure_callback=_handle_failed_dag_run
)
def extractor():

    get_cocktail = PythonOperator(
        task_id="get_cocktail",
        python_callable=_get_cocktail,
        outlets=[DATASET_COCKTAIL],
        retry_exponential_backoff=True,
        max_retry_delay=duration(minutes=15)
    )

    @task_group(
        # default_args={
        #     'retries':3,
        # }
    )
    def checks():
        check_size = PythonOperator(
            task_id='check_size',
            python_callable=_check_size,
            on_failure_callback=_handle_check_size_failure
        )
        # @task_group()
        # def nexted_task_group():
        #     validate_fields = PythonOperator(
        #         task_id='validate_fields',
        #         python_callable=_validate_cocktail_fields
        #     )
        #
        # check_size >> nexted_task_group()


        validate_fields = PythonOperator(
            task_id='validate_fields',
            python_callable=_validate_cocktail_fields
        )

        check_size >> validate_fields

    # def store_value(ti=None):
    #     ti.xcom_pull(task_ids="checks.validate_fields")


    @task.branch()
    def branch_cocktail_type():
        with open(DATASET_COCKTAIL.uri, 'r') as f:
            data = json.load(f)
            if data['drinks'][0]['strAlcoholic'] == 'Alcoholic':
                return 'alcoholic_drink'
            else:
                return 'non_alcoholic_drink'

    @task()
    def alcoholic_drink():
        print("Alcoholic drink")

    @task()
    def non_alcoholic_drink():
        print("Non alcoholic drink")

    @task(
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
        templates_dict={
            'the_current_date': '{{ ds }}',
            'my_api': '{{ var.value.api }}'
        }
    )
    def clean_data(templates_dict):
        import os
        if os.path.exists(DATASET_COCKTAIL.uri):
            os.remove(DATASET_COCKTAIL.uri)
        else:
            print("File does not exists")
        print(f"Data cleaned for the date {templates_dict["the_current_date"]}")
        print(f'API url {templates_dict['my_api']}')

    get_cocktail >> checks() >> branch_cocktail_type() >> [alcoholic_drink(), non_alcoholic_drink()] >> clean_data()

my_extractor = extractor()

if __name__ == "__main__":
    my_extractor.test()