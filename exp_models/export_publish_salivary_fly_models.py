#!/usr/bin/env python3
"""Export salivary persistence fly models and optionally publish/DOI them.

This follows:
  /groups/cellmap/cellmap/zouinkhim/export_models/cellmap-models/how_to/how_to_fly_model.md

Default behavior exports all configured models. Add --publish to upload the
exported folders to Hugging Face. Add --zenodo to create Zenodo DOI drafts
linked to exact Hugging Face revisions.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from dataclasses import dataclass
from pathlib import Path


WORKSPACE_ROOT = Path("/groups/cellmap/cellmap/zouinkhim")
SCRIPT_DIR = Path(__file__).resolve().parent
CELLMAP_MODELS_SRC = WORKSPACE_ROOT / "export_models/cellmap-models/src"
FLY_ORGANELLES_SRC = WORKSPACE_ROOT / "fly/fly-organelles/src"

STANDARD_INPUT_SHAPE = [178, 178, 178]
STANDARD_OUTPUT_SHAPE = [56, 56, 56]
EXPORT_INPUT_SHAPE = [1, 1, *STANDARD_INPUT_SHAPE]
INFERENCE_INPUT_SHAPE = [378, 378, 378]
INFERENCE_OUTPUT_SHAPE = [256, 256, 256]


@dataclass(frozen=True)
class SalivaryModelSpec:
    model_name: str
    channel_name: str
    checkpoint_path: Path
    iteration: int
    voxel_size_nm: int
    source_yamls: tuple[Path, ...]
    used_for: tuple[str, ...]

    @property
    def output_shape(self) -> list[int]:
        return STANDARD_OUTPUT_SHAPE

    @property
    def voxel_size(self) -> list[int]:
        return [self.voxel_size_nm, self.voxel_size_nm, self.voxel_size_nm]


MODELS = [
    SalivaryModelSpec(
        model_name="salivary_20250806_mito_mouse_distance_16nm_362000",
        channel_name="mito",
        checkpoint_path=WORKSPACE_ROOT
        / "c-elegen/v3/train/runs/20250806_mito_mouse_distance_16nm/model_checkpoint_362000",
        iteration=362000,
        voxel_size_nm=16,
        source_yamls=(
            WORKSPACE_ROOT
            / "exp_salivary/persistence/mito/jrc_mus-salivary-1/20250915_mito.yaml",
            WORKSPACE_ROOT
            / "exp_salivary/persistence/mito/jrc_mus-salivary-2/20250915_mito.yaml",
            WORKSPACE_ROOT
            / "exp_salivary/persistence/mito/jrc_mus-salivary-3/20250915_mito.yaml",
        ),
        used_for=(
            "jrc_mus-salivary-1 mito",
            "jrc_mus-salivary-2 mito",
            "jrc_mus-salivary-3 mito",
        ),
    ),
    SalivaryModelSpec(
        model_name="salivary_20250806_nuc_mouse_distance_64nm_90000",
        channel_name="nuc",
        checkpoint_path=WORKSPACE_ROOT
        / "c-elegen/v3/train/runs/20250806_nuc_mouse_distance_64nm/model_checkpoint_90000",
        iteration=90000,
        voxel_size_nm=64,
        source_yamls=(
            WORKSPACE_ROOT
            / "exp_salivary/persistence/nuc/jrc_mus-salivary-1/20250915_mito.yaml",
        ),
        used_for=("jrc_mus-salivary-1 nuc",),
    ),
    SalivaryModelSpec(
        model_name="salivary_20250725_nuc_all_mixed_distance_32nm_582000",
        channel_name="nuc",
        checkpoint_path=WORKSPACE_ROOT
        / "exp_c-elegen/v3/train/runs/20250725_nuc_all_mixed_distance_32nm/model_checkpoint_582000",
        iteration=582000,
        voxel_size_nm=32,
        source_yamls=(
            WORKSPACE_ROOT
            / "exp_salivary/persistence/nuc/jrc_mus-salivary-2/20250915_mito.yaml",
        ),
        used_for=("jrc_mus-salivary-2 nuc",),
    ),
    SalivaryModelSpec(
        model_name="salivary_20250806_nuc_mouse_distance_32nm_342000",
        channel_name="nuc",
        checkpoint_path=WORKSPACE_ROOT
        / "exp_c-elegen/v3/train/runs/20250806_nuc_mouse_distance_32nm/model_checkpoint_342000",
        iteration=342000,
        voxel_size_nm=32,
        source_yamls=(
            WORKSPACE_ROOT
            / "exp_salivary/persistence/nuc/jrc_mus-salivary-3/20250915_mito.yaml",
        ),
        used_for=("jrc_mus-salivary-3 nuc",),
    ),
    SalivaryModelSpec(
        model_name="salivary_20251215_er_setup_46_580000",
        channel_name="er",
        checkpoint_path=WORKSPACE_ROOT / "exp_mito/runs/setup_46/model_checkpoint_580000",
        iteration=580000,
        voxel_size_nm=8,
        source_yamls=(
            WORKSPACE_ROOT
            / "exp_salivary/persistence/er/jrc_mus-salivary-1/20251215_er.yaml",
            WORKSPACE_ROOT
            / "exp_salivary/persistence/er/jrc_mus-salivary-3/20251215_er.yaml",
        ),
        used_for=("jrc_mus-salivary-1 er", "jrc_mus-salivary-3 er"),
    ),
]


def prepare_import_paths() -> None:
    for path in (CELLMAP_MODELS_SRC, FLY_ORGANELLES_SRC):
        if path.exists():
            sys.path.insert(0, str(path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export salivary persistence fly models and optionally push to Hugging Face."
    )
    parser.add_argument(
        "--export-folder",
        default=os.environ.get(
            "CELLMAP_EXPORT_FOLDER", str(SCRIPT_DIR / "exported_models")
        ),
        help="Folder where Hugging Face-ready model folders are written.",
    )
    parser.add_argument(
        "--repo-org",
        default="cellmap",
        help="Hugging Face org/user used when --publish is set.",
    )
    parser.add_argument(
        "--model",
        action="append",
        choices=[spec.model_name for spec in MODELS],
        help="Model name to process. Repeat to select several. Defaults to all.",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Push exported model folders to Hugging Face after export.",
    )
    parser.add_argument(
        "--skip-export",
        action="store_true",
        help="Only publish already-exported folders.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite metadata/model files in existing export folders.",
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Create/update private Hugging Face repos when publishing.",
    )
    parser.add_argument(
        "--zenodo",
        action="store_true",
        help="Create a Zenodo draft DOI after export/publish.",
    )
    parser.add_argument(
        "--hf-revision",
        help=(
            "Exact Hugging Face revision to link in Zenodo. If omitted, the "
            "script queries the current repo SHA."
        ),
    )
    parser.add_argument(
        "--zenodo-production",
        action="store_true",
        help="Use production Zenodo for --zenodo. Default is Zenodo sandbox.",
    )
    parser.add_argument(
        "--zenodo-publish",
        action="store_true",
        help="Publish the Zenodo record immediately instead of leaving a draft.",
    )
    parser.add_argument(
        "--zenodo-yes",
        action="store_true",
        help="Confirm irreversible production publish when using --zenodo-publish.",
    )
    parser.add_argument(
        "--zenodo-upload",
        choices=("manifest", "archive"),
        default="manifest",
        help="Zenodo upload mode. Manifest is best for large model folders.",
    )
    parser.add_argument(
        "--zenodo-upload-type",
        choices=("dataset", "software", "other"),
        default="software",
        help="Zenodo upload type.",
    )
    parser.add_argument(
        "--zenodo-creator",
        action="append",
        help=(
            "Creator as 'Name|Affiliation|ORCID'. Can be repeated. Defaults "
            "to the creator shown in the fly-model how-to."
        ),
    )
    parser.add_argument("--zenodo-title", help="Zenodo record title.")
    parser.add_argument("--zenodo-description", help="Zenodo record description.")
    parser.add_argument(
        "--zenodo-keyword",
        action="append",
        help="Zenodo keyword. Can be repeated.",
    )
    parser.add_argument(
        "--zenodo-license",
        default="bsd-3-clause",
        help="Zenodo license id.",
    )
    parser.add_argument(
        "--device",
        default="auto",
        choices=("auto", "cpu", "cuda"),
        help="Device used to load and trace the model.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print configured model names and exit.",
    )
    parser.add_argument(
        "--strict-yaml-paths",
        action="store_true",
        help="Use only the checkpoint paths written in the YAMLs, with no local prefix fallback.",
    )
    return parser.parse_args()


def selected_specs(names: list[str] | None) -> list[SalivaryModelSpec]:
    if not names:
        return MODELS
    wanted = set(names)
    return [spec for spec in MODELS if spec.model_name in wanted]


def checkpoint_candidates(spec: SalivaryModelSpec, strict_yaml_paths: bool) -> list[Path]:
    candidates = [spec.checkpoint_path]
    if strict_yaml_paths:
        return candidates

    checkpoint_text = str(spec.checkpoint_path)
    fallback_texts = []
    if "/c-elegen/" in checkpoint_text:
        fallback_texts.append(checkpoint_text.replace("/c-elegen/", "/exp_c-elegen/"))
    if "/exp_mito/" in checkpoint_text:
        fallback_texts.append(checkpoint_text.replace("/exp_mito/", "/exp_salivary/"))

    for fallback_text in fallback_texts:
        fallback = Path(fallback_text)
        if fallback not in candidates:
            candidates.append(fallback)
    return candidates


def resolve_checkpoint_path(spec: SalivaryModelSpec, strict_yaml_paths: bool) -> Path:
    candidates = checkpoint_candidates(spec, strict_yaml_paths)
    for candidate in candidates:
        if candidate.exists():
            if candidate != spec.checkpoint_path:
                print(
                    f"Warning: YAML checkpoint is missing for {spec.model_name}; "
                    f"using local fallback {candidate}"
                )
            return candidate

    checked = "\n  - ".join(str(path) for path in candidates)
    raise FileNotFoundError(
        f"Could not find checkpoint for {spec.model_name}. Checked:\n  - {checked}"
    )


def load_eval_model(checkpoint_path: Path, device_name: str):
    import torch

    try:
        from fly_organelles.model import StandardUnet
    except ModuleNotFoundError as exc:
        if exc.name != "fibsem_tools":
            raise
        model_py = FLY_ORGANELLES_SRC / "fly_organelles/model.py"
        spec = importlib.util.spec_from_file_location("fly_organelles_model", model_py)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load fly model from {model_py}") from exc
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        StandardUnet = module.StandardUnet

    if device_name == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device_name)

    model_backbone = StandardUnet(1)
    try:
        checkpoint = torch.load(
            checkpoint_path, weights_only=True, map_location=device
        )
    except TypeError:
        checkpoint = torch.load(checkpoint_path, map_location=device)

    state_dict = checkpoint.get("model_state_dict", checkpoint)
    model_backbone.load_state_dict(state_dict)
    model = torch.nn.Sequential(model_backbone, torch.nn.Sigmoid())
    model.to(device)
    model.eval()
    if device.type != "cpu":
        print("Moving model to CPU for export; cellmap-models creates CPU dummy inputs.")
        model.to(torch.device("cpu"))
    return model


def build_metadata(spec: SalivaryModelSpec):
    from cellmap_models.model_export import ModelMetadata

    source_yamls = ", ".join(str(path) for path in spec.source_yamls)
    used_for = ", ".join(spec.used_for)
    description = (
        f"Fly StandardUnet model used for salivary persistence final results. "
        f"Channel: {spec.channel_name}. Used for: {used_for}. "
        f"Source YAMLs: {source_yamls}."
    )
    return ModelMetadata(
        model_name=spec.model_name,
        iteration=spec.iteration,
        model_type="StandardUnet",
        framework="torch",
        spatial_dims=3,
        in_channels=1,
        out_channels=1,
        channels_names=[spec.channel_name],
        input_shape=STANDARD_INPUT_SHAPE,
        output_shape=spec.output_shape,
        inference_input_shape=INFERENCE_INPUT_SHAPE,
        inference_output_shape=INFERENCE_OUTPUT_SHAPE,
        input_voxel_size=spec.voxel_size,
        output_voxel_size=spec.voxel_size,
        author="CellMap Project Team, HHMI Janelia",
        description=description,
        version="1.0.0",
    )


def export_model(spec: SalivaryModelSpec, args: argparse.Namespace, export_folder: Path) -> Path:
    import cellmap_models.model_export.config as export_config
    from cellmap_models.model_export import export_metadata, export_torch_model
    from cellmap_models.model_export.cellmap_model import CellmapModel

    folder_path = export_folder / spec.model_name
    if folder_path.exists() and not args.overwrite:
        print(f"Export exists, skipping without --overwrite: {folder_path}")
        CellmapModel(str(folder_path))
        return folder_path

    checkpoint_path = resolve_checkpoint_path(spec, args.strict_yaml_paths)
    print(f"Exporting {spec.model_name}")
    print(f"  checkpoint: {checkpoint_path}")
    print(f"  output:     {folder_path}")

    export_config.EXPORT_FOLDER = str(export_folder)
    model = load_eval_model(checkpoint_path, args.device)
    metadata = build_metadata(spec)

    export_metadata(metadata, overwrite=args.overwrite)
    export_torch_model(model, tuple(EXPORT_INPUT_SHAPE), str(folder_path))
    CellmapModel(str(folder_path))
    return folder_path


def publish_model(spec: SalivaryModelSpec, folder_path: Path, args: argparse.Namespace) -> None:
    from cellmap_models.model_export import push_to_huggingface

    repo_id = f"{args.repo_org}/{spec.model_name}"
    print(f"Pushing {folder_path} -> {repo_id}")
    push_to_huggingface(
        folder_path=str(folder_path),
        repo_id=repo_id,
        commit_message=f"Upload {spec.model_name}",
        private=args.private,
    )


def huggingface_repo_id(spec: SalivaryModelSpec, args: argparse.Namespace) -> str:
    return f"{args.repo_org}/{spec.model_name}"


def resolve_hf_revision(repo_id: str, requested_revision: str | None) -> str:
    if requested_revision:
        return requested_revision

    from huggingface_hub import HfApi

    print(f"Resolving exact Hugging Face revision for {repo_id}")
    info = HfApi().model_info(repo_id)
    revision = getattr(info, "sha", None)
    if not revision:
        raise RuntimeError(
            f"Could not resolve a Hugging Face commit SHA for {repo_id}. "
            "Pass --hf-revision explicitly."
        )
    return revision


def create_zenodo_doi(
    spec: SalivaryModelSpec, folder_path: Path, args: argparse.Namespace
) -> None:
    from cellmap_models.model_export import zenodo_doi

    repo_id = huggingface_repo_id(spec, args)
    hf_revision = resolve_hf_revision(repo_id, args.hf_revision)
    creators = args.zenodo_creator or ["Zouinkhi, Marwan|HHMI Janelia"]

    zenodo_args = [
        str(folder_path),
        "--hf-repo",
        repo_id,
        "--hf-revision",
        hf_revision,
        "--upload",
        args.zenodo_upload,
        "--upload-type",
        args.zenodo_upload_type,
        "--license",
        args.zenodo_license,
    ]
    for creator in creators:
        zenodo_args.extend(["--creator", creator])
    for keyword in args.zenodo_keyword or []:
        zenodo_args.extend(["--keyword", keyword])
    if args.zenodo_title:
        zenodo_args.extend(["--title", args.zenodo_title])
    if args.zenodo_description:
        zenodo_args.extend(["--description", args.zenodo_description])
    if args.zenodo_production:
        zenodo_args.append("--production")
    if args.zenodo_publish:
        zenodo_args.append("--publish")
    if args.zenodo_yes:
        zenodo_args.append("--yes")

    print(f"Creating Zenodo DOI draft for {repo_id}")
    zenodo_doi.main(zenodo_args)


def main() -> int:
    args = parse_args()
    specs = selected_specs(args.model)

    if args.list:
        for spec in specs:
            print(f"{spec.model_name}: {spec.checkpoint_path}")
        return 0

    prepare_import_paths()
    export_folder = Path(args.export_folder).expanduser().resolve()
    export_folder.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        folder_path = export_folder / spec.model_name
        if not args.skip_export:
            folder_path = export_model(spec, args, export_folder)
        elif not folder_path.exists():
            raise FileNotFoundError(
                f"Cannot publish {spec.model_name}; exported folder not found: {folder_path}"
            )

        if args.publish:
            publish_model(spec, folder_path, args)
        if args.zenodo:
            create_zenodo_doi(spec, folder_path, args)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
