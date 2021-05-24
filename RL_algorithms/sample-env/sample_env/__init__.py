from gym.envs.registration import register

register(
    id='sampleEnv-v0',
    entry_point='sample_env.envs:SampleEnv',
)

register(
    id='sampleEnv-v1',
    entry_point='sample_env.envs:SampleEnvDiscrete',
)