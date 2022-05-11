run_worker:
	huey_consumer worker.huey

run_task:
	python -c "import worker; result = worker.delayed_random(3); result(blocking=True, timeout=5)"
