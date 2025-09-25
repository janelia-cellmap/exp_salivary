import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import glob
from tqdm import tqdm


def delete_folder(folder_path):
    """Delete a single folder"""
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            return f"Deleted: {folder_path}"
        else:
            return f"Folder not found: {folder_path}"
    except Exception as e:
        return f"Error deleting {folder_path}: {e}"


def delete_mito_folders():
    """Delete all mito_* folders in parallel"""
    base_path = "/nrs/cellmap/zouinkhim/predictions/salivary/jrc_mus-salivary-1.zarr/postprocess"

    # Find all mito_* folders
    mito_folders = glob.glob(os.path.join(base_path, "mito_*/*/*"))

    if not mito_folders:
        print("No mito_* folders found")
        return

    print(f"Found {len(mito_folders)} mito_* folders to delete")

    # Delete folders in parallel with progress bar
    with ThreadPoolExecutor(max_workers=80) as executor:
        # Submit all tasks
        futures = {
            executor.submit(delete_folder, folder): folder for folder in mito_folders
        }

        # Process results with progress bar
        with tqdm(total=len(mito_folders), desc="Deleting folders") as pbar:
            for future in as_completed(futures):
                result = future.result()
                print(result)
                pbar.update(1)

    print("Deletion complete")


if __name__ == "__main__":
    delete_mito_folders()
# %%
