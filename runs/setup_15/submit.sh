bsub -J setup_15_lsd -P cellmap -n 12 -q gpu_h200 -gpu "num=1" -o output.log -e error.log python train.py
