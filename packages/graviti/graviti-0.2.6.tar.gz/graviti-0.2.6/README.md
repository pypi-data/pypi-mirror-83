# Graviti python SDK

## Installation

```bash
pip3 install graviti
```

## Usage

#### Get accessKey

AccessKey is required when upload data.

Use your username and password to login to [Graviti website](https://gas.graviti.cn/),
and get accessKey on profile page.

#### Upload data

This sample is for uploading dataset which only contains data collected from a single sensor.

```python
#!/usr/bin/env python3

from graviti import GAS

ACCESS_KEY = "Accesskey-****"
DATASET_NAME = "TestDataset"
SEGMENT_NAME = "segment1"

gas = GAS(ACCESS_KEY)

dataset = gas.get_or_create_dataset(DATASET_NAME)  # create dataset
segment = dataset.get_or_create_segment(SEGMENT_NAME)  # create segment

# single-thread upload
for filename in FILE_LIST:
    segment.upload_data(filename, "remote_path")
# 'remote_path' should follow linux style. If it has wrong format, raise GASPathError.

# # multi-thread uploading
# # when use multi-thread uploading
# # uncomment the following code and comment single-thread uploading code

# from concurrent.futures import ThreadPoolExecutor

# THREAD_NUM = 8 # number of threads

# with ThreadPoolExecutor(THREAD_NUM) as executor:
#     for filename in FILE_LIST:
#         executor.submit(segment.upload_data, filename, "remote_path")
```

#### Upload fusion data

This sample is for uploading dataset which contains data collected from fusion.

```python
#!/usr/bin/env python3

from graviti import GAS
from graviti.dataset import Frame, Data
from graviti.sensor import Camera

ACCESS_KEY = "Accesskey-****"
DATASET_NAME = "TestFusionDataset"
SEGMENT_NAME = "segment1"

gas = GAS(ACCESS_KEY)

dataset = gas.get_or_create_fusion_dataset(DATASET_NAME)  # create fusion dataset
segment = dataset.get_or_create_segment(SEGMENT_NAME)  # create segment

for sensor_name in SENSOR_LIST:
    camera = Camera(sensor_name)
    camera.description = "This is a camera"
    camera.set_translation(x=1.1, y=2.2, z=3.3)
    camera.set_rotation(w=1.1, x=2.2, y=3.3, z=4.4)
    camera.set_camera_matrix(fx=1.1, fy=2.2, cx=3.3, cy=4.4)
    camera.set_distortion_coefficients(p1=1.1, p2=2.2, k1=3.3, k2=4.4, k3=5.5)

    segment.upload_sensor_object(camera)

# single-thread uploading
for index, frame_info in enumerate(FRAME_LIST):
    frame = Frame()
    for sensor_name in SENSOR_LIST:
        frame[sensor_name] = Data(
            frame_info.filename, remote_path="remote_path", timestamp=frame_info.timestamp,
        )
    # 'remote_path' should follow linux style. If it has wrong format, raise GASPathError.
    segment.upload_frame_object(frame, index)

# # multi-thread uploading
# # when use multi-thread uploading
# # uncomment the following code and comment single-thread uploading code

# from concurrent.futures import ThreadPoolExecutor

# THREAD_NUM = 8  # number of threads

# with ThreadPoolExecutor(THREAD_NUM) as executor:
# for index, frame_info in enumerate(FRAME_LIST):
#     frame = Frame()
#     for sensor_name in SENSOR_LIST:
#         frame[sensor_name] = Data(
#             frame_info.filename, remote_path="remote_path", timestamp=frame_info.timestamp,
#         )
#         executor.submit(segment.upload_frame_object, frame, index)
```

#### Command line

We also provide `gas` command to call SDK APIs.

Use `gas` in terminal to see the available commands as follows.

```bash
gas config
gas create
gas delete
gas publish
gas ls
gas cp
gas rm
```

##### config environment

```bash
gas config [accessKey]                   # config accesskey to default environment
gas -c [config_name] config [accessKey]  # create an environment named [config_name]
                                         # and config accesskey to it
```

##### show config

```bash
gas config         # show config information of all environments
```

##### choose environment

```bash
gas [command] [args]                           # choose default environment
gas -c [config_name] [command] [args]          # choose the environment named [config_name]
gas -k [accessKey] [command] [args]            # appoint accessKey in current command line

# '-k' has higher priority than '-c'
```

##### create dataset

```bash
gas create tb:[dataset_name]
```

##### delete dataset

```bash
gas delete tb:[dataset_name]
```

##### publish dataset

```bash
gas publish tb:[dataset_name]
```

##### list data

```bash
gas ls [Options] [tbrn]

Options:
  -a, --all      List all files under all segments. Only works when [tbrn] is tb:[dataset_name].

tbrn:
  None                                              # list all dataset names
  tb:[dataset_name]                                 # list all segment names under the dataset
  tb:[dataset_name]:[segment_name]                  # list all files under the segment
  tb:[dataset_name]:[segment_name]://[remote_path]  # list files under the remote path
```

##### upload data

```bash
gas cp [Options] [local_path1] [local_path2]... [tbrn]

Options:
  -r, --recursive     Copy directories recursively.
  -j, --jobs INTEGER  The number of threads.

tbrn:
  tb:[dataset_name]:[segment_name]                  # copy files to the segment
  tb:[dataset_name]:[segment_name]://[remote_path]  # copy files to the remote path

# [segment_name] is must required.
# If only upload one file and [remote_path] doesn't end with '/',
# then the file will be uploaded and renamed as [remote_path]
```

##### delete data

```bash
gas rm [Options] [tbrn]

Options:
  -r, --recursive  Remove directories recursively.
  -f, --force      Delete segments forcibly regardless of the nature of the dataset.
                   By default, only segments with no sensor can be deleted.
                   Once '-f' is used, sensors along with their objects will also be deleted.

tbrn:
  tb:[dataset_name]                                 # remove all segments under the dataset
  tb:[dataset_name]:[segment_name]                  # remove a segment
  tb:[dataset_name]:[segment_name]://[remote_path]  # remove files under the remote path
```
