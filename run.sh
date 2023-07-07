python detect.py \
    --source videos/360p/gwanak_05_360p.mp4 \
    --weights yolov7-w6-face_resol1280.pt \
    --img-size 1280 1280 \
    --conf-thres 0.0001 \
    --iou-thres 0.001 \
    --project runs/yolov7-w6-face_resol1280/final \
    --device 0