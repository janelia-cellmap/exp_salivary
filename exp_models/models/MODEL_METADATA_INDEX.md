# Salivary Final Model Metadata

This directory contains exported model folders plus separate integrated metadata summaries for the salivary final-result models.

| Model | Metadata file |
|---|---|
| `salivary_20250806_mito_mouse_distance_16nm_362000` | `salivary_20250806_mito_mouse_distance_16nm_362000_integrated_metadata.md` |
| `salivary_20250725_nuc_all_mixed_distance_32nm_582000` | `salivary_20250725_nuc_all_mixed_distance_32nm_582000_integrated_metadata.md` |
| `salivary_20250806_nuc_mouse_distance_32nm_342000` | `salivary_20250806_nuc_mouse_distance_32nm_342000_integrated_metadata.md` |

Notes:

- `number_of_parameters` was derived by instantiating the actual `fly-organelles` `StandardUnet(1)` in the `fly` conda environment.
- `number_of_slices` is the sum of label-array z sizes over training crop IDs at the model voxel size. For the all-mixed nucleus model, the current filesystem is missing 12 referenced `jrc_c-elegans-comma-1` crop paths, so that slice count is incomplete.
- Hugging Face URLs assume the default publishing org/user `cellmap`.
