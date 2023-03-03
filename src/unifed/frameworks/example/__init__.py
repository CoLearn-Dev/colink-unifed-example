import sys

from unifed.frameworks.example import protocol


def run_protocol():
    print('Running protocol...')
    protocol.pop.run()  # FIXME: require extra testing here


def simulate_workload():
    argv = sys.argv
    # takes 3 args: mode(client/server), output, and logging destination
    if len(argv) != 4:
        raise ValueError(f'Invalid arguments. Got {argv}')
    role, output_path, log_path = argv[1:4]
    print('Simulated workload here begin.')
    print(f"Writing to {output_path} and {log_path}...")
    with open(output_path, 'w') as f:
        f.write(f"Some output for {role} here.")
    with open(log_path, 'w') as f:
        f.write(f"Some log for {role} here.")
    print('Simulated workload here end.')
