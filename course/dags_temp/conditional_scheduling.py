# from airflow.decorators import dag, task
# from airflow.datasets import Dataset
#
#
# a = Dataset("data_a")
# b = Dataset("data_b")
# c = Dataset("data_c")
# d = Dataset("data_d")
#
#
# @dag(schedule=(
#         (a | b) &
#         (c | d) ))
# def my_dag():
#     pass
#
# my_dag()


from airflow.decorators import dag, task
from airflow.timetables.datasets import DatasetOrTimeSchedule
from airflow.timetables.trigger import CronTriggerTimetable
from airflow.datasets import Dataset


a = Dataset("data_a")
b = Dataset("data_b")

@dag(schedule=DatasetOrTimeSchedule(timetable=CronTriggerTimetable("0 0 * * *", timezone="UTC"),
                                    datasets=(a | b)
                                    ))
def my_dag():
    pass

my_dag()
