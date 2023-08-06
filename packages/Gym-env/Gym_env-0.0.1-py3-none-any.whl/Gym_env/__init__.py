from gym.envs.registration import register

register(
    id='Gym_env-v0',
    entry_point='Gym_env.envs:GymEnv',
)