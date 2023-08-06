#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

MAJOR = 0
MINOR = 0
PATCH = 1
PRE_RELEASE = 'dev4'
# Use the following formatting: (major, minor, patch, prerelease)
VERSION = (MAJOR, MINOR, PATCH, PRE_RELEASE)

__shortversion__ = '.'.join(map(str, VERSION[:3]))
__version__ = '.'.join(map(str, VERSION[:3])) + "%s" % ''.join(VERSION[3:])

__contact_names__ = 'Jonathan Dekhtiar'
__contact_emails__ = 'jdekhtiar@nvidia.com'
__homepage__ = 'https://github.com/NVIDIA'
__repository_url__ = 'https://github.com/NVIDIA'
__download_url__ = 'https://github.com/NVIDIA'
__description__ = 'A fake package to warn the user he is not installing the ' \
                  'correct package.'
__license__ = 'Apache2'
__keywords__ = 'nvidia, deep learning, machine learning, supervised learning,'
__keywords__ += 'unsupervised learning, reinforcement learning, logging'

__faked_packages__ = [
    # Format
    # (package_name, readme_filename, error_filename),

    # Test Package
    ("nvidia-pyindex-test-pkg", None, None),  # Do not remove - @DEKHTIARJonathan

    # DL Frameworks
    ("nvidia-tensorflow", None, None),
    ("nvidia-pytorch", None, None),
    ("nvidia-torch", None, None),
    ("nvidia-torchvision", None, None),
    ("nvidia-mxnet", None, None),

    # TensorRT owned packages - Ask @Eric Work before doing any change
    ("nvidia-tensorrt", "tensorrt.rst", "tensorrt.txt"),
    ("graphsurgeon", "tensorrt.rst", "tensorrt.txt"),
    ("onnx-graphsurgeon", "tensorrt.rst", "tensorrt.txt"),
    ("polygraphy", "tensorrt.rst", "tensorrt.txt"),
    ("uff", "tensorrt.rst", "tensorrt.txt"),

    # TF additional libraries
    ("nvidia-tensorflow-estimator", None, None),
    ("nvidia-horovod", None, None),

    # Triton Library - Ask @David Goodwin or @David Zier before doing any change
    ("tritonclient", "tritonclient.rst", "tritonclient.txt"),

    # DALI public wheels - Ask @Janusz Lisiecki before doing any change
    ("nvidia-dali", "dali.rst", "dali.txt"),
    ("nvidia-dali-cuda90", "dali.rst", "dali.txt"),
    ("nvidia-dali-cuda91", "dali.rst", "dali.txt"),
    ("nvidia-dali-cuda92", "dali.rst", "dali.txt"),
    ("nvidia-dali-cuda100", "dali.rst", "dali.txt"),
    ("nvidia-dali-cuda101", "dali.rst", "dali.txt"),
    ("nvidia-dali-cuda102", "dali.rst", "dali.txt"),
    ("nvidia-dali-cuda110", "dali.rst", "dali.txt"),
    ("nvidia-dali-cuda111", "dali.rst", "dali.txt"),

    ("nvidia-dali-tf-plugin", "dali.rst", "dali.txt"),
    ("nvidia-dali-tf-plugin-cuda90", "dali.rst", "dali.txt"),
    ("nvidia-dali-tf-plugin-cuda91", "dali.rst", "dali.txt"),
    ("nvidia-dali-tf-plugin-cuda92", "dali.rst", "dali.txt"),
    ("nvidia-dali-tf-plugin-cuda100", "dali.rst", "dali.txt"),
    ("nvidia-dali-tf-plugin-cuda101", "dali.rst", "dali.txt"),
    ("nvidia-dali-tf-plugin-cuda102", "dali.rst", "dali.txt"),
    ("nvidia-dali-tf-plugin-cuda110", "dali.rst", "dali.txt"),
    ("nvidia-dali-tf-plugin-cuda111", "dali.rst", "dali.txt"),

    # DALI TF Plugin wheel used by `nvidia-tensorflow`
    ("nvidia-dali-nvtf-plugin", None, None),

    # DLProf - ask @David Zier before doing any change
    ("nvidia-dlprof", None, None),
    ("nvidia-tensorboard-plugin-dlprof", None, None),
    ("nvidia-tensorboard", None, None),

    # EFF - ask @Tomasz Kornuta before doing any change
    ("nvidia-eff", None, "eff.txt"),

    # CUDA-X Libraries
    ("nvidia-cublas", None, None),
    ("nvidia-cuda-cupti", None, None),
    ("nvidia-cuda-nvcc", None, None),
    ("nvidia-cuda-nvrtc", None, None),
    ("nvidia-cuda-runtime", None, None),
    ("nvidia-cuda-sanitizer-api", None, None),
    ("nvidia-cudnn", None, None),
    ("nvidia-cufft", None, None),
    ("nvidia-curand", None, None),
    ("nvidia-cusolver", None, None),
    ("nvidia-cusparse", None, None),
    ("nvidia-nccl", None, None),
    ("nvidia-npp", None, None),
    ("nvidia-nsys", None, None),
    ("nvidia-nsys-cli", None, None),
    ("nvidia-nvjpeg", None, None),
    ("nvidia-nvml-dev", None, None),
    ("nvidia-nvtx", None, None),
]

