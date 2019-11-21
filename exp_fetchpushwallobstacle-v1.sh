# Training.
trap '' 15
CUDA_VISIBLE_DEVICES=0 python test_her.py --env FetchPushWallObstacle-v1 --log_path logs/FetchPushWallObstacle-v1_heavy_purerandom/her_sac/ --num_timesteps 1e7 --heavy_obstacle --random_gripper
CUDA_VISIBLE_DEVICES=0 python test_her.py --env FetchPushWallObstacle-v1 --log_path logs/FetchPushWallObstacle-v1_heavy_purerandom_largebatch/her_sac/ --num_timesteps 1e7 --batch_size 128 --heavy_obstacle --random_gripper
CUDA_VISIBLE_DEVICES=0 python test_her.py --env FetchPushWallObstacle-v1 --log_path logs/FetchPushWallObstacle-v1_heavy_purerandom_hidev/her_sac/ --num_timesteps 1e7 --heavy_obstacle --random_gripper --hide_velocity
CUDA_VISIBLE_DEVICES=0 python test_ensemble.py --env FetchPushWallObstacle-v1 --log_path logs/FetchPushWallObstacle-v1_heavy_purerandom/her_sac_ensemble/ --num_timesteps 1e7 --heavy_obstacle --random_gripper

CUDA_VISIBLE_DEVICES=0 python test_ensemble.py --env FetchPushWallObstacle-v1 --log_path logs/FetchPushWallObstacle-v1_heavy_purerandom/her_sac_ensemble2/ --num_timesteps 1e7 --batch_size 128 --buffer_size 2e6 --heavy_obstacle --random_gripper

CUDA_VISIBLE_DEVICES=0 python test_ensemble.py --env FetchPushWallObstacle-v1 --load_path logs/FetchPushWallObstacle-v1_heavy_purerandom/her_sac_ensemble/model_0.zip --play --heavy_obstacle --random_gripper

# CUDA_VISIBLE_DEVICES=0 python test_her.py --env FetchPushWallObstacle-v1 --log_path logs/FetchPushWallObstacle-v1_heavy_random/her_sac --num_timesteps 6e6 --heavy_obstacle

# Visualize trained agent.
# CUDA_VISIBLE_DEVICES=0 python test_her.py --env FetchPushObstacle-v1 --play --load_path ./logs/FetchPushObstacle-v1/her/final

# Plot learning curve.
# python plot_log.py --env FetchPushObstacle-v1 --log_path ./logs/FetchPushObstacle-v1/her --xaxis timesteps