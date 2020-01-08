import sys, os
import numpy as np
import pandas
import matplotlib.pyplot as plt


if __name__ == '__main__':
    option = sys.argv[1]
    log_paths = sys.argv[2:]
    assert option in ['success_rate', 'eval', 'entropy']
    window = 10
    def get_item(log_file, label):
        data = pandas.read_csv(log_file, index_col=None, comment='#', error_bad_lines=True)
        return data[label].values
    def smooth(array, window):
        out = np.zeros(array.shape[0] - window)
        for i in range(out.shape[0]):
            out[i] = np.mean(array[i:i + window])
        return out
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    for log_path in log_paths:
        progress_file = os.path.join(log_path, 'progress.csv')
        eval_file = os.path.join(log_path, 'eval.csv')
        success_rate = get_item(progress_file, 'ep_reward_mean')
        total_timesteps = get_item(progress_file, 'total_timesteps')
        entropy = get_item(progress_file, 'policy_entropy')
        try:
            eval_reward = get_item(eval_file, 'mean_eval_reward')
            n_updates = get_item(eval_file, 'n_updates')
        except:
            pass
        # success_rate = smooth(success_rate, window)
        # total_timesteps = smooth(total_timesteps, window)
        if option == 'success_rate':
            ax[0].plot(smooth(total_timesteps, window), smooth(success_rate, window), label=log_path)
        elif option == 'eval':
            # ax[0].plot(n_updates*65536, eval_reward, label=log_path)
            
            ax[0].plot(smooth(total_timesteps[n_updates-1], window), smooth(eval_reward, window), label=log_path)
        elif option == 'entropy':
            ax[0].plot(smooth(total_timesteps, window), smooth(entropy, window), label=log_path)
        try:
            augment_steps = get_item(progress_file, 'augment_steps') / 65536
            # augment_steps = smooth(augment_steps, window)
        except:
            augment_steps = np.zeros(total_timesteps.shape)
        ax[1].plot(smooth(total_timesteps, window), smooth(augment_steps, window), label=log_path)
    if option == 'success_rate':
        ax[0].set_title('ep reward mean')
    elif option == 'eval':
        ax[0].set_title('eval success rate')
    elif option == 'entropy':
        ax[0].set_title('entropy')
    ax[1].set_title('augment steps / original rollout steps')
    ax[0].grid()
    ax[1].grid()
    plt.legend()
    plt.show()
    
