from functools import partial
from torch import torch
from pathlib import Path, PurePath
from .weights import get_path
import os

base_url = get_path.get_weights_dir()

def load_partial():

    url_path = 'mobilenet_v2-b0353104.pth'

    url = str(PurePath(base_url, url_path))

    partial_load = partial(torch.load, url)

    return partial_load


    

