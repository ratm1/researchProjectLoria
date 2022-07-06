import matplotlib.pyplot as plots
from plot import Plot

if __name__ == "__main__":
    # Low traffic (Experiment 1, Experiment 2, Experiment 3)
    # Rewards
    Plot_ = Plot('results_data/1.figure_training_cumulative_reward_training_low_traffic')
    Plot_.setFontSize(15)

    # Experiment 1

    Plot_.draw(plots, 'cumulative_reward_training_low_traffic',
               './results_data/1.figure_training_cumulative_reward_training_low_traffic'
               '/dataRewards_results_training_q2.csv', 'Episode',
               'Cumulative negative reward', 'r', 'Training, low traffic, QL, gamma (0.50) ', '')


    # # Experiment 2

    Plot_.draw(plots, 'cumulative_reward_training_low_traffic',
               './results_data/1.figure_training_cumulative_reward_training_low_traffic'
               '/dataRewards_results_training_q3.csv', 'Episode',
               'Cumulative negative reward', 'b', 'Training, low traffic, QL, gamma (0.75) ', '')


    # Experiment 3

    Plot_.draw(plots, 'cumulative_reward_training_low_traffic',
               './results_data/1.figure_training_cumulative_reward_training_low_traffic'
               '/dataRewards_results_training_p2.csv', 'Episode',
               'Cumulative negative reward', 'm', 'Training, low traffic, VP, gamma (0.50) ', '')

    # Experiment 4

    Plot_.draw(plots, 'cumulative_reward_training_low_traffic',
               './results_data/1.figure_training_cumulative_reward_training_low_traffic'
               '/dataRewards_results_training_p3.csv', 'Episode',
               'Cumulative negative reward', 'y', 'Training, low traffic, VP, gamma (0.75) ', '')
