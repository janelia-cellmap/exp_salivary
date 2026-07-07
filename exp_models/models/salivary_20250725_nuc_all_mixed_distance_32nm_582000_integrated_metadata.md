# salivary_20250725_nuc_all_mixed_distance_32nm_582000

| Field | Value |
|---|---|
| dataset name | Final-result dataset: `jrc_mus-salivary-2` nuc. Training YAML: `20250725_nuc_all_mixed.yaml` all-mixed dataset set. |
| architecture | `StandardUnet` |
| number of parameters | `792,405,937` |
| input voxel size (nm) | `[32, 32, 32]` |
| output voxel size (nm) | `[32, 32, 32]` |
| model location | `/groups/cellmap/cellmap/zouinkhim/exp_salivary/exp_models/models/salivary_20250725_nuc_all_mixed_distance_32nm_582000` |
| number of slices | At least `4,835` known training crop z-slices at 32 nm (`s2`). The current filesystem is missing 12 referenced `jrc_c-elegans-comma-1` crop paths, so the complete training slice count cannot be confirmed from current storage. Final salivary-only subset: `525`. |
| number of training epochs | Not applicable / not recorded. Training is iteration-based over sampled crops. |
| number of ids | Training dataset IDs: `14`; training crop IDs: `58`; final salivary dataset IDs: `1`. |
| training time (wall time) in seconds | `773,799` |
| training steps | Final checkpoint step: `582,000`. Training script planned `1,000,000` iterations. |
| GPU | `1x A100` (`gpu_a100` queue, `-gpu "num=1"`) |
| RAM | Requested: `491,520 MB`; max memory: `83,788 MB`; average memory: `51,479.22 MB`. |
| software | `fly-organelles 0.0.1`, `cellmap-models 0.2.3`, `PyTorch`, `funlib.learn.torch 0.1.0` |
| software DOI | Not found in local `fly-organelles` or `cellmap-models` metadata. |
| model URL | `https://huggingface.co/cellmap/salivary_20250725_nuc_all_mixed_distance_32nm_582000` |

## Sources

- Exported metadata: `/groups/cellmap/cellmap/zouinkhim/exp_salivary/exp_models/models/salivary_20250725_nuc_all_mixed_distance_32nm_582000/metadata.json`
- Final-result YAML: `/groups/cellmap/cellmap/zouinkhim/exp_salivary/persistence/nuc/jrc_mus-salivary-2/20250915_mito.yaml`
- Training YAML: `/groups/cellmap/cellmap/zouinkhim/exp_c-elegen/v3/yamls/generated/20250725_nuc_all_mixed.yaml`
- Training run: `/groups/cellmap/cellmap/zouinkhim/exp_c-elegen/v3/train/runs/20250725_nuc_all_mixed_distance_32nm`
- Final checkpoint: `/groups/cellmap/cellmap/zouinkhim/exp_c-elegen/v3/train/runs/20250725_nuc_all_mixed_distance_32nm/model_checkpoint_582000`
