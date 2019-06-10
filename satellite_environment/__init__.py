from gym.envs.registration import register

register(
    id='2D-Sat-v0',
    entry_point='satellite_environment.envs:SatEnv',
)

