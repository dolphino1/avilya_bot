from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

import logging
if __name__ == '__main__':
    logging.basicConfig(level='INFO')

    training_data_file = 'rasa_api/data/stories.md'
    model_path = 'rasa_api/models/dialogue'

    agent = Agent("rasa_api/domain.yml",
                  policies=[MemoizationPolicy()])

    agent.train(training_data_file,
                augmentation_factor=50,
                max_history=1,
                epochs=500,
                batch_size=10,
                validation_split=0.2)

    agent.persist(model_path)
