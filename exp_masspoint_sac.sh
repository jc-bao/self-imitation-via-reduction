CUDA_VISIBLE_DEVICES=0 python run_her.py --env MasspointPushDoubleObstacle-v1 --random_ratio 0.7 --num_timesteps 1e7 --num_workers 32 --log_path logs/MasspointPushDoubleObstacle-v1_random0.7/her_sac_32workers/0
CUDA_VISIBLE_DEVICES=0 python run_her_augment.py --env MasspointPushDoubleObstacle-v1 --random_ratio 0.7 --num_timesteps 1e7 --num_workers 32 --start_augment 0 --imitation_coef 1 --log_path logs/MasspointPushDoubleObstacle-v1_random0.7/her_sac_aug_32workers/start0

