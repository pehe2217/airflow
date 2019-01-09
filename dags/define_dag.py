"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/incubator-airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'Advisa',
    'depends_on_past': True,
    'start_date': datetime(2019, 1, 1),
    'email': ['per.hedbrant@netlight.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'pers_dag',
    default_args=default_args,
    schedule_interval=timedelta(hours=1),
    catchup=True,
)

def dummy_task_gen_prep():
    return "General Prep"


def dummy_task_backup_x():
    return "Backup task x"


def dummy_task_backup_y():
    return "Backup task y"


def dummy_task_housekeeping_a():
    return "Housekeeping task A"


def dummy_task_housekeeping_b():
    return "Housekeeping task B"


def dummy_task_general_cleanup():
    return "General clean-up"


gen_prep = PythonOperator(
    task_id='general_prep',
    python_callable=dummy_task_gen_prep,
    dag=dag)

backup_x = PythonOperator(
    task_id='backup_X',
    python_callable=dummy_task_backup_x,
    dag=dag)

backup_y = PythonOperator(
    task_id='backup_Y',
    python_callable=dummy_task_backup_y,
    dag=dag)

housekeeping_a = PythonOperator(
    task_id='housekeeping_A',
    python_callable=dummy_task_housekeeping_a,
    dag=dag)


housekeeping_b = PythonOperator(
    task_id='housekeeping_B',
    python_callable=dummy_task_housekeeping_b,
    dag=dag)

gen_cleanup = PythonOperator(
    task_id='general_cleanup',
    python_callable=dummy_task_general_cleanup,
    dag=dag)



gen_prep >> [backup_x, backup_y]
backup_x >> housekeeping_a
backup_y >> housekeeping_b
[housekeeping_a, housekeeping_b] >> gen_cleanup
