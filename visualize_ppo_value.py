import sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from run_ppo import make_env
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines import PPO2


def gen_value_with_obstacle(obs, model, env_hyperparam):
    obstacle_xpos, obstacle_ypos = np.meshgrid(np.linspace(env_hyperparam['xlim'][0], env_hyperparam['xlim'][1], 21),
                                               np.linspace(env_hyperparam['ylim'][0], env_hyperparam['ylim'][1], 21))
    grid_shape = obstacle_xpos.shape
    _obstacle_xpos = np.reshape(obstacle_xpos, (-1, 1))
    _obstacle_ypos = np.reshape(obstacle_ypos, (-1, 1))
    batch_obs = np.tile(obs, (_obstacle_xpos.shape[0], 1))
    batch_obs[:, 6] = _obstacle_xpos[:, 0]
    batch_obs[:, 7] = _obstacle_ypos[:, 0]
    batch_obs[:, 12] = batch_obs[:, 6] - batch_obs[:, 0]
    batch_obs[:, 13] = batch_obs[:, 7] - batch_obs[:, 1]
    # Compute value2
    batch_value = model.value(batch_obs)
    grid_value = np.reshape(batch_value, grid_shape)

    # Compute value1
    subgoal_obs = np.tile(obs, (_obstacle_xpos.shape[0], 1))
    # Achieved goal (current obstacle pos)
    subgoal_obs[:, -10: -7] = subgoal_obs[:, 6: 9]
    subgoal_obs[:, -7: -5] = np.array([[0., 1.]])
    # Desired goal (sampled perturbed obstacle pos)
    obstacle_xy = np.concatenate([_obstacle_xpos, _obstacle_ypos, subgoal_obs[:, 8:9]], axis=-1)
    subgoal_obs[:, -5: -2] = obstacle_xy
    subgoal_obs[:, -2: ] = np.array([[0., 1.]])
    # Value1 aim to answer if the subgoal is easy to achieve
    value1 = model.value(subgoal_obs)
    grid_value1 = np.reshape(value1, grid_shape)

    # min_value = np.min(np.concatenate([np.expand_dims(value1, 1), np.expand_dims(batch_value,1)], axis=1), axis=1)
    # grid_value_min = np.reshape(min_value, grid_shape)
    normalized_value1 = (value1 - np.min(value1)) / (np.max(value1) - np.min(value1))
    normalized_value2 = (batch_value - np.min(batch_value)) / (np.max(batch_value) - np.min(batch_value))
    value_prod = normalized_value1 * normalized_value2
    grid_value_prod = np.reshape(value_prod, grid_shape)

    return obstacle_xpos, obstacle_ypos, grid_value, grid_value1, grid_value_prod


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python visualize_ppo_value.py [load_path]')
    load_path = sys.argv[1]
    env_name = 'FetchPushWallObstacle-v4'
    env_kwargs = dict(random_box=True,
                      heavy_obstacle=True,
                      random_ratio=0.0,
                      random_gripper=True,
                      max_episode_steps=100, )
    env_hyperparam = dict(xlim=(1.05, 1.55), ylim=(0.4, 1.1))
    # env_name = 'MasspointPushSingleObstacle-v2'
    # env_kwargs = dict(random_box=True,
    #                   random_ratio=0.0,
    #                   random_pusher=True,
    #                   max_episode_steps=200, )
    # env_hyperparam = dict(xlim=(-1.0, 4.0), ylim=(-1.5, 3.5),
    #                       )
    n_cpu = 1
    env = make_env(env_id=env_name, seed=None, rank=0, log_dir=None, kwargs=env_kwargs)

    model = PPO2.load(load_path)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    plt.rcParams.update({'font.size': 20, 'xtick.labelsize': 20, 'ytick.labelsize': 20,
                         'axes.labelsize': 20})
    obs = env.reset()
    # while np.argmax(obs[-2:]) != 0 \
    #         or (obs[0] - obs[6]) * (obs[6] - env.pos_wall0[0]) < 0 \
    #         or (obs[3] - env.pos_wall0[0]) * (obs[6] - env.pos_wall0[0]) < 0:
    #     obs = env.reset()
    while not (obs[4] > 0.70 and obs[4] < 0.80):
        obs = env.reset()
    env.set_goal(np.array([1.2, 0.75, 0.425, 1, 0]))
    obs = env.get_obs()
    obs = np.concatenate([obs[key] for key in ['observation', 'achieved_goal', 'desired_goal']])
    for step in range(1):
        img = env.render(mode='rgb_array')
        xs, ys, zs, value1s, value_prods = gen_value_with_obstacle(obs, model, env_hyperparam)
        print(step, 'gripper', obs[:3], 'box', obs[3:6], 'obstacle', obs[6:9], )
        np.save('xs.npy', xs)
        np.save('ys.npy', ys)
        np.save('value1.npy', value1s)
        np.save('value2.npy', zs)
        np.save('value_prod.npy', value_prods)
        plt.imsave(os.path.join(os.path.dirname(load_path), 'tempimg%d.png' % step), img)
        exit()
        # ax[0].cla()
        # ax[1].cla()
        # ax[0].imshow(img)
        # surf = ax[1].contour(xs, ys, zs, 20, cmap=cm.coolwarm)
        # ax[1].clabel(surf, surf.levels, inline=True)
        # ax[1].scatter(obs[6], obs[7], c='tab:brown')
        # ax[1].set_xlim(env_hyperparam['xlim'][0], env_hyperparam['xlim'][1])
        # ax[1].set_ylim(env_hyperparam['xlim'][0], env_hyperparam['xlim'][1])
        # ax[1].set_xlabel('obstacle x')
        # ax[1].set_ylabel('obstacle y')
        # ax[1].set_title('step %d' % step)
        # plt.savefig(os.path.join(os.path.dirname(load_path), 'tempimg%d.png' % step))
        ax.cla()
        surf = ax.contourf((xs - 1.05) / 0.5, (ys - 0.4) / 0.7, value_prods, 15, cmap=cm.coolwarm)
        # ax.clabel(surf, surf.levels, inline=True)
        # ax.set_xlim(env_hyperparam['xlim'][0], env_hyperparam['xlim'][1])
        # ax.set_ylim(env_hyperparam['ylim'][0], env_hyperparam['ylim'][1])
        ax.set_xlabel('x', fontsize=24)
        ax.set_ylabel('y', fontsize=24)
        ax.plot([(1.25-1.05) / 0.5, (1.25 - 1.05) / 0.5], [0, (0.65 - 0.4) / 0.7], 'k', linestyle='--')
        ax.plot([(1.25 - 1.05) / 0.5, (1.25 - 1.05) / 0.5], [(0.85 - 0.4) / 0.7, (1.1 - 0.4) / 0.7], 'k', linestyle='--')
        ax.axis([0., 1., 0., 1.])
        cb = plt.colorbar(surf)
        plt.savefig(os.path.join(os.path.dirname(load_path), 'tempvaluemin_%d.png' % step))
        # plt.pause(0.1)
        cb.remove()
        plt.draw()
        ax.cla()
        surf = ax.contourf((xs - 1.05) / 0.5, (ys - 0.4) / 0.7, value1s, 15, cmap=cm.coolwarm)
        ax.set_xlabel('x', fontsize=24)
        ax.set_ylabel('y', fontsize=24)
        ax.plot([(1.25 - 1.05) / 0.5, (1.25 - 1.05) / 0.5], [0, (0.65 - 0.4) / 0.7], 'k', linestyle='--')
        ax.plot([(1.25 - 1.05) / 0.5, (1.25 - 1.05) / 0.5], [(0.85 - 0.4) / 0.7, (1.1 - 0.4) / 0.7], 'k', linestyle='--')
        ax.axis([0., 1., 0., 1.])
        cb = plt.colorbar(surf)
        plt.savefig(os.path.join(os.path.dirname(load_path), 'tempvalue1_%d.png' % step))
        cb.remove()
        plt.draw()
        ax.cla()
        surf = ax.contourf((xs - 1.05) / 0.5, (ys - 0.4) / 0.7, zs, 15, cmap=cm.coolwarm)
        ax.set_xlabel('x', fontsize=24)
        ax.set_ylabel('y', fontsize=24)
        ax.plot([(1.25 - 1.05) / 0.5, (1.25 - 1.05) / 0.5], [0, (0.65 - 0.4) / 0.7], 'k', linestyle='--')
        ax.plot([(1.25 - 1.05) / 0.5, (1.25 - 1.05) / 0.5], [(0.85 - 0.4) / 0.7, (1.1 - 0.4) / 0.7], 'k', linestyle='--')
        ax.axis([0., 1., 0., 1.])
        cb = plt.colorbar(surf)
        plt.savefig(os.path.join(os.path.dirname(load_path), 'tempvalue2_%d.png' % step))

        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        if done:
            break
    exit()
    model_idx = int(os.path.basename(load_path).strip('.zip').split('_')[1])
    os.system(('ffmpeg -r 2 -start_number 0 -i ' + os.path.dirname(load_path) + '/tempimg%d.png -c:v libx264 -pix_fmt yuv420p ' +
              os.path.join(os.path.dirname(load_path), 'value_obstacle_model_%d.mp4' % model_idx)))
    for step in range(env_kwargs['max_episode_steps']):
        try:
            os.remove(os.path.join(os.path.dirname(load_path), 'tempimg%d.png' % step))
        except:
            pass
