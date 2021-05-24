import gym
import sample_env

env = gym.make('sampleEnv-v0')

state = env.reset()
env.render()
done = False

i = 0

while i < 100:
    state, reward, done, info = env.step(env.action_space.sample())
    env.render()
    i+= 1

env.close()