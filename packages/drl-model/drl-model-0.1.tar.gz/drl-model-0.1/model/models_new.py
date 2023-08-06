# common library
import pandas as pd
import numpy as np
import time
import gym
import tensorflow as tf

# RL models from stable-baselines
from stable_baselines import SAC
from stable_baselines import PPO2
from stable_baselines import A2C
from stable_baselines import DDPG
from stable_baselines import TD3
from stable_baselines.ddpg.policies import DDPGPolicy
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise, AdaptiveParamNoiseSpec
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.vec_env import SubprocVecEnv
from preprocessing.preprocessors import *
from config import config

# customized env
from env.EnvMultipleStock_train import StockEnvTrain
from env.EnvMultipleStock_validation import StockEnvValidation
from env.EnvMultipleStock_trade import StockEnvTrade


def train_A2C(env_train, model_name, timesteps=50000):
    """A2C model"""

    start = time.time()
    model = A2C('MlpPolicy', env_train, verbose=0)
    model.learn(total_timesteps=timesteps)
    end = time.time()

    model.save(f"{config.TRAINED_MODEL_DIR}/{model_name}")
    print('Training time (A2C): ', (end - start) / 60, ' minutes')
    return model


def train_DDPG(env_train, model_name, batch_size=128, timesteps=50000, n_env=1, n_steps=1, n_batch=1):
    """DDPG model"""

    start = time.time()
    #model = DDPG('MlpPolicy', env_train)
    policy_kwargs = dict(n_env=n_env, n_steps=n_steps, n_batch=n_batch)
    model = TD3('MlpPolicy', env_train, batch_size=batch_size, policy_kwargs=policy_kwargs)
    model.learn(total_timesteps=timesteps, log_interval=10)
    end = time.time()

    model.save(f"{config.TRAINED_MODEL_DIR}/{model_name}")
    print('Training time (DDPG): ', (end - start) / 60, ' minutes')
    return model


def train_PPO(env_train, model_name, timesteps=50000):
    """PPO model"""

    start = time.time()
    model = PPO2('MlpPolicy', env_train)
    model.learn(total_timesteps=timesteps)
    end = time.time()

    model.save(f"{config.TRAINED_MODEL_DIR}/{model_name}")
    print('Training time (PPO): ', (end - start) / 60, ' minutes')
    return model


def DRL_prediction(df,
                   model,
                   name,
                   last_state,
                   iter_num,
                   unique_trade_date,
                   rebalance_window,
                   turbulence_threshold,
                   initial):
    ### make a prediction based on trained model### 

    ## trading env
    trade_data = data_split(df, start=unique_trade_date[iter_num - rebalance_window], end=unique_trade_date[iter_num])
    env_trade = DummyVecEnv([lambda: StockEnvTrade(trade_data,
                                                   turbulence_threshold=turbulence_threshold,
                                                   initial=initial,
                                                   previous_state=last_state,
                                                   model_name=name,
                                                   iteration=iter_num)])
    obs_trade = env_trade.reset()
    
    ans = 0

    for i in range(len(trade_data.index.unique())):
        action, _states = model.predict(obs_trade)
        obs_trade, rewards, dones, info = env_trade.step(action)
        ans = ans + rewards
        if i == (len(trade_data.index.unique()) - 2):
            # print(env_test.render())
            last_state = env_trade.render()
            ans = ans - rewards
            #print(last_state.shape)

    df_last_state = pd.DataFrame({'last_state': last_state})
    df_last_state.to_csv('results/last_state_{}_{}.csv'.format(name, i), index=False)
    return last_state, ans


def DRL_prediction_DDPG(df,
                   model,
                   name,
                   last_state,
                   iter_num,
                   unique_trade_date,
                   rebalance_window,
                   turbulence_threshold,
                   initial,
                   n_batch):
    ### make a prediction based on trained model### 

    ## trading env
    trade_data = data_split(df, start=unique_trade_date[iter_num - rebalance_window], end=unique_trade_date[iter_num])
    env_l = [lambda: StockEnvTrade(trade_data, turbulence_threshold=turbulence_threshold,
                                                   initial=initial,
                                                   previous_state=last_state,
                                                   model_name=name,
                                                   iteration=iter_num)]
    env_list = []
    for ind in range(n_batch):
        env_list.extend(env_l)
    env_trade = DummyVecEnv(env_list)
    
    obs_trade = env_trade.reset()
    
    ans = 0

    for i in range(len(trade_data.index.unique())):
        action, _states = model.predict(obs_trade)
        obs_trade, rewards, dones, info = env_trade.step(action)
        ans = ans + rewards
        if i == (len(trade_data.index.unique()) - 2):
#             print(obs_trade)
#             print("123")
#             last_state = obs_trade[0,:].tolist()
#             print(last_state)
            ans = ans - rewards
            #last_state = env_trade.render()

    df_last_state = pd.DataFrame({'last_state': last_state})
    df_last_state.to_csv('results/last_state_{}_{}.csv'.format(name, i), index=False)
    return last_state, ans


def DRL_validation(model, test_data, test_env, test_obs) -> None:
    ###validation process###
    for i in range(len(test_data.index.unique())):
        action, _states = model.predict(test_obs)
        test_obs, rewards, dones, info = test_env.step(action)


def get_validation_sharpe(iteration):
    ###Calculate Sharpe ratio based on validation results###
    df_total_value = pd.read_csv('results/account_value_validation_{}.csv'.format(iteration), index_col=0)
    df_total_value.columns = ['account_value_train']
    df_total_value['daily_return'] = df_total_value.pct_change(1)
    sharpe = (4 ** 0.5) * df_total_value['daily_return'].mean() / \
             df_total_value['daily_return'].std()
    return sharpe


def run_ensemble_strategy(df, unique_trade_date, rebalance_window, validation_window, timesteps, batch_size, n_env, n_steps) -> None:
    """Ensemble Strategy that combines PPO, A2C and DDPG"""
    print("============Start Ensemble Strategy============")
    # for ensemble model, it's necessary to feed the last state
    # of the previous model to the current model as the initial state
    last_state_ensemble = []

    ppo_sharpe_list = []
    ddpg_sharpe_list = []
    a2c_sharpe_list = []

    model_use = []

    # based on the analysis of the in-sample data
    #turbulence_threshold = 140
    insample_turbulence = df[(df.datadate<20151000) & (df.datadate>=20090000)]
    insample_turbulence = insample_turbulence.drop_duplicates(subset=['datadate'])
    insample_turbulence_threshold = np.quantile(insample_turbulence.turbulence.values, .90)

    start = time.time()
    for i in range(rebalance_window + validation_window, len(unique_trade_date), rebalance_window):
        print("============================================")
        ## initial state is empty
        if i - rebalance_window - validation_window == 0:
            # inital state
            initial = True
        else:
            # previous state
            initial = False

        # Tuning trubulence index based on historical data
        # Turbulence lookback window is one quarter
        historical_turbulence = df[(df.datadate<unique_trade_date[i - rebalance_window - validation_window]) & (df.datadate>=(unique_trade_date[i - rebalance_window - validation_window-63]))]
        historical_turbulence = historical_turbulence.drop_duplicates(subset=['datadate'])
        historical_turbulence_mean = np.mean(historical_turbulence.turbulence.values)   

        if historical_turbulence_mean > insample_turbulence_threshold:
            # if the mean of the historical data is greater than the 90% quantile of insample turbulence data
            # then we assume that the current market is volatile, 
            # therefore we set the 90% quantile of insample turbulence data as the turbulence threshold 
            # meaning the current turbulence can't exceed the 90% quantile of insample turbulence data
            turbulence_threshold = insample_turbulence_threshold
        else:
            # if the mean of the historical data is less than the 90% quantile of insample turbulence data
            # then we tune up the turbulence_threshold, meaning we lower the risk 
            turbulence_threshold = np.quantile(insample_turbulence.turbulence.values, 0.99)
        print("turbulence_threshold: ", turbulence_threshold)

        ############## Environment Setup starts ##############
        ## training env
        train = data_split(df, start=20090000, end=unique_trade_date[i - rebalance_window - validation_window])
        env_train = DummyVecEnv([lambda: StockEnvTrain(train)])
        env_t = [lambda: StockEnvTrain(train)]
        env_t_list = []
        n_batch = n_env * n_steps
        for index_list in range(n_batch):
            env_t_list.extend(env_t)
        env_train_ddpg = DummyVecEnv(env_t_list)

        ## validation env
        validation = data_split(df, start=unique_trade_date[i - rebalance_window - validation_window],
                                end=unique_trade_date[i - rebalance_window])
        env_val = DummyVecEnv([lambda: StockEnvValidation(validation,
                                                          turbulence_threshold=turbulence_threshold,
                                                          iteration=i)])
        obs_val = env_val.reset()
        env_list = [lambda: StockEnvValidation(validation, turbulence_threshold=turbulence_threshold, iteration=i)]
        env_val_list = []
        n_batch = n_env * n_steps
        for index_list in range(n_batch):
            env_val_list.extend(env_list)
        env_val_ddpg = DummyVecEnv(env_val_list)
        obs_val_ddpg = env_val_ddpg.reset()
        ############## Environment Setup ends ##############

        ############## Training and Validation starts ##############
        print("======Model training from: ", 20090000, "to ",
              unique_trade_date[i - rebalance_window - validation_window])
        # print("training: ",len(data_split(df, start=20090000, end=test.datadate.unique()[i-rebalance_window]) ))
        # print("==============Model Training===========")
        print("======A2C Training========")
        model_a2c = train_A2C(env_train, model_name="A2C_10k_dow_{}".format(i), timesteps=10)
        print("======A2C Validation from: ", unique_trade_date[i - rebalance_window - validation_window], "to ",
              unique_trade_date[i - rebalance_window])
        DRL_validation(model=model_a2c, test_data=validation, test_env=env_val, test_obs=obs_val)
        sharpe_a2c = get_validation_sharpe(i)
        print("A2C Sharpe Ratio: ", sharpe_a2c)

        print("======PPO Training========")
        model_ppo = train_PPO(env_train, model_name="PPO_100k_dow_{}".format(i), timesteps=5)
        print("======PPO Validation from: ", unique_trade_date[i - rebalance_window - validation_window], "to ",
              unique_trade_date[i - rebalance_window])
        DRL_validation(model=model_ppo, test_data=validation, test_env=env_val, test_obs=obs_val)
        sharpe_ppo = get_validation_sharpe(i)
        print("PPO Sharpe Ratio: ", sharpe_ppo)

        print("======DDPG Training========")
        model_ddpg = train_DDPG(env_train_ddpg, model_name="DDPG_10k_dow_{}".format(i), batch_size=batch_size, timesteps=timesteps, n_env=n_env, n_steps=n_steps, n_batch=n_batch)
        print("======DDPG Validation from: ", unique_trade_date[i - rebalance_window - validation_window], "to ",
              unique_trade_date[i - rebalance_window])
        DRL_validation(model=model_ddpg, test_data=validation, test_env=env_val_ddpg, test_obs=obs_val_ddpg)
        sharpe_ddpg = get_validation_sharpe(i)
        print("DDPG Sharpe Ratio: ", sharpe_ddpg)

        ppo_sharpe_list.append(sharpe_ppo)
        a2c_sharpe_list.append(sharpe_a2c)
        ddpg_sharpe_list.append(sharpe_ddpg)
        
        flag_trade = 0

        # Model Selection based on sharpe ratio
        if (sharpe_ppo >= sharpe_a2c) & (sharpe_ppo >= sharpe_ddpg):
            model_ensemble = model_ppo
            model_use.append('PPO')
        elif (sharpe_a2c > sharpe_ppo) & (sharpe_a2c > sharpe_ddpg):
            model_ensemble = model_a2c
            model_use.append('A2C')
        else:
            flag_trade = 1
            model_ensemble = model_ddpg
            model_use.append('DDPG')
        ############## Training and Validation ends ##############    

        ############## Trading starts ############## 
        
        print("======Trading from: ", unique_trade_date[i - rebalance_window], "to ", unique_trade_date[i])
        print("Used Model: ", model_ensemble)
#         model_ensemble = model_ddpg
#         flag_trade = 1
        if(flag_trade):
            last_state_ensemble,rew = DRL_prediction_DDPG(df=df, model=model_ensemble, name="ensemble",
                                             last_state=last_state_ensemble, iter_num=i,
                                             unique_trade_date=unique_trade_date,
                                             rebalance_window=rebalance_window,
                                             turbulence_threshold=turbulence_threshold,
                                             initial=initial, 
                                             n_batch=n_batch)
        else:
            last_state_ensemble,rew = DRL_prediction(df=df, model=model_ensemble, name="ensemble",
                                             last_state=last_state_ensemble, iter_num=i,
                                             unique_trade_date=unique_trade_date,
                                             rebalance_window=rebalance_window,
                                             turbulence_threshold=turbulence_threshold,
                                             initial=initial)
        # print("============Trading Done============")
        ############## Trading ends ##############    
    #print(last_state_ensemble)

    #reward_last = last_state_ensemble[0] - 1000000
    #print(reward_last)
    print(rew[0])
    end = time.time()
    print("Ensemble Strategy took: ", (end - start) / 60, " minutes")