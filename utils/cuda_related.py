import importlib.util
import subprocess
import sys
from pathlib import Path

import torch
from packaging.version import Version
from torch.utils.cpp_extension import CUDA_HOME


def parse(version: str) -> Version:
    """Parse the given version string.

    >>> parse('1.0.dev1')
    <Version('1.0.dev1')>

    :param version: The version string to parse.
    :raises InvalidVersion: When the version string is not a valid version.
    """
    return Version(version)


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


ROOT_DIR = Path(__file__).resolve().parent
envs = load_module_from_path("envs", ROOT_DIR.joinpath("vllm/envs.py"))

VLLM_TARGET_DEVICE = envs.VLLM_TARGET_DEVICE


def get_nvcc_cuda_version() -> Version:
    """Get the CUDA version from nvcc.

    Adapted from https://github.com/NVIDIA/apex/blob/8b7a1ff183741dd8f9b87e7bafd04cfde99cea28/setup.py
    """
    nvcc_output = subprocess.check_output(
        [CUDA_HOME + "/bin/nvcc", "-V"], universal_newlines=True
    )
    output = nvcc_output.split()
    release_idx = output.index("release") + 1
    nvcc_cuda_version = parse(output[release_idx].split(",")[0])
    return nvcc_cuda_version


def _is_cuda() -> bool:
    has_cuda = torch.version.cuda is not None
    return VLLM_TARGET_DEVICE == "cuda" and has_cuda


if __name__ == "__main__":
    if _is_cuda() and get_nvcc_cuda_version() >= Version("11.2"):
        pass
