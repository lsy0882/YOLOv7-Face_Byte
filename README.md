# YOLOv7-Face_Byte
<br>

## Notification
* 라이센스 문제로 인해, 본 코드에 대한 상업적인 사용은 불가함.
* 본 시스템은 GPU를 이용한 구동에 최적화 되어있음.
<br>

## Google drive
* 링크: https://drive.google.com/drive/folders/1STAohMO5NEK2vYcPYx3nm4Uq08MiUkbv?usp=sharing
* 모델관련 안내
    * 상기 링크 내 "YOLOv7-Face_Byte / Weight 파일" 폴더에서 "yolov7-w6-face_resol1280.pt", "yolov7s-face_resol640.pt" 다운로드 (이름 변경 X)
    * 다운로드 완료한 .pt 파일을 git clone 한 폴더(YOLOv7-Face_Byte)에 저장.
* 데모에 쓰인 원본 영상 안내
    * 상기 링크 내 "원본 영상" 폴더 속 영상 파일들 다운로드해서 활용
* 대표 데모영상 (gwanak_05_360p_yolov7-w6-face.gif)
<br>
[![Video Label](http://img.youtube.com/vi/Pt3AtdnqhZM/0.jpg)](https://youtu.be/Pt3AtdnqhZM)
<br>
{% include video id="Pt3AtdnqhZM" provider="youtube" %}

<br>

## 입력 영상 요구사항
* 해상도
  * 가능 해상도: 360p, 480p, 720p, 1080p, 4k 
  * 최적 해상도: 360p
* FPS
  * 가능 FPS: 10 fps, 20 fps, 30 fps
  * 최적 FPS: 30 fps
<br>

## Inference time table
* 실험환경
    * CPU: Intel(R) Core(TM) i9-10920X CPU @ 3.50GHz * 1ea (core : 12, Thread : 24)
    * GPU: RTX3090 x 1ea

* yolo7s 모델 실험결과 (최소 fps / 평균 fps / 최대 fps)

| video(30fps) | params |    360p-cpu    |        360p-gpu         |   480p-cpu    |        480p-gpu         |   1080p-cpu    |       1080p-gpu        |    4k-cpu     |         4k-gpu         |
|:------------:|:------:|:--------------:|:-----------------------:|:-------------:|:-----------------------:|:--------------:|:----------------------:|:-------------:|:----------------------:|
|   aihub_02   | 8.47M  | 6.5/17.4/20.2  | 35.6/81.3/89.4 (367% ↑) | 6.2/15.0/19.7 | 44.1/78.4/88.6 (423% ↑) | 3.6/13.7/20.3  | 39.4/73.7/78.0(438% ↑) |               |                        |
|  gwanak_05   | 8.47M  | 11.5/17.2/21.8 | 41.5/78.5/85.3 (356% ↑) | 6.9/17.3/20.2 | 61.7/77.8/84.6 (350% ↑) | 10.1/15.6/20.7 | 36.6/74.1/80.3(375% ↑) |               |                        |
|     23-1     | 8.47M  |                |                         |               |                         |                |                        | 7.0/14.3/18.4 | 40.7/61.7/78.8(311% ↑) |
|     21-1     | 8.47M  |                |                         |               |                         |                |                        | 6.6/13.7/17.9 | 41.0/60.9/76.9(345% ↑) | 
* yolo7-w6-tta 모델 실험결과 (최소 fps / 평균 fps / 최대 fps)

| video(30fps) | params |  360p-cpu   |        360p-gpu         |  480p-cpu   |        480p-gpu         |  1080p-cpu  |        1080p-gpu        |   4k-cpu    |         4k-gpu          |
|:------------:|:------:|:-----------:|:-----------------------:|:-----------:|:-----------------------:|:-----------:|:-----------------------:|:-----------:|:-----------------------:|
|   aihub_02   | 133.2M | 1.0/1.7/2.1 | 7.1/50.0/59.5 (2841% ↑) | 1.0/1.8/2.1 | 6.8/49.5/59.1 (2650% ↑) | 1.0/1.8/2.2 | 5.1/48.2/58.9 (2578% ↑) |             |                         |
|  gwanak_05   | 133.2M | 1.0/1.7/2.0 | 7.2/49.0/61.9 (2782% ↑) | 1.0/1.8/2.1 | 7.0/48.5/60.8 (2594% ↑) | 1.0/1.8/2.2 | 6.5/48.2/59.2 (2578% ↑) |             |                         |
|     23-1     | 133.2M |             |                         |             |                         |             |                         | 1.2/1.8/2.4 | 27.1/55.2/61.3(2967% ↑) |
|     21-1     | 133.2M |             |                         |             |                         |             |                         | 1.1/1.8/2.3 | 30.8/54.4/57.5(2922% ↑) | 
<br>

## Guide
### 1. git clone 및 conda 가상환경 설정
* git, conda 설치 및 설정이 완료된 상황임을 가정하여 작성함.
```shell
# git clone
cd ~
git clone https://github.com/lsy0882/YOLOv7-Face_Byte.git

# conda 가상환경 생성
conda create -n yolov7-face_byte python=3.9

# conda 가상환경 활성화
conda activate yolov7-face_byte

# conda 내 pip 패키지 설치
cd YOLOv7-Face_Byte
pip install -r requirements.txt
pip install Cython
pip install cython_bbox
pip install lap
```
<br>

### 2. 가상환경 내 모델 설정 방법
```shell
# vim 또는 vi 등 편집기를 이용해서 run.sh 내용을 기호에 맞게 수정함.
vim run.sh

# 아래는 run.sh 내 arguments에 대한 설명임.
python detect.py \
    --source videos/gwanak_05_360p.mp4 \ # 모델에 입력할 영상 데이터 경로
    --weights yolov7-w6-face_resol1280.pt \ # 딥러닝 모델의 weights 파일. yolov7-w6-face_resol1280.pt 또는 yolov7s-face_resol640.pt로 설정
    --img-size 1280 1280 \ # yolov7-w6-face_resol1280.pt는 1280 1280으로 설정, yolov7s-face_resol640.pt는 640 640으로 설정
    --conf-thres 0.0001 \ # detect한 face 객체의 신뢰점수 임계값. 낮을수록 다양하지만 정확도 낮은 객체 검출
    --iou-thres 0.001 \ # face 객체의 box 정확도 관련 임계값. 낮을수록 다양하지만 정확도 낮은 box 검출
    --project runs/yolov7-w6-face_resol1280/final \ # 결과를 저장한 경로
    --device 0 # cpu 라고 적으면 cpu로 동작, 0, 1, ..., n으로 적으면 0번째, 1번째, ..., n번째 GPU로 동작
```
<br>

### 3. 가상환경 내 모델 실행 방법
* 앞선 "2. 가상환경 내 모델 설정 방법"을 통해 설정이 완료된 상황임을 가정하여 작성함.
```
cd ~/YOLOv7-Face_Byte/
sh run.sh
```
<br>

## P.S.
* git, conda 설치 및 설정 / 가상환경 내 패키치 설정 / sh 파일 내 arguments 설명 / 오류 해결법 등 궁금한 사항이 있으시다면 아래 연락처로 연락주시기 바랍니다.
    * 제작자: 이상윤
    * 소속: 서강대학교 IIPLAB
    * 지도교수: 박형민 교수님
    * 연락처: +82-010-3354-0882
    * 이메일: leesy0882@gmail.com
