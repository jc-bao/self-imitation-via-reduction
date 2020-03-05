CUDA_VISIBLE_DEVICES=0 python run_her.py --env FetchStack-v0 --num_timesteps 1e7 --reward_type sparse --n_object 2 --log_path logs/FetchStack-v0/her_sac/0
CUDA_VISIBLE_DEVICES=0 python run_her.py --env FetchStack-v1 --num_timesteps 1e7 --random_ratio 0.5 --reward_type sparse --n_object 2 --log_path logs/FetchStack-v1_0.5fix/her_sac/0
CUDA_VISIBLE_DEVICES=0 python run_her.py --env FetchStack-v1 --num_timesteps 1e7 --random_ratio 0.5 --num_workers 32 --policy AttentionPolicy --reward_type sparse --n_object 2 --log_path logs/FetchStack-v1/her_sac_32workers/attention_0
CUDA_VISIBLE_DEVICES=0 python run_her.py --env FetchStack-v1 --num_timesteps 1e7 --random_ratio 0.5 --num_workers 1 --policy AttentionPolicy --reward_type sparse --n_object 2 --log_path logs/FetchStack-v1_0.5fix/her_sac_1workers/attention_0
CUDA_VISIBLE_DEVICES=1 python run_her.py --env FetchStack-v1 --num_timesteps 1e7 --random_ratio 0.7 --num_workers 1 --policy AttentionPolicy --reward_type sparse --n_object 2 --log_path logs/FetchStack-v1_0.7fix/her_sac_1workers/attentionln_3_ent0.01_explr0.1
CUDA_VISIBLE_DEVICES=0 python run_her.py --env FetchReach-v1 --num_timesteps 1e5 --num_workers 16 --policy CustomSACPolicy
