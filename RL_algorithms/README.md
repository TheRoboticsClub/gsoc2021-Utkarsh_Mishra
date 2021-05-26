# RL Algorithms: Implementation and Baseline

It contains some Reinforcement Learning algorithm implementations with custom environments.
The RL algorithms are modular and can adapt to environments with vector based observations, pixel based observation or both simultaneously. 

## Sample Environment

This is a sample gym environment with both pixel based observations and state vector. The environment typically represents a robot with active
perception and state estimation. To install the environment

```
source ~/pyenvs/gsoc21/bin/activate
cd gsoc21code/RL_algorithms/
pip install -e sample-env
```

There are two environments:
- Env ID `sampleEnv-v0`: Sample environment with continuous action space (for DDPG and PPO) 
- Env ID `sampleEnv-v1`: Sample environment with discrete action space (for DQN and PPO) 

## Hyperparameters for the code

```
# For all the algorithms (default to DQN)
-h, --help                                      show this help message and exit
--env_id                  ENV_ID                Environment Id
--algorithm               ALGORITHM             Algorithm to run
--render                  RENDER                Render environment or not
--num_process             NUM_PROCESS           Number of process to run environment
--lr                      LR                    Learning rate for Policy Net
--gamma                   GAMMA                 Discount factor
--epsilon                 EPSILON               Probability controls greedy action
--explore_size            EXPLORE_SIZE          Explore steps before execute deterministic policy
--memory_size             MEMORY_SIZE           Size of replay memory
--step_per_iter           STEP_PER_ITER         Number of steps of interaction in each iteration
--batch_size              BATCH_SIZE            Batch size
--min_update_step         MIN_UPDATE_STEP       Minimum interacts for updating
--update_target_gap       UPDATE_TARGET_GAP     Steps between updating target q net
--max_iter                MAX_ITER              Maximum iterations to run
--eval_iter               EVAL_ITER             Iterations to evaluate the model
--save_iter               SAVE_ITER             Iterations to save the model
--model_path              MODEL_PATH            Directory to store model
--log_path                LOG_PATH              Directory to save logs
--seed                    SEED                  Seed for reproducing

# For DDPG specific algorithm

--lr_p                    LR_P                  Learning rate for Policy Net
--lr_v                    LR_V                  Learning rate for Value Net
--polyak                  POLYAK                Interpolation factor in polyak averaging for target networks
--update_step             UPDATE_STEP           Steps between updating policy and critic
--action_noise            ACTION_NOISE          Std for noise of action

# For PPO specific algorithm

--tau                     TAU                   GAE factor
--epsilon_ppo             EPSILON_PPO           Clip rate for PPO
--batch_size_ppo          BATCH_SIZE_PPO        Batch size for PPO
--ppo_mini_batch_size     PPO_MINI_BATCH_SIZE   PPO mini-batch size (default 0 -> don't use mini-batch update)
--ppo_epochs              PPO_EPOCHS            PPO step
```

## Running the Code

```
source ~/pyenvs/gsoc21/bin/activate
cd gsoc21code/RL_algorithms/

# For DQN

python main.py --env_id sampleEnv-v1 \
            --algorithm DQN \
            --num_process 1  \
            --lr 3e-3 \
            --gamma 0.99 \ 
            --epsilon 0.90 \
            --explore_size 5000 \ 
            --memory_size 100000 \
            --step_per_iter 1000 \
            --batch_size 256 \
            --min_update_step 1000 \ 
            --update_target_gap 50 \
            --max_iter 1000 \
            --eval_iter 50 \
            --save_iter 50 \
            --model_path trained_models \
            --log_path log/  \
            --seed 1234

# For DDPG

python main.py --env_id sampleEnv-v0 \
            --algorithm DDPG \
            --num_process 1 \
            --lr_p 3e-3 \
            --lr_v 3e-3 \
            --gamma 0.99 \
            --polyak 0.995 \
            --explore_size 5000 \
            --memory_size 100000 \
            --step_per_iter 1000 \
            --batch_size 256 \
            --min_update_step 1000 \ 
            --update_step 50 \
            --max_iter 1000 \
            --eval_iter 50 \
            --save_iter 50 \
            --action_noise 0.1 \ 
            --model_path trained_models  \
            --log_path log/  \
            --seed 1234 \

# For PPO

python main.py --env_id sampleEnv-v0 \
            --algorithm PPO \
            --num_process 4  \
            --lr_p 3e-3 \
            --lr_v 3e-3 \
            --gamma 0.99 \
            --tau 0.95 \
            --epsilon_ppo 0.2 \
            --batch_size_ppo 4000 \
            --ppo_mini_batch_size 256   \
            --ppo_epochs 10 \
            --max_iter 1000 \
            --eval_iter 50 \
            --save_iter 50 \
            --model_path trained_models \
            --log_path log/  \
            --seed 1234
```

The results are saved in the `./experiments/` directory. Tensorboard can be launched with `./experiments/log` directory.