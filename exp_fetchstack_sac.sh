CUDA_VISIBLE_DEVICES=0 python run_her.py --env FetchStack-v0 --num_timesteps 1e7 --reward_type sparse --n_object 2 --log_path logs/FetchStack-v0/her_sac/0
CUDA_VISIBLE_DEVICES=0 python run_her.py --env FetchStack-v1 --num_timesteps 1e7 --random_ratio 0.5 --reward_type sparse --n_object 2 --log_path logs/FetchStack-v1_0.5fix/her_sac/0
