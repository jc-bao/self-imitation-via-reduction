from stable_baselines import PPO2, logger
from stable_baselines.bench import Monitor
from stable_baselines.common import set_global_seeds
from stable_baselines.common.vec_env import SubprocVecEnv
from gym.wrappers import FlattenDictWrapper
from run_ppo_augment import eval_model, log_eval

from push_wall_obstacle import FetchPushWallObstacleEnv_v4
from push_wall_double_obstacle import FetchPushWallDoubleObstacleEnv
from masspoint_env import MasspointPushDoubleObstacleEnv, MasspointPushSingleObstacleEnv, MasspointPushSingleObstacleEnv_v2
# from push_wall import FetchPushWallEnv
# from push_box import FetchPushBoxEnv
import gym
from utils.wrapper import DoneOnSuccessWrapper
import numpy as np

import os, time, argparse, imageio
import matplotlib.pyplot as plt

ENTRY_POINT = {'FetchPushWallObstacle-v4': FetchPushWallObstacleEnv_v4,
               'FetchPushWallObstacleUnlimit-v4': FetchPushWallObstacleEnv_v4,
               'FetchPushWallDoubleObstacle-v1': FetchPushWallDoubleObstacleEnv,
               # 'FetchPushWall-v1': FetchPushWallEnv,
               # 'FetchPushBox-v1': FetchPushBoxEnv,
               }

MASS_ENTRY_POINT = {
    'MasspointPushSingleObstacle-v1': MasspointPushSingleObstacleEnv,
    'MasspointPushSingleObstacle-v2': MasspointPushSingleObstacleEnv_v2,
    'MasspointPushDoubleObstacle-v1': MasspointPushDoubleObstacleEnv,
}

def arg_parse():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--env', default='FetchPushWallObstacle-v4')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--num_timesteps', type=float, default=1e8)
    parser.add_argument('--log_path', default=None, type=str)
    parser.add_argument('--load_path', default=None, type=str)
    parser.add_argument('--random_ratio', default=1.0, type=float)
    parser.add_argument('--play', action="store_true", default=False)
    parser.add_argument('--export_gif', action="store_true", default=False)
    args = parser.parse_args()
    return args

def configure_logger(log_path, **kwargs):
    if log_path is not None:
        logger.configure(log_path)
    else:
        logger.configure(**kwargs)

def make_env(env_id, seed, rank, log_dir=None, allow_early_resets=True, kwargs=None):
    """
    Create a wrapped, monitored gym.Env for MuJoCo.

    :param env_id: (str) the environment ID
    :param seed: (int) the inital seed for RNG
    :param allow_early_resets: (bool) allows early reset of the environment
    :return: (Gym Environment) The mujoco environment
    """
    if env_id in ENTRY_POINT.keys() or env_id in MASS_ENTRY_POINT.keys():
        # env = ENTRY_POINT[env_id](**kwargs)
        # print(env)
        # from gym.wrappers.time_limit import TimeLimit
        kwargs = kwargs.copy()
        max_episode_steps = None
        if 'max_episode_steps' in kwargs:
            max_episode_steps = kwargs['max_episode_steps']
            del kwargs['max_episode_steps']
        if env_id in ENTRY_POINT.keys():
            gym.register(env_id, entry_point=ENTRY_POINT[env_id], max_episode_steps=max_episode_steps, kwargs=kwargs)
        elif env_id in MASS_ENTRY_POINT.keys():
            gym.register(env_id, entry_point=MASS_ENTRY_POINT[env_id], max_episode_steps=max_episode_steps, kwargs=kwargs)
        env = gym.make(env_id)
        # env = TimeLimit(env, max_episode_steps=50)
    else:
        env = gym.make(env_id, reward_type='sparse')
    env = FlattenDictWrapper(env, ['observation', 'achieved_goal', 'desired_goal'])
    env = DoneOnSuccessWrapper(env)
    if log_dir is not None:
        env = Monitor(env, os.path.join(log_dir, str(rank) + ".monitor.csv"), allow_early_resets=allow_early_resets, info_keywords=('is_success',))
    # env.seed(seed + 10000 * rank)
    return env

def main(env_name, seed, num_timesteps, log_path, load_path, play, export_gif, random_ratio):
    log_dir = log_path if (log_path is not None) else "/tmp/stable_baselines_" + time.strftime('%Y-%m-%d-%H-%M-%S')
    configure_logger(log_dir) 
    
    set_global_seeds(seed)

    n_cpu = 32 if not play else 1
    if 'MasspointPushDoubleObstacle' in env_name:
        n_cpu = 64 if not play else 1
    if env_name in ['FetchReach-v1', 'FetchPush-v1', 'CartPole-v1', 'FetchPickAndPlace-v1']:
        env_kwargs = {}
        # pass
    elif env_name in ENTRY_POINT.keys():
        env_kwargs = dict(random_box=True,
                          heavy_obstacle=True,
                          random_ratio=random_ratio,
                          random_gripper=True,
                          max_episode_steps=100, )
    elif env_name in MASS_ENTRY_POINT.keys():
        env_kwargs = dict(random_box=True,
                          random_ratio=random_ratio,
                          random_pusher=True,
                          max_episode_steps=100,)
        if 'MasspointPushSingleObstacle' in env_name:
            env_kwargs['max_episode_steps']=200
        if 'MasspointPushDoubleObstacle' in env_name:
            env_kwargs['max_episode_steps']=300
    else:
        raise NotImplementedError("%s not implemented" % env_name)
    def make_thunk(rank):
        return lambda: make_env(env_id=env_name, seed=seed, rank=rank, log_dir=log_dir, kwargs=env_kwargs)
    env = SubprocVecEnv([make_thunk(i) for i in range(n_cpu)])
    if env_name in ENTRY_POINT.keys():
        eval_env_kwargs = dict(random_box=True,
                               heavy_obstacle=True,
                               random_ratio=0.0,
                               random_gripper=True,
                               max_episode_steps=100, )
    elif env_name in MASS_ENTRY_POINT.keys():
        eval_env_kwargs = dict(random_box=True,
                               random_ratio=0.0,
                               random_pusher=True,
                               max_episode_steps=100,)
    elif env_name in ['FetchPickAndPlace-v1']:
        eval_env_kwargs = {}
    eval_env = make_env(env_id=env_name, seed=seed, rank=0, kwargs=eval_env_kwargs)
    print(eval_env)
    if not play:
        os.makedirs(log_dir, exist_ok=True)
        policy_kwargs = dict(layers=[256, 256])
        # if 'MasspointPushDoubleObstacle' in env_name:
        #     policy_kwargs = dict(layers=[512, 512])
        print(policy_kwargs)
        # policy_kwargs = {}
        # TODO: vectorize env
        model = PPO2('MlpPolicy', env, verbose=1, n_steps=2048, nminibatches=32, lam=0.95, gamma=0.99, noptepochs=10,
                     ent_coef=0.01, learning_rate=3e-4, cliprange=0.2, policy_kwargs=policy_kwargs,
                     )
        def callback(_locals, _globals):
            num_update = _locals["update"]
            if env_name in ENTRY_POINT.keys() or env_name in MASS_ENTRY_POINT.keys():
                mean_eval_reward = eval_model(eval_env, _locals["self"])
                log_eval(num_update, mean_eval_reward)
            if num_update % 10 == 0:
                model_path = os.path.join(log_dir, 'model_' + str(num_update // 10))
                model.save(model_path)
                print('model saved to', model_path)
            return True
        model.learn(total_timesteps=num_timesteps, callback=callback, seed=seed, log_interval=1)
        model.save(os.path.join(log_dir, 'final'))
    
    else:
        assert load_path is not None
        model = PPO2.load(load_path)
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        obs = env.reset()
        goal_dim = env.get_attr('goal')[0].shape[0]
        while np.argmax(obs[0][-goal_dim + 3:]) != 0:
            obs = env.reset()
        # while (obs[0][3] - 1.25) * (obs[0][6] - 1.25) < 0:
        #     obs = env.reset()
        # img = env.render(mode='rgb_array')
        episode_reward = 0.0
        num_episode = 0
        frame_idx = 0
        images = []
        if not 'max_episode_steps' in env_kwargs.keys():
            env_kwargs['max_episode_steps'] = 100
        for i in range(env_kwargs['max_episode_steps'] * 5):
            img = env.render(mode='rgb_array')
            ax.cla()
            ax.imshow(img)
            if env_name == 'FetchPickAndPlace-v1':
                ax.set_title('episode ' + str(num_episode) + ', frame ' + str(frame_idx))
            else:
                ax.set_title('episode ' + str(num_episode) + ', frame ' + str(frame_idx) +
                             ', goal idx ' + str(np.argmax(env.get_attr('goal')[0][3:])))
            images.append(img)
            action, _ = model.predict(obs)
            # print('action', action)
            obs, reward, done, _ = env.step(action)
            episode_reward += reward
            frame_idx += 1
            if not export_gif:
                plt.pause(0.1)
            else:
                plt.savefig(os.path.join(os.path.dirname(load_path), 'tempimg%d.png' % i))
            if done:
                # obs = env.reset()
                # while (obs[0][3] - 1.25) * (obs[0][6] - 1.25) < 0:
                #     obs = env.reset()
                while np.argmax(obs[0][-goal_dim + 3:]) != 0:
                    obs = env.reset()
                print('episode_reward', episode_reward)
                episode_reward = 0.0
                frame_idx = 0
                num_episode += 1
                if num_episode >= 5:
                    break
        # imageio.mimsave(env_name + '.gif', images)
        if export_gif:
            os.system('ffmpeg -r 5 -start_number 0 -i ' + os.path.dirname(load_path) + '/tempimg%d.png -c:v libx264 -pix_fmt yuv420p ' +
                      os.path.join(os.path.dirname(load_path), env_name + '.mp4'))
            for i in range(env_kwargs['max_episode_steps'] * 5):
                # images.append(plt.imread('tempimg' + str(i) + '.png'))
                try:
                    os.remove(os.path.join(os.path.dirname(load_path), 'tempimg' + str(i) + '.png'))
                except:
                    pass

if __name__ == '__main__':
    args = arg_parse()
    print('arg parsed')
    main(env_name=args.env, seed=args.seed, num_timesteps=int(args.num_timesteps), 
         log_path=args.log_path, load_path=args.load_path, play=args.play, export_gif=args.export_gif,
         random_ratio=args.random_ratio)
