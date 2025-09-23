# %%
yaml_file = "/groups/cellmap/cellmap/zouinkhim/exp_salivary/runs/setup_16/20250914_all_mitos.yaml"
import itertools
import yaml
import os
with open(yaml_file, "r") as data_yaml:
    datasets = yaml.safe_load(data_yaml)
#%%
crops_all = list(itertools.chain.from_iterable(v["crops"].values() for _,v in datasets["datasets"].items()))
print(crops_all)
len(crops_all)
# %%

#%%
from statistics import mode
import fibsem_tools as fst
sampling = [16,16,16]
min_size = 50
errors = []
for raw_store in crops_all:
    try:
        raw_grp = fst.read(os.path.join(raw_store,"mito"))
        raw_scale, raw_offset, raw_shape = find_target_scale(raw_grp, sampling)
        # print(raw_shape)
        size = mode(raw_shape)
        # if size < min_size:
        #     print(f"Warning: {raw_store} has one dimension smaller than {min_size}, size: {raw_shape}")
        # print(raw_scale, raw_offset, raw_shape)
        # break
    except Exception as e:
        # raise Exception(f"Error processing {raw_store}: {e}")
        # print(f"Error processing {raw_store}: {e}")
        rr = raw_store.split("groundtruth/")[-1]
        print(f"Error processing {rr}")
        errors.append(raw_store)
len(errors)
# %%
for raw_store in errors:
    zarr_grp = fst.read(raw_store)
    r = get_scale_info(zarr_grp)
    print(raw_store)
    print(r)
# %%
errors
# %%

from fly_organelles.utils import find_target_scale, get_scale_info

raw_grp = fst.read(os.path.join("/nrs/cellmap/zubovy/crop_splits/c-elegans/8nm/rescaled/jrc_c-elegans-comma-1/groundtruth.zarr/crop512/mito"))
raw_scale, raw_offset, raw_shape = find_target_scale(raw_grp, sampling)
# %%
