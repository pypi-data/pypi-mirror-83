# dask_k8

Create Dask clusters in Kubernetes easily.

The aim of this package is to be able to start a Dask client from _outside_ of a Kubernetes cluster
connecting to a Dask scheduler/workers running _inside_ of a Kubernetes cluster.

The dashboard of the dask scheduler running inside Kubernetes is accessible, the corresponding url is printed after the cluster creation.

First ensure you have proper Kubernetes access, try running `kubectl get pods` for instance.

### Installation

```
pip install dask_k8
```

### Example usage

```python
from dask_k8 import DaskCluster

# Use a kubernetes namespace where you have the proper rights, the cluster_id is to distinguish between possible different clusters
cluster = DaskCluster(namespace="dhlab", cluster_id="seguin-0")

# Initialize cluster
cluster.create()
# Get a dask.distributed.Client
dask_client = cluster.make_dask_client()
# Increase/decrease the number of workers
cluster.scale(40, blocking=True)  # Will block until all the workers are effectively connected to the scheduler

# Do the computation
dask_client.compute(...)

# IMPORTANT: Release the kubernetes resources, it is not done automatically
cluster.close()
```

In order not to forget to release the resources, the following can be done:
```python
from dask_k8 import DaskCluster
from dask.diagnostics import progress
from dask.distributed import wait

cluster = DaskCluster(namespace="dhlab", cluster_id="seguin-0")

with cluster:
    dask_client = cluster.make_dask_client()  # Waits for the scheduler to be started
    cluster.scale(40)  # Waits for the workers to be started
    # Compute
    dask_client.compute(..., sync=True)
    # Or
    future = dask_client.compute(...)
    progress(future)
    wait(future)
```

The corresponding output is:
```
Scheduler: tcp://10.90.47.7:31791
Dashboard: http://10.90.47.7:7062
Could not connect to scheduler, retrying...
Could not connect to scheduler, retrying...
Currently 0 workers out of the 40 required, waiting...
Currently 13 workers out of the 40 required, waiting...
Currently 21 workers out of the 40 required, waiting...
Currently 32 workers out of the 40 required, waiting...
Currently 33 workers out of the 40 required, waiting...
Currently 33 workers out of the 40 required, waiting...
Currently 34 workers out of the 40 required, waiting...
Reached the desired 40 workers!
```

### Specifying the workers/scheduler specifications

Arbitrary pod specification can be given both for the scheduler and the worker.
```python
from dask_k8 import DaskCluster

cluster = DaskCluster(namespace="dhlab", cluster_id="seguin-0", worker_pod_spec="""
  containers:
    - image: daskdev/dask:latest
      args: [dask-worker, $(DASK_SCHEDULER_ADDRESS), --nthreads, '1', --no-bokeh, --memory-limit, 4GB, --death-timeout, '60']
      imagePullPolicy: Always
      name: dask-worker
      env:
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: EXTRA_PIP_PACKAGES
          value: s3fs
        - name: EXTRA_CONDA_PACKAGES
          value:
      resources:
        requests:
          cpu: 1
          memory: "4G"
        limits:
          cpu: 1
          memory: "4G"
""")
```

### How does it work?

- Kubernetes services are started to connect the dask scheduler and its dashboard to the outside of the Kubernetes cluster. They can be seen
with `kubectl get svc` when `DaskCluster` is running (after calling `.create()`).
- Two Kubernetes deployments are created, one for the scheduler and one for the workers. They can be seen with `kubectl get deployments`.
- The corresponding pods are automatically managed by Kubernetes and their states can be seen with `kubectl get pods`.

## Project

The 'impresso - Media Monitoring of the Past' project is funded by the Swiss National Science Foundation (SNSF) under grant number [CRSII5_173719](http://p3.snf.ch/project-173719) (Sinergia program). The project aims at developing tools to process and explore large-scale collections of historical newspapers, and at studying the impact of this new tooling on historical research practices. More information at https://impresso-project.ch.

## License

Copyright (C) 2020  The *impresso* team. Contributors to this program include: [Benoit Seguin](https://github.com/SeguinBe).

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See the [GNU Affero General Public License](https://github.com/impresso/dask_k8/blob/master/LICENSE) for more details.
