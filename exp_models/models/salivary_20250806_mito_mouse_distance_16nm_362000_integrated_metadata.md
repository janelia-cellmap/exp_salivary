# salivary_20250806_mito_mouse_distance_16nm_362000

| Field | Value |
|---|---|
| dataset name | Final-result datasets: `jrc_mus-salivary-1` mito, `jrc_mus-salivary-2` mito, `jrc_mus-salivary-3` mito. Training YAML: `20250806_mito_mouse.yaml` mouse dataset set. |
| architecture | `StandardUnet` |
| number of parameters | `792,405,937` |
| input voxel size (nm) | `[16, 16, 16]` |
| output voxel size (nm) | `[16, 16, 16]` |
| model location | `/groups/cellmap/cellmap/zouinkhim/exp_salivary/exp_models/models/salivary_20250806_mito_mouse_distance_16nm_362000` |
| number of slices | `8,035` training crop z-slices at 16 nm (`s1`). Final salivary-only subset: `4,160`. |
| number of training epochs | Not applicable / not recorded. Training is iteration-based over sampled crops. |
| number of ids | Training dataset IDs: `10`; training crop IDs: `48`; final salivary dataset IDs: `3`. |
| training time (wall time) in seconds | `1,359,307` |
| training steps | Final checkpoint step: `362,000`. Training script planned `1,000,000` iterations. |
| GPU | `1x A100` (`gpu_a100` queue, `-gpu "num=1"`) |
| RAM | Requested: `491,520 MB`. Measured max/average memory were not reported in the LSF summary. |
| software | `fly-organelles 0.0.1`, `cellmap-models 0.2.3`, `PyTorch`, `funlib.learn.torch 0.1.0` |
| software DOI | Not found in local `fly-organelles` or `cellmap-models` metadata. |
| model URL | `https://huggingface.co/cellmap/salivary_20250806_mito_mouse_distance_16nm_362000` |

## Sources

- Exported metadata: `/groups/cellmap/cellmap/zouinkhim/exp_salivary/exp_models/models/salivary_20250806_mito_mouse_distance_16nm_362000/metadata.json`
- Final-result YAMLs:
  - `/groups/cellmap/cellmap/zouinkhim/exp_salivary/persistence/mito/jrc_mus-salivary-1/20250915_mito.yaml`
  - `/groups/cellmap/cellmap/zouinkhim/exp_salivary/persistence/mito/jrc_mus-salivary-2/20250915_mito.yaml`
  - `/groups/cellmap/cellmap/zouinkhim/exp_salivary/persistence/mito/jrc_mus-salivary-3/20250915_mito.yaml`
- Training YAML: `/groups/cellmap/cellmap/zouinkhim/exp_c-elegen/v3/yamls/generated/20250806_mito_mouse.yaml`
- Training run: `/groups/cellmap/cellmap/zouinkhim/exp_c-elegen/v3/train/runs/20250806_mito_mouse_distance_16nm`
- Final checkpoint: `/groups/cellmap/cellmap/zouinkhim/exp_c-elegen/v3/train/runs/20250806_mito_mouse_distance_16nm/model_checkpoint_362000`
