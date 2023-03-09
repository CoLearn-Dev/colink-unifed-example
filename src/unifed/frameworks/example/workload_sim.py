import sys
from time import sleep
import random

import flbenchmark.logging

def simulate_workload():
    argv = sys.argv
    # takes 3 args: mode(client/server), output, and logging destination
    if len(argv) != 5:
        raise ValueError(f'Invalid arguments. Got {argv}')
    role, participant_id, output_path, log_path = argv[1:5]
    print('Simulated workload here begin.')
    simulate_logging(participant_id, role)
    print(f"Writing to {output_path} and {log_path}...")
    with open(output_path, 'w') as f:
        f.write(f"Some output for {role} here.")
    with open(log_path, 'w') as f:
        with open(f"./log/{participant_id}.log", 'r') as f2:
            f.write(f2.read())
    # or, alternatively
    # with open(log_path, 'w') as f:
    #     f.write(f"Some log for {role} here.")
    print('Simulated workload here end.')


def simulate_logging(participant_id, role):
    # source: https://github.com/AI-secure/FLBenchmark-toolkit/blob/166a7a42a6906af1190a15c2f9122ddaf808f39a/tutorials/logging/run_fl.py
    if role == 'server':
        with flbenchmark.logging.Logger(id=participant_id, agent_type='aggregator') as logger:
            # weights = [0.0, 0.0]
            with logger.training():
                for i in range(4):
                    # Log every training round
                    with logger.training_round():
                        # Wait for the gradients from clients
                        # w1 = pipe1.recv()
                        # w2 = pipe2.recv()
                        # Average the gradients
                        with logger.computation() as c:
                            sleep(random.random())  # Simulate the computation
                            # weights = [(w1[0]+w2[0])/2, (w1[1]+w2[1])/2]  # Average the gradients
                            c.report_metric('flop', 123)  # Report the cost
                        # Distribute the new model
                        with logger.communication(target_id=1) as c:
                            # pipe1.send(weights)  # Simulate the network communication
                            c.report_metric('byte', 1234)  # Report the cost
                        with logger.communication(target_id=2) as c:
                            # pipe2.send(weights)  # Simulate the network communication
                            c.report_metric('byte', 1234)  # Report the cost
            # Model evaluation
            with logger.model_evaluation() as e:
                sleep(0.1)
                e.report_metric('accuracy', 99.9)
                e.report_metric('mse', 0.2)
    elif role == 'client':
        logger = flbenchmark.logging.Logger(id=participant_id, agent_type='client')
        # Log the data processing
        logger.preprocess_data_start()
        sleep(0.3)
        # weights = [0.1, 0.2]
        logger.preprocess_data_end()
        # Log the training process
        logger.training_start()
        for i in range(4):
            # Log every training round
            logger.training_round_start()
            # inner epochs
            for _ in range(3):
                # Log every computation epoch
                logger.computation_start()
                sleep(random.random())  # Simulate the computation
                # weights = [random.random(), random.random()]  # Get the gradient
                logger.computation_end(metrics={'flop': 123, 'loss': 0.8})  # Report the cost of this computation and loss
            # Upload the gradient
            logger.communication_start(target_id=0)
            # pipe.send(weights)  # Simulate the network communication
            logger.communication_end(metrics={'byte': 1234})  # Report the cost of this communication
            # Wait for the new model
            # weights = pipe.recv()
            logger.training_round_end(metrics={'client_num': 2})  # Report the number of clients in this round
        logger.training_end()
        # End the logging
        logger.end()
    else:
        raise ValueError(f'Invalid role {role}')
