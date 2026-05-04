#!/usr/bin/env python3
"""
gpu_utils.py
Shared GPU acceleration utilities for Argos Translate.

This module provides centralized GPU detection and configuration logic
to avoid code duplication across translation scripts.
"""

import os
import sys


def setup_gpu_acceleration(debug_log_func=None):
    """
    Configure GPU acceleration for argostranslate.
    Sets ARGOS_DEVICE_TYPE to 'cuda' if GPU is available, otherwise 'cpu'.

    Args:
        debug_log_func: Optional function for debug logging (e.g., debug_log from translate_runner)

    Returns:
        str: The device type that was configured ('cuda' or 'cpu')
    """
    # Helper for optional debug logging
    def log(msg):
        if debug_log_func:
            debug_log_func(msg)

    # Only set if not already configured by user
    if "ARGOS_DEVICE_TYPE" in os.environ:
        log(f"GPU config: Using user-defined ARGOS_DEVICE_TYPE={os.environ['ARGOS_DEVICE_TYPE']}")
        return os.environ["ARGOS_DEVICE_TYPE"]

    device_type = "cpu"  # Default fallback

    try:
        import torch
        if torch.cuda.is_available():
            device_type = "cuda"
            msg = "[translate] GPU acceleration enabled (CUDA available)"
            print(msg, file=sys.stderr)
            log("GPU config: GPU acceleration enabled (CUDA available)")
        else:
            msg = "[translate] Using CPU (no CUDA device found)"
            print(msg, file=sys.stderr)
            log("GPU config: Using CPU (no CUDA device found)")
    except ImportError:
        # PyTorch not installed, fall back to CPU
        msg = "[translate] Using CPU (PyTorch not available for GPU detection)"
        print(msg, file=sys.stderr)
        log("GPU config: Using CPU (PyTorch not available for GPU detection)")
    except Exception as e:
        # Any other error, fall back to CPU
        msg = f"[translate] Using CPU (error during GPU detection: {e})"
        print(msg, file=sys.stderr)
        log(f"GPU config: Using CPU (error during GPU detection: {e})")

    os.environ["ARGOS_DEVICE_TYPE"] = device_type
    log(f"GPU config: Set ARGOS_DEVICE_TYPE={device_type}")

    return device_type


# Valid ctranslate2 compute_type values. 'auto' lets ctranslate2 pick best
# for the hardware. 'int8' / 'int8_float32' speed up CPU inference 2-4x at
# minimal quality cost. 'float16' is GPU-only.
_VALID_COMPUTE_TYPES = {
    "default", "auto", "int8", "int8_float32", "int8_float16",
    "int16", "float16", "bfloat16", "float32",
}


def setup_compute_type(debug_log_func=None):
    """
    Validate the ARGOS_COMPUTE_TYPE env var and let argostranslate consume
    it natively (argostranslate >= 1.11 reads it via settings.get_setting()).

    Must be called BEFORE argostranslate is imported. If the value is not in
    the supported set, the env var is removed so argostranslate falls back
    to its own default ('auto'). This prevents ctranslate2 from raising
    "Invalid compute type" deep inside the translate path.

    No env var → no-op (argostranslate keeps 'auto').

    Returns:
        str | None: validated compute type left in env, or None if cleared/unset.
    """
    def log(msg):
        if debug_log_func:
            debug_log_func(msg)

    requested = os.environ.get("ARGOS_COMPUTE_TYPE")
    if not requested:
        return None

    if requested not in _VALID_COMPUTE_TYPES:
        msg = (f"[translate] Ignoring invalid ARGOS_COMPUTE_TYPE={requested!r} "
               f"(valid: {sorted(_VALID_COMPUTE_TYPES)}); falling back to 'auto'")
        print(msg, file=sys.stderr)
        log(msg)
        del os.environ["ARGOS_COMPUTE_TYPE"]
        return None

    msg = f"[translate] Quantization: compute_type={requested}"
    print(msg, file=sys.stderr)
    log(f"Compute type config: ARGOS_COMPUTE_TYPE={requested}")
    return requested
