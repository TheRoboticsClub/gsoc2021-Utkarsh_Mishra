#!/usr/bin/env python

import argparse
import torch
from torch.utils.tensorboard import SummaryWriter

from DQN.dqn import DQN
from DDPG.ddpg import DDPG
from PPO.ppo import PPO

import sample_env


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--env_id", type=str, default="sampleEnv-v0", help="Environment Id")
    parser.add_argument("--algorithm", type=str, default="DQN", help="Algorithm to run")
    parser.add_argument("--render", type=bool, default=False, help="Render environment or not")
    parser.add_argument("--num_process", type=int, default=1, help="Number of process to run environment")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate for Policy Net")
    parser.add_argument("--gamma", type=float, default=0.99, help="Discount factor")
    parser.add_argument("--epsilon", type=float, default=0.90, help="Probability controls greedy action")
    parser.add_argument("--explore_size", type=int, default=1000, help="Explore steps before execute deterministic policy")
    parser.add_argument("--memory_size", type=int, default=1000000, help="Size of replay memory")
    parser.add_argument("--step_per_iter", type=int, default=1000, help="Number of steps of interaction in each iteration")
    parser.add_argument("--batch_size", type=int, default=256, help="Batch size")
    parser.add_argument("--min_update_step", type=int, default=1000, help="Minimum interacts for updating")
    parser.add_argument("--update_target_gap", type=int, default=50, help="Steps between updating target q net")
    parser.add_argument("--max_iter", type=int, default=500, help="Maximum iterations to run")
    parser.add_argument("--eval_iter", type=int, default=1, help="Iterations to evaluate the model")
    parser.add_argument("--save_iter", type=int, default=1, help="Iterations to save the model")
    parser.add_argument("--model_path", type=str, default="trained_models", help="Directory to store model")
    parser.add_argument("--log_path", type=str, default="log/", help="Directory to save logs")
    parser.add_argument("--seed", type=int, default=123, help="Seed for reproducing")

    ## For DDPG
    parser.add_argument("--lr_p", type=float, default=1e-3, help="Learning rate for Policy Net")
    parser.add_argument("--lr_v", type=float, default=1e-3, help="Learning rate for Value Net")
    parser.add_argument("--polyak", type=float, default=0.995, help="Interpolation factor in polyak averaging for target networks")
    parser.add_argument("--update_step", type=int, default=50, help="Steps between updating policy and critic")
    parser.add_argument("--action_noise", type=float, default=0.1, help="Std for noise of action")

    ## For PPO
    parser.add_argument("--tau", type=float, default=0.95, help="GAE factor")
    parser.add_argument("--epsilon_ppo", type=float, default=0.2, help="Clip rate for PPO")
    parser.add_argument("--batch_size_ppo", type=int, default=4000, help="Batch size")
    parser.add_argument("--ppo_mini_batch_size", type=int, default=500,
                  help="PPO mini-batch size (default 0 -> don't use mini-batch update)")
    parser.add_argument("--ppo_epochs", type=int, default=10, help="PPO step")

    args = parser.parse_args()
    return args

def runDQN(env_id, render, num_process, lr, gamma, epsilon, explore_size, memory_size, step_per_iter, batch_size,
         min_update_step, update_target_gap, max_iter, eval_iter, save_iter, model_path, log_path, seed):
    base_dir = './experiments/' + log_path + env_id + "/DQN_exp{}".format(seed)
    writer = SummaryWriter(base_dir)
    dqn = DQN(env_id,
              render=render,
              num_process=num_process,
              memory_size=memory_size,
              lr_q=lr,
              gamma=gamma,
              epsilon=epsilon,
              explore_size=explore_size,
              step_per_iter=step_per_iter,
              batch_size=batch_size,
              min_update_step=min_update_step,
              update_target_gap=update_target_gap,
              seed=seed)

    for i_iter in range(1, max_iter + 1):
        dqn.learn(writer, i_iter)

        if i_iter % eval_iter == 0:
            dqn.eval(i_iter, render=render)

        if i_iter % save_iter == 0:
            dqn.save('./experiments/' + model_path)

        torch.cuda.empty_cache()

def runDDPG(env_id, render, num_process, lr_p, lr_v, gamma, polyak, explore_size, memory_size, step_per_iter, batch_size,
         min_update_step, update_step, max_iter, eval_iter, save_iter, action_noise, model_path, log_path, seed):
    base_dir = './experiments/' + log_path + env_id + "/DDPG_exp{}".format(seed)
    writer = SummaryWriter(base_dir)

    ddpg = DDPG(env_id,
                render=render,
                num_process=num_process,
                memory_size=memory_size,
                lr_p=lr_p,
                lr_v=lr_v,
                gamma=gamma,
                polyak=polyak,
                explore_size=explore_size,
                step_per_iter=step_per_iter,
                batch_size=batch_size,
                min_update_step=min_update_step,
                update_step=update_step,
                action_noise=action_noise,
                seed=seed)

    for i_iter in range(1, max_iter + 1):
        ddpg.learn(writer, i_iter)

        if i_iter % eval_iter == 0:
            ddpg.eval(i_iter, render=render)

        if i_iter % save_iter == 0:
            ddpg.save('./experiments/' + model_path)

        torch.cuda.empty_cache()

def runPPO(env_id, render, num_process, lr_p, lr_v, gamma, tau, epsilon, batch_size,
         ppo_mini_batch_size, ppo_epochs, max_iter, eval_iter, save_iter, model_path, log_path, seed):
    base_dir = './experiments/' + log_path + env_id + "/PPO_exp{}".format(seed)
    writer = SummaryWriter(base_dir)

    ppo = PPO(env_id=env_id,
              render=render,
              num_process=num_process,
              min_batch_size=batch_size,
              lr_p=lr_p,
              lr_v=lr_v,
              gamma=gamma,
              tau=tau,
              clip_epsilon=epsilon,
              ppo_epochs=ppo_epochs,
              ppo_mini_batch_size=ppo_mini_batch_size,
              seed=seed)

    for i_iter in range(1, max_iter + 1):
        ppo.learn(writer, i_iter)

        if i_iter % eval_iter == 0:
            ppo.eval(i_iter, render=render)

        if i_iter % save_iter == 0:
            ppo.save('./experiments/' + model_path)

            pickle.dump(ppo,
                        open('{}/{}_ppo.p'.format('./experiments/' + model_path, env_id), 'wb'))

        torch.cuda.empty_cache()


if __name__ == '__main__':
    args = parse_args()

    if args.algorithm == 'DQN':

      runDQN(args.env_id, 
            args.render, 
            args.num_process, 
            args.lr, 
            args.gamma, 
            args.epsilon, 
            args.explore_size, 
            args.memory_size, 
            args.step_per_iter, 
            args.batch_size,
            args.min_update_step, 
            args.update_target_gap, 
            args.max_iter, 
            args.eval_iter, 
            args.save_iter, 
            args.model_path, 
            args.log_path, 
            args.seed)

    elif args.algorithm == 'DDPG':

      runDDPG(args.env_id, 
            args.render, 
            args.num_process, 
            args.lr_p, 
            args.lr_v, 
            args.gamma, 
            args.polyak, 
            args.explore_size, 
            args.memory_size, 
            args.step_per_iter, 
            args.batch_size, 
            args.min_update_step, 
            args.update_step, 
            args.max_iter, 
            args.eval_iter, 
            args.save_iter, 
            args.action_noise, 
            args.model_path, 
            args.log_path, 
            args.seed)

    elif args.algorithm == 'PPO':

      runPPO(args.env_id, 
            args.render, 
            args.num_process, 
            args.lr_p, 
            args.lr_v, 
            args.gamma, 
            args.tau, 
            args.epsilon_ppo, 
            args.batch_size_ppo, 
            args.ppo_mini_batch_size, 
            args.ppo_epochs, 
            args.max_iter, 
            args.eval_iter, 
            args.save_iter, 
            args.model_path, 
            args.log_path, 
            args.seed)

    else:
      assert False, "Please enter a valid algorithm. Currently supported: DQN. DDPG, PPO" 
