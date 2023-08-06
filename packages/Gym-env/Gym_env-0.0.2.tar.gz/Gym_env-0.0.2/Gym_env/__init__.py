from gym.envs.registration import register

register(
    id='Gym_env-v1',
    entry_point='Gym_env.envs:GymEnv',
)