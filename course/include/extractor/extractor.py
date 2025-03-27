def _handle_failed_dag_run(context):
    print(f"""DAG run failed with the task {context["task_instance"].task_id} 
    for the data interval {context["prev_ds"]} and {context["next_ds"]}""")
    print(f"ContextType:{type(context)}, ContextData: {str(context)}")

def _handle_check_size_failure(context):
    print(f"There is no cocktail process for data interval { context['prev_ds'] } and { context['next_ds'] }")