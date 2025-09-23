## Runs: 

| Name     | Org  | Learning Rate | Resolution | Batch Size | LSD | Starter Checkpoint                                                                           |
|----------|------|---------------|------------|------------|-----|----------------------------------------------------------------------------------------------|
| setup_15 | mito | 5.0e-05       | 16nm       | 14         | No  | 20250806_mito_mouse_distance_16nm/model_checkpoint_362000                                    |
| setup_16 | mito | 5.0e-05       | 16nm       | 14         | Yes | setup_15/model_checkpoint_80000                                                              |
| setup_17 | mito | 5.0e-05       | 32nm       | 14         | Yes | setup_16/model_checkpoint_30000                                                              |
| setup_18 | mito | 5.0e-05       | 32nm       | 14         | Yes | 20250725_mito_all_mixed_distance_16nm/model_checkpoint_372000                                |
| setup_19 | mito | 5.0e-05       | 16nm       | 14         | Yes | 20250725_mito_all_mixed_distance_16nm/model_checkpoint_372000                                |