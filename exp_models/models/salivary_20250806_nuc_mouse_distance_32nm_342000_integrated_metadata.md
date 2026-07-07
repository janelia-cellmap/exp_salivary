# salivary_20250806_nuc_mouse_distance_32nm_342000

| Field | Value |
|---|---|
| dataset name | Final-result dataset: `jrc_mus-salivary-3` nuc. Training YAML: `20250806_nuc_mouse.yaml` mouse dataset set. |
| architecture | `StandardUnet` |
| number of parameters | `792,405,937` |
| input voxel size (nm) | `[32, 32, 32]` |
| output voxel size (nm) | `[32, 32, 32]` |
| model location | `/groups/cellmap/cellmap/zouinkhim/exp_salivary/exp_models/models/salivary_20250806_nuc_mouse_distance_32nm_342000` |
| number of slices | `3,313` training crop z-slices at 32 nm (`s2`). Final salivary-only subset: `592`. |
| number of training epochs | Not applicable / not recorded. Training is iteration-based over sampled crops. |
| number of ids | Training dataset IDs: `10`; training crop IDs: `37`; final salivary dataset IDs: `1`. |
| training time (wall time) in seconds | `1,359,088` |
| training steps | Final checkpoint step: `342,000`. Training script planned `1,000,000` iterations. |
| GPU | `1x A100` (`gpu_a100` queue, `-gpu "num=1"`) |
| RAM | Requested: `491,520 MB`. Measured max/average memory were not reported in the LSF summary. |
| software | `fly-organelles 0.0.1`, `cellmap-models 0.2.3`, `PyTorch`, `funlib.learn.torch 0.1.0` |
| software DOI | Not found in local `fly-organelles` or `cellmap-models` metadata. |
| model URL | `https://huggingface.co/cellmap/salivary_20250806_nuc_mouse_distance_32nm_342000` |

## Sources

- Exported metadata: `/groups/cellmap/cellmap/zouinkhim/exp_salivary/exp_models/models/salivary_20250806_nuc_mouse_distance_32nm_342000/metadata.json`
- Final-result YAML: `/groups/cellmap/cellmap/zouinkhim/exp_salivary/persistence/nuc/jrc_mus-salivary-3/20250915_mito.yaml`
- Training YAML: `/groups/cellmap/cellmap/zouinkhim/exp_c-elegen/v3/yamls/generated/20250806_nuc_mouse.yaml`
- Training run: `/groups/cellmap/cellmap/zouinkhim/exp_c-elegen/v3/train/runs/20250806_nuc_mouse_distance_32nm`
- Final checkpoint: `/groups/cellmap/cellmap/zouinkhim/exp_c-elegen/v3/train/runs/20250806_nuc_mouse_distance_32nm/model_checkpoint_342000`
