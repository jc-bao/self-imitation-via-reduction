CUDA_VISIBLE_DEVICES=0 python test_universal_sanity.py --env FetchPushWallObstacle-v4 --policy CustomSACPolicy --trained_model logs/FetchPushWallObstacle-v4_heavy_purerandom_fixz/final.zip --num_timesteps 1e7 --random_ratio 0.7 --log_path logs/FetchPushWallObstacle-v4_heavy_random0.7_fixz/her_sac_augment_sanity/0
CUDA_VISIBLE_DEVICES=2 python test_universal_sanity.py --env FetchPushWallObstacle-v4 --policy CustomSACPolicy --trained_model logs/FetchPushWallObstacle-v4_heavy_purerandom_fixz/final.zip --num_timesteps 1e7 --random_ratio 0.7 --goal_selection_strategy future_and_final --log_path logs/FetchPushWallObstacle-v4_heavy_random0.7_fixz/her_sac_augment_sanity/1
CUDA_VISIBLE_DEVICES=2 python test_universal_sanity.py --env FetchPushWallObstacle-v4 --policy CustomSACPolicy --trained_model logs/FetchPushWallObstacle-v4_heavy_purerandom_fixz/final.zip --num_timesteps 1e7 --random_ratio 0.7 --goal_selection_strategy future_and_final --n_sampled_goal 12 --buffer_size 3e6 --log_path logs/FetchPushWallObstacle-v4_heavy_random0.7_fixz/her_sac_augment_sanity/2

CUDA_VISIBLE_DEVICES=0 python test_universal_sanity.py --env FetchPushWallObstacle-v4 --policy CustomSACPolicy --trained_model logs/FetchPushWallObstacle-v4_heavy_purerandom_fixz/final.zip --num_timesteps 1e7 --random_ratio 0.3 --log_path logs/FetchPushWallObstacle-v4_heavy_random0.3_fixz/her_sac_augment_sanity/0
CUDA_VISIBLE_DEVICES=3 python test_universal_sanity.py --env FetchPushWallObstacle-v4 --policy CustomSACPolicy --trained_model logs/FetchPushWallObstacle-v4_heavy_purerandom_fixz/final.zip --num_timesteps 1e7 --random_ratio 0.3 --goal_selection_strategy future_and_final --log_path logs/FetchPushWallObstacle-v4_heavy_random0.3_fixz/her_sac_augment_sanity/1
CUDA_VISIBLE_DEVICES=3 python test_universal_sanity.py --env FetchPushWallObstacle-v4 --policy CustomSACPolicy --trained_model logs/FetchPushWallObstacle-v4_heavy_purerandom_fixz/final.zip --num_timesteps 1e7 --random_ratio 0.3 --goal_selection_strategy future_and_final --n_sampled_goal 12 --buffer_size 3e6 --log_path logs/FetchPushWallObstacle-v4_heavy_random0.3_fixz/her_sac_augment_sanity/2
