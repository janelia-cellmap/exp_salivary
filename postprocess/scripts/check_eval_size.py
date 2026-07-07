import torch


def find_valid_sizes(min_size, max_size, divisor=32):
    """
    Generate sizes that are compatible with the UNet architecture.
    Sizes should be divisible by the downsampling factor.
    """
    valid_sizes = []
    for size in range(min_size, max_size + 1):
        # Check if size works with repeated division by 2
        temp = size
        valid = True
        for _ in range(5):  # Assuming 5 levels of downsampling
            if temp % 2 != 0:
                valid = False
                break
            temp = temp // 2
        if valid or size % divisor == 0:
            valid_sizes.append(size)
    return valid_sizes


def binary_search_max_size(model, device, min_size=64, max_size=512, divisor=2):
    """
    Use binary search to find the maximum input size that works.
    Only tests sizes compatible with UNet downsampling.

    Args:
        model: The model to test
        device: The device to run on
        min_size: Minimum size to test (known to work)
        max_size: Maximum size to test (known to fail or upper bound)
        divisor: Divisor for valid sizes (typically 2 for UNet)

    Returns:
        Maximum successful input size
    """
    print(f"\n{'='*60}")
    print(f"Binary search for maximum size between {min_size} and {max_size}")
    print(f"(Testing only sizes compatible with downsampling by {divisor})")
    print(f"{'='*60}\n")

    # Generate valid sizes
    valid_sizes = []
    for size in range(min_size, max_size + 1):
        # Must be even for multiple levels of division by 2
        temp = size
        is_valid = True
        # Check if can be divided by 2 at least 5 times (typical UNet depth)
        for _ in range(5):
            if temp % 2 != 0:
                is_valid = False
                break
            temp = temp // 2
        if is_valid:
            valid_sizes.append(size)

    if not valid_sizes:
        print("No valid sizes found in the range!")
        return None

    print(f"Valid sizes to test: {len(valid_sizes)} sizes")
    print(f"Range: {valid_sizes[0]} to {valid_sizes[-1]}")
    print()

    left, right = 0, len(valid_sizes) - 1
    max_working = None

    while left <= right:
        mid_idx = (left + right) // 2
        mid = valid_sizes[mid_idx]
        size = (mid, mid, mid)

        try:
            torch.cuda.empty_cache()
            print(f"Testing size {mid}³ = {size}...")

            dummy_input = torch.randn(1, 1, *size, device=device)

            with torch.no_grad():
                output = model(dummy_input)

            allocated = torch.cuda.memory_allocated(0) / 1e9
            print(f"  ✓ SUCCESS - Output shape: {output.shape}")
            print(f"    Allocated: {allocated:.4f} GB")

            max_working = mid
            left = mid_idx + 1  # Try larger

            del dummy_input, output
            torch.cuda.empty_cache()

        except Exception as e:
            error_str = str(e)
            if "INT_MAX" in error_str or "upsample" in error_str:
                print(f"  ✗ FAILED - INT_MAX limitation")
            elif "out of memory" in error_str:
                print(f"  ✗ FAILED - Out of memory")
            elif "downsample" in error_str:
                print(f"  ✗ FAILED - Incompatible size for downsampling")
            else:
                print(f"  ✗ FAILED - {error_str[:100]}...")

            right = mid_idx - 1  # Try smaller

    if max_working:
        print(f"\n{'='*60}")
        print(
            f"Binary search result: Maximum size = {max_working}³ = ({max_working}, {max_working}, {max_working})"
        )
        print(f"{'='*60}\n")

    return max_working


def check_max_gpu_size(model, input_size=(178, 178, 178), step=128, max_size=1024):
    """
    Check the maximum input size that can be fed to the GPU for inference.

    Args:
        input_size: Starting input size as a tuple (z, y, x) or single int for cubic
        step: Step size for increasing dimensions
        max_size: Maximum size to test

    Returns:
        Maximum successful input size as a tuple
    """

    # Print GPU info
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(
        f"Total GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB"
    )
    print(f"Initial allocated: {torch.cuda.memory_allocated(0) / 1e9:.4f} GB")
    print(f"Initial reserved: {torch.cuda.memory_reserved(0) / 1e9:.4f} GB\n")

    # Handle input_size as int or tuple
    if isinstance(input_size, int):
        start_size = input_size
    else:
        start_size = input_size[0]  # Use first dimension

    # Generate test sizes dynamically
    test_sizes = []
    current_size = start_size
    while current_size <= max_size:
        test_sizes.append((current_size, current_size, current_size))
        current_size += step

    print(f"Testing sizes from {start_size} to {max_size} with step {step}")
    print(f"Test sizes: {test_sizes}\n")
    print("Testing input sizes with the model...\n")

    max_successful_size = None
    INT_MAX = 2147483647  # Maximum value for 32-bit signed integer

    for size in test_sizes:
        try:
            torch.cuda.empty_cache()
            print(f"Testing size {size}...")

            # Create a dummy input
            dummy_input = torch.randn(1, 1, *size, device=device)

            # Run inference
            with torch.no_grad():
                output = model(dummy_input)

            allocated = torch.cuda.memory_allocated(0) / 1e9
            reserved = torch.cuda.memory_reserved(0) / 1e9

            print(f"  ✓ SUCCESS - Output shape: {output.shape}")
            print(f"    Allocated: {allocated:.4f} GB, Reserved: {reserved:.4f} GB")
            print()

            max_successful_size = size

            # Clean up
            del dummy_input, output
            torch.cuda.empty_cache()

        except RuntimeError as e:
            error_str = str(e)
            if "out of memory" in error_str:
                print(f"  ✗ FAILED - Out of memory")
                print(f"    Error: {error_str[:150]}...")
                print()
                break
            elif "INT_MAX" in error_str or "upsample" in error_str:
                print(f"  ✗ FAILED - INT_MAX limitation in upsample operation")
                print(f"    Error: {error_str[:150]}...")
                print()
                # Extract the problematic tensor shape if available
                if "[" in error_str and "]" in error_str:
                    import re

                    match = re.search(r"\[[\d,\s]+\]", error_str)
                    if match:
                        shape_str = match.group()
                        print(f"    Problematic tensor shape: {shape_str}")
                        # Calculate elements
                        try:
                            shape_vals = [
                                int(x.strip()) for x in shape_str.strip("[]").split(",")
                            ]
                            elements = 1
                            for val in shape_vals:
                                elements *= val
                            print(
                                f"    Total elements: {elements:,} (INT_MAX: {INT_MAX:,})"
                            )
                        except:
                            pass
                print()
                break
            else:
                print(f"  ✗ FAILED - Runtime error")
                print(f"    Error: {error_str[:150]}...")
                print()
                break
        except Exception as e:
            print(f"  ✗ FAILED - {str(e)[:150]}...")
            print()
            break

    if max_successful_size:
        print(f"\n{'='*60}")
        print(f"Maximum successful input size: {max_successful_size}")
        print(f"{'='*60}")

    return max_successful_size


from fly_organelles.model import StandardUnet

if not torch.cuda.is_available():
    raise ValueError("CUDA is not available")

device = torch.device("cuda")

# Load model
model_backbone = StandardUnet(1)
model = torch.nn.Sequential(model_backbone, torch.nn.Sigmoid())
model.to(device)
model.eval()

# First do a quick step-based search
max_found = check_max_gpu_size(model, step=128)

# Then use binary search to find the exact maximum
if max_found:
    last_size = max_found[0]
    # Binary search between the last successful and last_successful + step
    binary_search_max_size(model, device, min_size=last_size, max_size=last_size + 128)


# bsub -P cellmap -J h100_task -q gpu_h100 -gpu "num=1" -n12 -o h100.err -e h100.out python check_eval_size.py
# bsub -P cellmap -J h200_task -q gpu_h200 -gpu "num=1" -n12 -o h200.err -e h200.out python check_eval_size.py
