FROM ubuntu:22.04

ARG http_proxy
ARG https_proxy

ENV LOCAL_IP                            127.0.0.1
ENV LC_ALL                              C.UTF-8
ENV LANG                                C.UTF-8

# Basic dependencies and DCAP
RUN apt update && \
    apt install -y build-essential apt-utils wget git && \
    mkdir -p /opt/intel/ && \
    cd /opt/intel && \ 
    wget https://download.01.org/intel-sgx/sgx-dcap/1.16/linux/distro/ubuntu22.04-server/sgx_linux_x64_sdk_2.19.100.3.bin && \
    chmod a+x ./sgx_linux_x64_sdk_2.19.100.3.bin && \
    printf "no\n/opt/intel\n"|./sgx_linux_x64_sdk_2.19.100.3.bin && \
    . /opt/intel/sgxsdk/environment && \
    cd /opt/intel && \
    wget https://download.01.org/intel-sgx/sgx-dcap/1.16/linux/distro/ubuntu22.04-server/sgx_debian_local_repo.tgz && \
    tar xzf sgx_debian_local_repo.tgz && \
    echo 'deb [trusted=yes arch=amd64] file:///opt/intel/sgx_debian_local_repo jammy main' | tee /etc/apt/sources.list.d/intel-sgx.list && \
    wget -qO - https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key | apt-key add - && \
    apt update && \
    apt install -y libsgx-enclave-common-dev libsgx-qe3-logic libsgx-pce-logic libsgx-ae-qe3 libsgx-ae-qve libsgx-urts libsgx-dcap-ql libsgx-dcap-default-qpl libsgx-dcap-quote-verify-dev libsgx-dcap-ql-dev libsgx-dcap-default-qpl-dev libsgx-quote-ex-dev libsgx-uae-service libsgx-ra-network libsgx-ra-uefi libtdx-attest libtdx-attest-dev 

# Python
RUN apt install -y python3-minimal && \
    apt install -y build-essential python3 python3-setuptools python3-dev python3-pip && \
    pip3 install --upgrade pip && \
    pip install setuptools==58.4.0 flask requests pyopenssl

# # BigDL Python Lib
# RUN mkdir /ppml && \
#     cd /ppml/ && \
#     git clone https://github.com/intel-analytics/BigDL.git && \
#     cd BigDL && \
#     mkdir -p /ppml/bigdl-ppml/ && \
#     cp -r /ppml/BigDL/python/ppml/src/ /ppml/bigdl-ppml && \
#     rm -rf /ppml/BigDL

ENV PYTHONPATH   /usr/lib/python3.9:/usr/lib/python3.9/lib-dynload:/usr/local/lib/python3.9/dist-packages:/usr/lib/python3/dist-packages:/ppml/bigdl-ppml/src

ADD ./bigdl-aa /ppml/bigdl-aa
ADD ./entrypoint.sh /ppml/entrypoint.sh
RUN chmod +x /ppml/entrypoint.sh

WORKDIR /ppml
ENTRYPOINT [ "/ppml/entrypoint.sh" ]
