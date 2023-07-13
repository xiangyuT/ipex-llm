export IMAGE_NAME=xiangyut/test-image
export IMAGE_VERSION=bigdl-aa-0712

sudo docker build \
    --build-arg http_proxy=http://child-prc.intel.com:913 \
    --build-arg https_proxy=http://child-prc.intel.com:913 \
    -t $IMAGE_NAME:$IMAGE_VERSION -f ./Dockerfile .