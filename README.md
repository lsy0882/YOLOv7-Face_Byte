# YOLOv7-Face_Byte
<br>

## Notification
* 라이센스 문제로 인해, 본 코드에 대한 상업적인 사용은 불가함.
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
pip install -r requirements.txt
```
<br>

### 2. 가상환경 내 모델 설정 방법
```shell
cd ~/YOLOv7-Face_Byte/

# vim 또는 vi 등 편집기를 이용해서 run.sh 내용을 기호에 맞게 수정함.
vim run.sh

# 아래는 run.sh 내 arguments에 대한 설명임.
python detect.py \
    --source videos/360p/gwanak_05_360p.mp4 \ # 모델에 입력할 영상 데이터 경로
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
