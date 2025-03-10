"""Graphbolt."""
import os
import sys

import torch

from .._ffi import libinfo
from .base import *
from .minibatch import *
from .dataloader import *
from .dataset import *
from .feature_fetcher import *
from .feature_store import *
from .impl import *
from .itemset import *
from .item_sampler import *
from .negative_sampler import *
from .sampled_subgraph import *
from .subgraph_sampler import *
from .utils import (
    add_reverse_edges,
    unique_and_compact,
    unique_and_compact_node_pairs,
)


def load_graphbolt():
    """Load Graphbolt C++ library"""
    version = torch.__version__.split("+", maxsplit=1)[0]

    if sys.platform.startswith("linux"):
        basename = f"libgraphbolt_pytorch_{version}.so"
    elif sys.platform.startswith("darwin"):
        basename = f"libgraphbolt_pytorch_{version}.dylib"
    elif sys.platform.startswith("win"):
        basename = f"graphbolt_pytorch_{version}.dll"
    else:
        raise NotImplementedError("Unsupported system: %s" % sys.platform)

    dirname = os.path.dirname(libinfo.find_lib_path()[0])
    path = os.path.join(dirname, "graphbolt", basename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Cannot find DGL C++ graphbolt library at {path}"
        )

    try:
        torch.classes.load_library(path)
    except Exception:  # pylint: disable=W0703
        raise ImportError("Cannot load Graphbolt C++ library")


load_graphbolt()
