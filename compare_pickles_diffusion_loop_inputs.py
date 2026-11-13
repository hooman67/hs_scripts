import pickle
import torch
import numpy as np
from typing import Any, Dict
import os


def tensor_equal(t1: Any, t2: Any) -> bool:
    """Compare two tensors or arrays, handling different types."""
    if type(t1) != type(t2):
        print(f"Type mismatch: {type(t1)} vs {type(t2)}")
        return False

    if isinstance(t1, (torch.Tensor, np.ndarray)):
        if t1.shape != t2.shape:
            print(f"Shape mismatch: {t1.shape} vs {t2.shape}")
            return False
        return torch.allclose(torch.tensor(t1), torch.tensor(t2), rtol=1e-5, atol=1e-8)
    return t1 == t2


def compare_nested_structures(d1: Any, d2: Any, path: str = "") -> None:
    """Recursively compare two nested structures (dicts, lists, tensors, etc)."""
    if isinstance(d1, dict):
        if not isinstance(d2, dict):
            print(f"{path}: Type mismatch - d1 is dict, d2 is {type(d2)}")
            return

        # Check for key differences
        keys1, keys2 = set(d1.keys()), set(d2.keys())
        if keys1 != keys2:
            print(f"Key differences at {path}:")
            print(f"Keys only in first dict: {keys1 - keys2}")
            print(f"Keys only in second dict: {keys2 - keys1}")

        # Compare values for common keys
        for k in keys1 & keys2:
            new_path = f"{path}.{k}" if path else k
            compare_nested_structures(d1[k], d2[k], new_path)

    elif isinstance(d1, (list, tuple)):
        if not isinstance(d2, (list, tuple)):
            print(f"{path}: Type mismatch - d1 is {type(d1)}, d2 is {type(d2)}")
            return

        if len(d1) != len(d2):
            print(f"{path}: Length mismatch - {len(d1)} vs {len(d2)}")
            return

        for i, (v1, v2) in enumerate(zip(d1, d2)):
            compare_nested_structures(v1, v2, f"{path}[{i}]")

    elif isinstance(d1, (torch.Tensor, np.ndarray)) or isinstance(d2, (torch.Tensor, np.ndarray)):
        if not tensor_equal(d1, d2):
            print(f"{path}: Tensor/array values differ")
            if hasattr(d1, "shape") and hasattr(d2, "shape"):
                print(f"Shapes: {d1.shape} vs {d2.shape}")
            if hasattr(d1, "dtype") and hasattr(d2, "dtype"):
                print(f"DTypes: {d1.dtype} vs {d2.dtype}")

    elif d1 != d2:
        print(f"{path}: Values differ - {d1} vs {d2}")


def main():
    pickle1_path = "/sensei-fs/users/hshariati/del/from_colligo_512_t5.pkl"
    pickle2_path = "/sensei-fs/users/hshariati/del/diffusion_loop_inputs.pkl"

    # Load pickles
    with open(pickle1_path, "rb") as f:
        data1 = pickle.load(f)
    with open(pickle2_path, "rb") as f:
        data2 = pickle.load(f)

    print("Comparing pickles...")
    compare_nested_structures(data1, data2)
    print("Comparison complete.")


if __name__ == "__main__":
    main()
