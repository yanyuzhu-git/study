FROM registry.aps.datacanvas.com:5000/aps/module/base/datacanvas-aps:3.1.2

USER root

COPY gpu.tar .
RUN tar xf gpu.tar && \
    mv cuda.repo /etc/yum.repos.d/cuda.repo && \
    rm -f gpu.tar && \
    chmod a+x files/* && \
    mv files/* /

#===========add nvidia gpu support==================
RUN NVIDIA_GPGKEY_SUM=d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5 && \
    cat 7fa2af80.pub | sed '/^Version/d' > /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA && \
    echo "$NVIDIA_GPGKEY_SUM  /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA" | sha256sum -c --strict -

ENV CUDA_VERSION 9.0.176

ENV CUDA_PKG_VERSION 9-0-$CUDA_VERSION-1
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA
RUN yum clean all && \
    yum install -y cuda-cudart-$CUDA_PKG_VERSION && \
    ln -s cuda-9.0 /usr/local/cuda && \
    rm -rf /var/cache/yum/*

RUN yum install -y \
        cuda-libraries-$CUDA_PKG_VERSION \
        cuda-cublas-9-0-9.0.176.4-1 && \
    rm -rf /var/cache/yum/*

RUN yum install -y \
        cuda-libraries-dev-$CUDA_PKG_VERSION \
        cuda-nvml-dev-$CUDA_PKG_VERSION \
        cuda-minimal-build-$CUDA_PKG_VERSION \
        cuda-command-line-tools-$CUDA_PKG_VERSION \
        cuda-core-9-0-9.0.176.3-1 \
        cuda-cublas-dev-9-0-9.0.176.4-1 && \
    rm -rf /var/cache/yum/*

ENV CUDNN_VERSION 7.2.1.38
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=cf007437b9ac6250ec63b89c25f248d2597fdd01369c80146567f78e75ce4e37 && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-9.0-linux-x64-v7.2.1.38.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-9.0-linux-x64-v7.2.1.38.tgz -C /usr/local --wildcards 'cuda/lib64/libcudnn.so.*' && \
    rm cudnn-9.0-linux-x64-v7.2.1.38.tgz && \
    ldconfig

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES none
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=9.0"
#===========add tensorflow gpu support==================
LABEL com.datacanvas.aps.version="3.0.0" \
 com.datacanvas.aps.gpu.enabled="1"

RUN pip3 uninstall keras -y && \
     pip  uninstall keras -y && \
     pip3 uninstall tensorflow -y && \
     pip  uninstall tensorflow -y

RUN pip3 install nvidia-ml-py3 -i https://mirrors.aliyun.com/pypi/simple/

USER aps

