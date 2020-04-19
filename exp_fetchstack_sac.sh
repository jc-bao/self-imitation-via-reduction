CUDA_VISIBLE_DEVICES=1 python run_her.py --env FetchStack-v1 --num_timesteps 1e7 --curriculum --num_workers 32 --policy AttentionPolicy --reward_type sparse --n_object 3 --log_path logs/FetchStack-v1_adapt/her_sac_32workers/attention_critic_3obj
CUDA_VISIBLE_DEVICES=0 python run_her_augment.py --env FetchStack-v1 --num_timesteps 2.5e6 --curriculum --num_workers 32 --policy AttentionPolicy --reward_type sparse --n_object 2 --start_augment 1.2e7 --imitation_coef 1 --log_path logs/FetchStack-v1_adapt/her_sac_aug_32workers/attention_critic_2obj_imitation1
CUDA_VISIBLE_DEVICES=0 python run_her_augment.py --env FetchStack-v1 --num_timesteps 1e7 --curriculum --num_workers 32 --policy AttentionPolicy --reward_type sparse --n_object 3 --start_augment 1.5e7 --imitation_coef 1 --log_path logs/FetchStack-v1_adapt/her_sac_aug_32workers/attention_critic_3obj_imitation1
CUDA_VISIBLE_DEVICES=1 python run_her.py --env FetchStack-v1 --num_timesteps 1e7 --curriculum --sequential --num_workers 32 --policy AttentionPolicy --reward_type sparse --n_object 6 --log_path logs/FetchStack-v1_adapt/her_sac_32workers/attention_critic_6obj_seq
CUDA_VISIBLE_DEVICES=0 python run_her_augment.py --env FetchStack-v1 --num_timesteps 1e7 --curriculum --sequential --num_workers 32 --policy AttentionPolicy --reward_type sparse --n_object 6 --start_augment 2.5e7 --imitation_coef 1 --log_path logs/FetchStack-v1_adapt/her_sac_aug_32workers/attention_critic_6obj_seq_imitation1
# SIL
CUDA_VISIBLE_DEVICES=1 python run_her.py --env FetchStack-v1 --num_timesteps 1e7 --curriculum --num_workers 32 --policy AttentionPolicy --reward_type sparse --n_object 2 --sil --sil_coef 0.1 --log_path logs/FetchStack-v1_adapt/her_sac_sil_32workers/attention_critic_2obj_0.1
CUDA_VISIBLE_DEVICES=0 python run_her.py --env FetchReach-v1 --num_timesteps 1e5 --num_workers 16 --policy CustomSACPolicy
CUDA_VISIBLE_DEVICES=2 python run_her.py --env FetchPush-v1 --num_timesteps 1e7 --num_workers 16 --policy CustomSACPolicy --log_path logs/FetchPush-v1/her_sac_16workers/no_priority
CUDA_VISIBLE_DEVICES=2 python run_her.py --env FetchPush-v1 --num_timesteps 1e7 --num_workers 16 --policy CustomSACPolicy --priority --log_path logs/FetchPush-v1/her_sac_16workers/priority
CUDA_VISIBLE_DEVICES=2 python run_her_baseline.py --env FetchPush-v1 --num_timesteps 1e7 --log_path logs/FetchPush-v1/her_sac_baseline/0

# stack-v2
CUDA_VISIBLE_DEVICES=1 python run_her.py --env FetchStack-v2 --num_timesteps 1e7 --curriculum --num_workers 32 --policy AttentionPolicy --reward_type sparse --n_object 3 --log_path logs/FetchStack-v2_adapt/her_sac_32workers/attention_critic_3obj
CUDA_VISIBLE_DEVICES=0 python run_her_augment.py --env FetchStack-v2 --num_timesteps 1e7 --curriculum --num_workers 32 --policy AttentionPolicy --reward_type sparse --n_object 3 --imitation_coef 1 --log_path logs/FetchStack-v2_adapt/her_sac_aug_32workers/attention_critic_3obj_imitation1

