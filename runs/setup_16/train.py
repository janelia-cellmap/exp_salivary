# %%
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

labels = config["run"]["labels"]
yaml_file = config["paths"]["yaml_file"]
log_dir = config["paths"]["log_dir"]
voxel_size = tuple([config["run"]["voxel_size"] for _ in range(3)])
l_rate = config["run"].get("l_rate", 0.5e-5)
batch_size = config["run"].get("batch_size", 14)
starter_checkpoint = config["checkpoint"]["path"]
checkpoint_classes = config["checkpoint"].get("classes", None)
is_lsd = config["run"].get("lsd", False)



import warnings

# Suppress only UserWarning and FutureWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import yaml
import torch
import numpy as np
import logging
from fly_organelles.run import run
from fly_organelles.model import StandardUnet

from fly_organelles.run import set_weights
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

logger = logging.getLogger(__name__)


iterations = 1000000


affinities_map = [
                        [1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1],
    ]


with open(yaml_file, "r") as data_yaml:
    datasets = yaml.safe_load(data_yaml)
# label_stores, raw_stores, crop_copies = read_data_yaml(data_yaml)
total_labels = len(labels)
if is_lsd:
    total_labels = total_labels * 13
model = StandardUnet(total_labels)
# %%
import glob
import os

checkpoint_files = glob.glob(
    os.path.join(os.path.dirname(__file__), "model_checkpoint_*")
)
if checkpoint_files:

    def extract_step(fp):
        try:
            return int(os.path.basename(fp).split("_")[-1])
        except Exception:
            return -1

    latest_ckpt = max(checkpoint_files, key=extract_step)
    checkpoint = torch.load(latest_ckpt, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)
else:
    checkpoint = torch.load(starter_checkpoint, weights_only=True, map_location=device)
    if checkpoint_classes is None:
        model.load_state_dict(checkpoint["model_state_dict"], strict=True)
    else:
        updated_checkpoint = set_weights(
            model, checkpoint["model_state_dict"], checkpoint_classes, labels
        )
        model.load_state_dict(updated_checkpoint, strict=True)

model = model.to(device)


run(
    model,
    iterations,
    labels,
    None,
    datasets,
    voxel_size=voxel_size,
    batch_size=batch_size,
    l_rate=l_rate,
    log_dir=log_dir,
    affinities = True, 
    affinities_map = affinities_map,
)
