# Training.
CUDA_VISIBLE_DEVICES=0 mpirun -n 8 python test_her.py --env FetchPush-v1

# Visualize trained agent.
# CUDA_VISIBLE_DEVICES=0 python test_her.py --env FetchPush-v1 --play

# Plot learning curve.
# python plot_log.py --env FetchPush-v1 
