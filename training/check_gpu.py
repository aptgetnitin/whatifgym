#!/usr/bin/env python3
"""Check that this machine can train: CUDA, the GPU and its architecture, the training libraries, a small matmul.

    python training/check_gpu.py

An RTX 50-series GPU (Blackwell) is compute capability 12.0 and needs a PyTorch build that lists `sm_120`;
an older build fails later with "no kernel image is available".
"""
import importlib
import sys


def main() -> int:
    ok = True
    import torch

    print(f"torch {torch.__version__}, CUDA build {torch.version.cuda}")
    if not torch.cuda.is_available():
        print("FAIL: CUDA is not available. On WSL2, check `nvidia-smi` inside Ubuntu and the Windows driver.")
        return 1
    cap = torch.cuda.get_device_capability(0)
    free, total = torch.cuda.mem_get_info(0)
    print(f"GPU {torch.cuda.get_device_name(0)}: compute capability {cap[0]}.{cap[1]}, "
          f"{total / 1e9:.1f} GB ({free / 1e9:.1f} GB free)")
    arch = torch.cuda.get_arch_list()
    needed = f"sm_{cap[0]}{cap[1]}"
    if needed not in arch:
        print(f"FAIL: this PyTorch build has {arch}, not {needed}. Install the CUDA 12.8 build (training/README.md).")
        ok = False
    x = torch.randn(2048, 2048, device="cuda", dtype=torch.bfloat16)
    torch.cuda.synchronize()
    print(f"matmul ok: {float((x @ x).float().abs().mean()):.3f}")
    for lib in ("unsloth", "vllm", "trl", "datasets", "pulp", "highspy"):
        try:
            mod = importlib.import_module(lib)
            print(f"{lib} {getattr(mod, '__version__', '?')}")
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL: cannot import {lib}: {type(exc).__name__}: {exc}")
            ok = False
    print("READY" if ok else "NOT READY")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
