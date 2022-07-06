import matplotlib.pyplot as plots
from plot import Plot

if __name__ == "__main__":
    # Low traffic (Experiment 1, Experiment 2, Experiment 3)
    # Rewards
    Plot_ = Plot('results_data/2.figure_training_cumulative_reward_training_high_traffic', 15)
    # Experiment 1
    Plot_.draw(plots, '2.cumulative_reward_training_high_traffic',
               './results_data/2.figure_training_cumulative_reward_training_high_traffic/dataRewards_results_training_q5.csv',
               'Episode',
               'Cumulative negative reward', 'r', 'Training, high traffic, QL, gamma (0.50) ', '')

    # Experiment 2
    Plot_.draw(plots, '2.cumulative_reward_training_high_traffic',
               './results_data/2.figure_training_cumulative_reward_training_high_traffic/dataRewards_results_training_q6.csv',
               'Episode',
               'Cumulative negative reward', 'b', 'Training, high traffic, QL, gamma (0.75) ', '')

    # Experiment 3
    Plot_.draw(plots, '2.cumulative_reward_training_high_traffic',
               './results_data/2.figure_training_cumulative_reward_training_high_traffic/dataRewards_results_training_p5.csv',
               'Episode',
               'Cumulative negative reward', 'm', 'Training, high traffic, VP, gamma (0.50) ', '')

    # Experiment 4
    Plot_.draw(plots, '2.cumulative_reward_training_high_traffic',
               './results_data/2.figure_training_cumulative_reward_training_high_traffic/dataRewards_results_training_p6.csv',
               'Episode',
               'Cumulative negative reward', 'y', 'Training, high traffic, VP, gamma (0.75) ', '')
