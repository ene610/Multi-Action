import pfrl
import torch
import torch.nn
import gym
import numpy

# register the env with gym
# https://github.com/openai/gym/tree/master/gym/envs#how-to-create-new-environments-for-gym
from gym.envs.registration import register

from Multi_Action.DQN_AZUL.Env_mini_azul import CustomEnv

def main():

    id_str = "GraphWorld-v1"
    register(id = id_str,entry_point = CustomEnv,)

    env = gym.make(id_str)

    class QFunction(torch.nn.Module):

        def __init__(self, obs_size, n_actions):
            super().__init__()
            self.l1 = torch.nn.Linear(obs_size, 512)
            self.l2 = torch.nn.Linear(512, 1024)
            self.l3 = torch.nn.Linear(1024, 1024)
            self.l4 = torch.nn.Linear(1024, 512)
            self.l5 = torch.nn.Linear(512, n_actions)

        def forward(self, x):
            h = x
            h = torch.nn.functional.relu(self.l1(h))
            h = torch.nn.functional.relu(self.l2(h))
            h = torch.nn.functional.relu(self.l3(h))
            h = torch.nn.functional.relu(self.l4(h))
            h = self.l5(h)
            return pfrl.action_value.DiscreteActionValue(h)

    obs_size = env.observation_space.shape[0]
    n_actions = env.action_space.n
    q_func = QFunction(obs_size, n_actions)

    # Use Adam to optimize q_func. eps=1e-2 is for stability.
    optimizer = torch.optim.Adam(q_func.parameters(), eps=1e-2)

    # Set the discount factor that discounts future rewards.
    gamma = 0.9

    # Use epsilon-greedy for exploration
    explorer = pfrl.explorers.ConstantEpsilonGreedy(
        epsilon=0.3, random_action_func=env.action_space.sample)

    # DQN uses Experience Replay.
    # Specify a replay buffer and its capacity.
    replay_buffer = pfrl.replay_buffers.ReplayBuffer(capacity=10 ** 6)

    # Since observations from CartPole-v0 is numpy.float64 while
    # As PyTorch only accepts numpy.float32 by default, specify
    # a converter as a feature extractor function phi.

    # Set the device id to use GPU. To use CPU only, set it to -1.
    gpu = -1

    # Now create an agent that will interact with the environment.
    agent = pfrl.agents.DoubleDQN(
        q_func,
        optimizer,
        replay_buffer,
        gamma,
        explorer,
        replay_start_size = 500,
        update_interval = 1,
        target_update_interval = 100,
        gpu = gpu,
    )

    n_episodes = 300 * 1000
    max_episode_len = 1000

    for i in range(1, n_episodes + 1):
        obs = env.reset()

        R = 0  # return (sum of rewards)
        t = 0  # time step

        while True:
            # Uncomment to watch the behavior in a GUI window
            # env.render()
            action = agent.act(obs)
            obs, reward, done, _ = env.step(action)
            R += reward
            t += 1
            reset = t == max_episode_len
            agent.observe(obs, reward, done, reset)
            if done or reset:
                break
        if i % 10 == 0:
            print('episode:', i, 'R:', R)
        if i % 50 == 0:
            print('statistics:', agent.get_statistics())
    print('Finished.')

if __name__ == "__main__" :
    main()