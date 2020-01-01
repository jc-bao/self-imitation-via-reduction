import os
import copy
from gym import utils
from masspoint_base import MasspointPushEnv
import gym.envs.robotics.utils as robot_utils
import numpy as np


MODEL_XML_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'masspoint', 'double_obstacle.xml')


class MasspointPushDoubleObstacleEnv(MasspointPushEnv, utils.EzPickle):
    def __init__(self, reward_type='sparse', random_box=True,
                 random_ratio=1.0, random_pusher=False):
        XML_PATH = MODEL_XML_PATH
        initial_qpos = {
            'masspoint:slidex': 0.0,
            'masspoint:slidey': 0.0,
            'object0:slidex': 0.0,
            'object0:slidey': 0.0,
            'object1:joint': [1.4, 0.47, 0.4, 1., 0., 0., 0.],
            'object2:joint': [1.4, 0.6, 0.4, 1., 0., 0., 0.],
        }
        self.random_box = random_box
        self.random_ratio = random_ratio
        self.random_pusher = random_pusher
        MasspointPushEnv.__init__(
            self, XML_PATH, n_substeps=20,
            target_in_the_air=False, target_offset=0.0,
            obj_range=0.3, target_range=0.3, distance_threshold=0.05,
            initial_qpos=initial_qpos, reward_type=reward_type, n_object=3)
        utils.EzPickle.__init__(self)
        self.pos_wall0 = self.sim.model.geom_pos[self.sim.model.geom_name2id('wall0')]
        self.pos_wall2 = self.sim.model.geom_pos[self.sim.model.geom_name2id('wall2')]
        self.size_wall = self.sim.model.geom_size[self.sim.model.geom_name2id('wall0')]
        self.size_obstacle = self.sim.model.geom_size[self.sim.model.geom_name2id('object1')]
        self.size_object = self.sim.model.geom_size[self.sim.model.geom_name2id('object0')]

    def _reset_sim(self):
        # self.sim.set_state(self.initial_state)
        sim_state = copy.deepcopy(self.initial_state)
        # TODO: randomize masspoint pos
        if self.random_pusher:
            masspoint_jointx_i = self.sim.model.get_joint_qpos_addr('masspoint:slidex')
            masspoint_jointy_i = self.sim.model.get_joint_qpos_addr('masspoint:slidey')
            masspoint_pos = self.np_random.uniform([1.0, 0.45], [1.6, 1.05])
            sim_state.qpos[masspoint_jointx_i] = masspoint_pos[0]
            sim_state.qpos[masspoint_jointy_i] = masspoint_pos[1]
        else:
            masspoint_pos = self.initial_masspoint_xpos[:2]

        def config_valid(object_xpos, obstacle1_xpos, obstacle2_xpos):
            if np.linalg.norm(object_xpos - masspoint_pos) >= 0.1 \
                    and abs(object_xpos[1] - self.pos_wall0[1]) >= self.size_object[1] + self.size_wall[1] \
                    and abs(object_xpos[1] - self.pos_wall2[1]) >= self.size_object[1] + self.size_wall[1] \
                    and abs(obstacle1_xpos[1] - self.pos_wall0[1]) >= self.size_obstacle[1] + self.size_wall[1] \
                    and abs(obstacle1_xpos[1] - self.pos_wall2[1]) >= self.size_obstacle[1] + self.size_wall[1] \
                    and abs(obstacle2_xpos[1] - self.pos_wall0[1]) >= self.size_obstacle[1] + self.size_wall[1] \
                    and abs(obstacle2_xpos[1] - self.pos_wall2[1]) >= self.size_obstacle[1] + self.size_wall[1] \
                    and (abs(object_xpos[0] - obstacle1_xpos[0]) >= self.size_object[0] + self.size_obstacle[0] or abs(
                            object_xpos[1] - obstacle1_xpos[1]) >= self.size_object[1] + self.size_obstacle[1]) \
                    and (abs(object_xpos[0] - obstacle2_xpos[0]) >= self.size_object[0] + self.size_obstacle[0] or abs(
                            object_xpos[1] - obstacle2_xpos[1]) >= self.size_object[1] + self.size_obstacle[1]) \
                    and (abs(obstacle1_xpos[0] - obstacle2_xpos[0]) >= self.size_obstacle[0] * 2 or abs(
                            obstacle1_xpos[1] - obstacle2_xpos[1]) >= self.size_obstacle[1] * 2):
                return True
            else:
                return False

        # Randomize start position of object.
        if self.random_box and self.np_random.uniform() < self.random_ratio:
            self.sample_hard = False
            object_xpos = self.initial_masspoint_xpos[:2] + self.np_random.uniform(-self.obj_range, self.obj_range, size=2)
            stick1_xpos = object_xpos.copy()
            stick2_xpos = object_xpos.copy()
            while not config_valid(object_xpos, stick1_xpos, stick2_xpos):
                object_xpos = self.initial_masspoint_xpos[:2] + self.np_random.uniform(-self.obj_range, self.obj_range, size=2)
                stick1_xpos = self.initial_masspoint_xpos[:2] + self.np_random.uniform(-self.obj_range, self.obj_range, size=2)
                stick2_xpos = self.initial_masspoint_xpos[:2] + self.np_random.uniform(-self.obj_range, self.obj_range, size=2)
        else:
            self.sample_hard = True
            stick1_xpos = np.array([1.3, self.pos_wall0[1] - self.size_wall[1] - self.size_obstacle[1]])
            stick2_xpos = np.array([1.3, self.pos_wall2[1] - self.size_wall[1] - self.size_obstacle[1]])
            object_xpos = self.initial_masspoint_xpos[:2] + self.np_random.uniform(-self.obj_range, self.obj_range, size=2)
            while object_xpos[1] > stick1_xpos[1] - self.size_obstacle[1] - self.size_object[1]:
                object_xpos = self.initial_masspoint_xpos[:2] + self.np_random.uniform(-self.obj_range, self.obj_range, size=2)
        # Set the position of box. (two slide joints)
        box_jointx_i = self.sim.model.get_joint_qpos_addr("object0:slidex")
        box_jointy_i = self.sim.model.get_joint_qpos_addr("object0:slidey")
        sim_state.qpos[box_jointx_i] = object_xpos[0]
        sim_state.qpos[box_jointy_i] = object_xpos[1]
        self.sim.set_state(sim_state)
        # Set the position of obstacle. (free joint)
        stick1_qpos = self.sim.data.get_joint_qpos('object1:joint')
        stick2_qpos = self.sim.data.get_joint_qpos('object2:joint')
        assert stick1_qpos.shape == (7,)
        assert stick2_qpos.shape == (7,)
        stick1_qpos[:2] = stick1_xpos
        stick2_qpos[:2] = stick2_xpos
        self.sim.data.set_joint_qpos('object1:joint', stick1_qpos)
        self.sim.data.set_joint_qpos('object2:joint', stick2_qpos)

        self.sim.forward()
        return True

    def compute_reward(self, observation, goal, info):
        # Note: the input is different from other environments.
        one_hot = goal[3:]
        idx = np.argmax(one_hot)
        # HACK: parse the corresponding object position from observation
        achieved_goal = observation[3 + 3 * idx : 3 + 3 * (idx + 1)]
        r = MasspointPushEnv.compute_reward(self, achieved_goal, goal[0:3], info)
        return r

    def step(self, action):
        action = np.clip(action, self.action_space.low, self.action_space.high)
        self._set_action(action)
        self.sim.step()
        self._step_callback()
        obs = self._get_obs()

        done = False
        info = {
            'is_success': self._is_success(obs['achieved_goal'][0:3], self.goal[0:3]),
        }
        reward = self.compute_reward(obs['observation'], self.goal, info)
        return obs, reward, done, info