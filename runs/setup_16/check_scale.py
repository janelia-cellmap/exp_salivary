# %%
yaml_file = "/groups/cellmap/cellmap/zouinkhim/exp_salivary/runs/setup_16/20250914_all_mitos.yaml"
import yaml
with open(yaml_file, "r") as data_yaml:
    datasets = yaml.safe_load(data_yaml)
#%%
raws = [v["raw"] for _,v in datasets["datasets"].items()]

len(raws)
# %%
from fly_organelles.utils import find_target_scale, get_nominal_scale_info
#%%
import fibsem_tools as fst
sampling = [16,16,16]
errors = []
for raw_store in raws:
    try:
        raw_grp = fst.read(raw_store)
        raw_scale, raw_offset, raw_shape = find_target_scale(raw_grp, sampling)
    except Exception as e:
        errors.append(raw_store)
len(errors)
# %%
for raw_store in errors:
    zarr_grp = fst.read(raw_store)
    r = get_nominal_scale_info(zarr_grp)
    print(raw_store)
    print(r[1])
# %%
errors
# %%
from fly_organelles.utils import find_target_scale, get_nominal_scale_info
import fibsem_tools as fst
sampling = [16,16,16]
raw_grp = fst.read(raw_store)
raw_scale, raw_offset, raw_shape = find_target_scale(raw_grp, sampling)
# %%
