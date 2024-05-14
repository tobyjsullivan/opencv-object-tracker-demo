# Downloading models

Only the `kcf` (default) and `csrt` trackers will work out of the box. For the others, download models from the following sources. Place the downloaded models in the appropriate directories under `data/`.

For GOTURN:

- goturn.prototxt and goturn.caffemodel: https://github.com/opencv/opencv_extra/tree/c4219d5eb3105ed8e634278fad312a1a8d2c182d/testdata/tracking

For DaSiamRPN:

- network: https://www.dropbox.com/s/rr1lk9355vzolqv/dasiamrpn_model.onnx?dl=0
- kernel_r1: https://www.dropbox.com/s/999cqx5zrfi7w4p/dasiamrpn_kernel_r1.onnx?dl=0
- kernel_cls1: https://www.dropbox.com/s/qvmtszx5h339a0w/dasiamrpn_kernel_cls1.onnx?dl=0

For NanoTrack:

- nanotrack_backbone: https://github.com/HonglinChu/SiamTrackers/blob/master/NanoTrack/models/nanotrackv2/nanotrack_backbone_sim.onnx
- nanotrack_headneck: https://github.com/HonglinChu/SiamTrackers/blob/master/NanoTrack/models/nanotrackv2/nanotrack_head_sim.onnx

Original source: https://github.com/opencv/opencv/blob/03507e06b40450244a0489abba8e989d9b337d18/samples/python/tracker.py
