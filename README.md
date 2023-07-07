# YOLOv7-Face_Byte
<br>

## Notification
* 라이센스 문제로 인해, 본 코드에 대한 상업적인 사용은 불가함.
* 다양한 환경에서도 Opencv-GPU를 사용하기 위해 Docker image를 제작함.
<br>

## Guide
### 1. Docker 이미지 다운로드 및 컨테이너 생성 방법
* 도커 설치 및 설정이 완료된 상황임을 가정하여 작성함.
```shell
# 이미지 다운로드
docker pull lsy0882/yunet_byte:ubuntu20.04_cuda11.7.1_cudnn8_v1.0.0

# 컨테이너 생성
docker run --gpus all -it -d --name yunet_byte lsy0882/yunet_byte:ubuntu20.04_cuda11.7.1_cudnn8_v1.0.0

# 컨테이너 접속
docker attach yunet_byte
```
<br>

### 2. 컨테이너 내 환경 설정모델 실행 방법
```shell
# 컨테이너 내 가상환경 활성화
workon opencv_dnn_cuda

# GPU compute capability 버전 확인 (1~n번째 줄에 출력된 숫자 0번 GPU ~ n-1번 GPU의 compute capability 버전)
# 만약 GPU compute capability 버전이 8.6이면, 
# 아래의 "OpenCV 다운로드", "OpenCV 설정"은 생략하고 "3. 컨테이너 내 모델 설정 방법"으로 넘어갈 것.
nvidia-smi --query-gpu=compute_cap --format=csv

# OpenCV 다운로드
cd ~
wget -O opencv-4.7.0.zip https://github.com/opencv/opencv/archive/4.7.0.zip
unzip -q opencv-4.7.0.zip
mv opencv-4.7.0 opencv
rm -f opencv-4.7.0.zip

wget -O opencv_contrib-4.7.0.zip https://github.com/opencv/opencv_contrib/archive/4.7.0.zip
unzip -q opencv_contrib-4.7.0.zip
mv opencv_contrib-4.7.0 opencv_contrib
rm -f opencv_contrib-4.7.0.zip

# OpenCV 설정
cd ~/opencv
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D INSTALL_PYTHON_EXAMPLES=ON \
  -D INSTALL_C_EXAMPLES=OFF \
  -D OPENCV_ENABLE_NONFREE=ON \
  -D WITH_CUDA=ON \
  -D WITH_CUDNN=ON \
  -D OPENCV_DNN_CUDA=ON \
  -D ENABLE_FAST_MATH=1 \
  -D CUDA_FAST_MATH=1 \
  -D CUDA_ARCH_BIN=0.0 \ # (중요) 이 값은, 앞서 확인한 GPU compute capability 버전값으로 입력해야함.
  -D WITH_CUBLAS=1 \
  -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
  -D HAVE_opencv_python3=ON \
  -D PYTHON_EXECUTABLE=~/.virtualenvs/opencv_dnn_cuda/bin/python \
  -D PYTHON3_PACKAGE_PATH=~/.virtualenvs/opencv_dnn_cuda/lib/python3.8/site-packages \
  -D BUILD_EXAMPLES=ON ..

make -j$(nproc)
make install
ldconfig
```
<br>

### 3. 컨테이너 내 모델 설정 방법
* 모델에 입력할 영상 데이터를 컨테이너로 옮긴 상황임을 가정하여 작성함.
```shell
cd ~/YuNet_Byte/

# vim 또는 vi 등 편집기를 이용해서 setting.yml 내용을 기호에 맞게 수정함.
vim setting.yml
```
```yaml
# 아래는 setting.yml 내 파라미터에 대한 설명임.
main:
  backend_target: 1 # 0: [OpenCV Imp, CPU], 1: [CUDA, GPU(CUDA FP32)] || 0은 CPU로 동작, 1은 GPU로 동작
  video_file_path: /root/YuNet_Byte/videos/4k/23-1_cam01_assault01_place02_night_spring.mp4 # 모델에 입력할 영상 데이터 경로

object_detecting:
  detector_name: face_detection_yunet_2022mar.onnx # Detector weight 파일. 변경 X
  conf_threshold: 0.1 # detect한 face 객체의 신뢰점수 임계값. 낮을수록 다양하지만 정확도 낮은 객체 검출
  nms_threshold: 0.3 # face 객체의 box 정확도 관련 임계값. 낮을수록 다양하지만 정확도 낮은 box 검출
  top_k: 5000 # nms하기 전 box 후보군 개수 설정값. 변경 X

object_tracking:
  score_threshold: 0.1 # 변경 X
  track_threshold: 0.5 # tracking 관련 설정값. 변경 X
  track_buffer: 150 # tracker의 결과를 유지하는 설정값. 변경 X
  match_threshold: 0.8 # kalman filter가 예측한 위치와 실제 검출 위치간의 유사성 계산관련 설정값. 변경 X
  min_box_area: 3 # 오검출을 줄이기위한 값.
  frame_rate: 30 # tracker의 결과를 유지하는 설정값. 변경 X
```
<br>

### 4. 컨테이너 내 모델 실행 방법
* 앞선 "3. 컨테이너 내 모델 설정 방법"을 통해 설정이 완료된 상황임을 가정하여 작성함.
```
cd ~/YuNet_Byte/
python demo.py
```
<br>

## P.S.
* 도커 설치 및 설정 / 이미지 다운로드 및 컨테이너 설정 / OpenCV 설정 등 궁금한 사항이 있으시다면 아래 연락처로 연락주시기 바랍니다.
  * 제작자: 이상윤
  * 소속: 서강대학교 IIPLAB
  * 지도교수: 박형민 교수님
  * 연락처: +82-010-3354-0882
  * 이메일: leesy0882@gmail.com
