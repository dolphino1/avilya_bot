tests:
	@echo "Running all tests ..."
	python `which nosetests`

tests_with_coverage:
	@echo "Running all tests with coverage ..."
	python `which nosetests` --with-coverage --cover-package=.

train_nlu_model:
	@echo "Training Rasa-NLU model on intents..."
	python -m rasa_nlu.train -c rasa_api/nlu_config.json --fixed_model_name current


train_core_model:
	@echo "Training Rasa-Core Model on stories"
	python -m rasa_core.train -s rasa_api/data/stories.md -d rasa_api/domain.yml -o rasa_api/models/dialogue --epochs 300

	cd rasa_api && python -m rasa_core.train -s data/stories.md -d domain.yml -o models/dialogue

train_memory_only_core_model:
	python rasa_api/train.py

run_server:
	python rasa_api/run_server.py runserver -h 0.0.0.0
