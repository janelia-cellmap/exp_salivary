# Salivary Segmentation Models

This project tracks the model assignments for the `jrc_mus-salivary-*` datasets and the Hugging Face DOI citations for the exported salivary models.

## Dataset Model Assignments

| Dataset | Mito model | Nucleus model |
|---|---|---|
| `jrc_mus-salivary-1` | `mito_mouse_16_362000` | `nuc_mouse_64_90000` |
| `jrc_mus-salivary-2` | `mito_mouse_16_362000` | `nuc_all_mixed_32_582000` |
| `jrc_mus-salivary-3` | `mito_mouse_16_362000` | `nuc_mouse_32_342000` |

## Published Hugging Face Models

| Local alias | Hugging Face repo | DOI |
|---|---|---|
| `mito_mouse_16_362000` | [`cellmap/salivary_20250806_mito_mouse_distance_16nm_362000`](https://huggingface.co/cellmap/salivary_20250806_mito_mouse_distance_16nm_362000) | [`10.57967/HF/9493`](https://doi.org/10.57967/HF/9493) |
| `nuc_all_mixed_32_582000` | [`cellmap/salivary_20250725_nuc_all_mixed_distance_32nm_582000`](https://huggingface.co/cellmap/salivary_20250725_nuc_all_mixed_distance_32nm_582000) | [`10.57967/HF/9499`](https://doi.org/10.57967/HF/9499) |
| `nuc_mouse_32_342000` | [`cellmap/salivary_20250806_nuc_mouse_distance_32nm_342000`](https://huggingface.co/cellmap/salivary_20250806_nuc_mouse_distance_32nm_342000) | [`10.57967/HF/9492`](https://doi.org/10.57967/HF/9492) |

`nuc_mouse_64_90000` is listed in the dataset assignments above, but no matching public Hugging Face DOI was found for it during the citation fetch.

## APA Citations

### Mitochondria model

Janelia Cellmap. (2026). <i>salivary_20250806_mito_mouse_distance_16nm_362000</i> (Version 7df6a60). Hugging Face. https://doi.org/10.57967/HF/9493

### Mixed nucleus model

Janelia Cellmap. (2026). <i>salivary_20250725_nuc_all_mixed_distance_32nm_582000</i> (Version 82cfdb4). Hugging Face. https://doi.org/10.57967/HF/9499

### Mouse nucleus model

Janelia Cellmap. (2026). <i>salivary_20250806_nuc_mouse_distance_32nm_342000</i> (Version 8d2195d). Hugging Face. https://doi.org/10.57967/HF/9492

## BibTeX

```bibtex
@misc{janelia_cellmap_2026_salivary_mito_mouse_distance_16nm_362000,
  doi = {10.57967/HF/9493},
  url = {https://huggingface.co/cellmap/salivary_20250806_mito_mouse_distance_16nm_362000},
  author = {{Janelia Cellmap}},
  title = {salivary_20250806_mito_mouse_distance_16nm_362000},
  publisher = {Hugging Face},
  year = {2026}
}

@misc{janelia_cellmap_2026_salivary_nuc_all_mixed_distance_32nm_582000,
  doi = {10.57967/HF/9499},
  url = {https://huggingface.co/cellmap/salivary_20250725_nuc_all_mixed_distance_32nm_582000},
  author = {{Janelia Cellmap}},
  title = {salivary_20250725_nuc_all_mixed_distance_32nm_582000},
  publisher = {Hugging Face},
  year = {2026}
}

@misc{janelia_cellmap_2026_salivary_nuc_mouse_distance_32nm_342000,
  doi = {10.57967/HF/9492},
  url = {https://huggingface.co/cellmap/salivary_20250806_nuc_mouse_distance_32nm_342000},
  author = {{Janelia Cellmap}},
  title = {salivary_20250806_nuc_mouse_distance_32nm_342000},
  publisher = {Hugging Face},
  year = {2026}
}
```
