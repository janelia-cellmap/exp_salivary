---
library_name: cellmap-models
tags:
- pytorch
- onnx
- torchscript
- 3d
- segmentation
- electron-microscopy
- cellmap
- mito
license: bsd-3-clause
---

# salivary_20250806_mito_mouse_distance_16nm_362000

Fly StandardUnet model used for salivary persistence final results. Channel: mito. Used for: jrc_mus-salivary-1 mito, jrc_mus-salivary-2 mito, jrc_mus-salivary-3 mito. Source YAMLs: /groups/cellmap/cellmap/zouinkhim/exp_salivary/persistence/mito/jrc_mus-salivary-1/20250915_mito.yaml, /groups/cellmap/cellmap/zouinkhim/exp_salivary/persistence/mito/jrc_mus-salivary-2/20250915_mito.yaml, /groups/cellmap/cellmap/zouinkhim/exp_salivary/persistence/mito/jrc_mus-salivary-3/20250915_mito.yaml.

## Model Details

| | |
|---|---|
| **Architecture** | StandardUnet |
| **Framework** | torch |
| **Spatial Dims** | 3 |
| **Input Channels** | 1 |
| **Output Channels** | 1 |
| **Channel Names** | mito |
| **Iteration** | 362000 |
| **Input Voxel Size** | 16, 16, 16 nm |
| **Output Voxel Size** | 16, 16, 16 nm |
| **Inference Input Shape** | 378, 378, 378 |
| **Inference Output Shape** | 256, 256, 256 |

## Available Formats

| File | Format | Usage |
|---|---|---|
| `model.pt` | PyTorch pickle | `torch.load("model.pt")` |
| `model.ts` | TorchScript | `torch.jit.load("model.ts")` |
| `model.onnx` | ONNX | `onnxruntime.InferenceSession("model.onnx")` |
| `metadata.json` | JSON | Model metadata |

## Usage

```bash
pip install cellmap-models
```

```python
from cellmap_models.model_export.cellmap_model import CellmapModel

model = CellmapModel("path/to/model/folder")

# Inference
output = model.ts_model(input_tensor)

# Finetuning
trainable_model = model.train()
```

Or download from this repo and load directly:

```python
from huggingface_hub import snapshot_download
from cellmap_models.model_export.cellmap_model import CellmapModel

path = snapshot_download(repo_id="salivary_20250806_mito_mouse_distance_16nm_362000")
model = CellmapModel(path)
```

## Author

CellMap Project Team, HHMI Janelia

## Links

- [cellmap-models](https://github.com/janelia-cellmap/cellmap-models)
- [CellMap Project](https://www.janelia.org/project-team/cellmap)
