import numpy as np

from .kalman_filter import KalmanFilter
from .basetrack import TrackState
from .utils import *
from .STrack import STrack

import pdb

class BYTETracker():
    def __init__(self, params):
        self.tracked_stracks = []
        self.lost_stracks = []
        self.removed_stracks = []

        self.frame_id = 0

        self.match_thresh = params["match_threshold"]
        self.track_thresh = params["track_threshold"]
        self.det_thresh = self.track_thresh + 0.0002
        self.buffer_size = int(params["frame_rate"] / 30.0 * params["track_buffer"])
        self.max_time_lost = self.buffer_size
        self.kalman_filter = KalmanFilter()

    @staticmethod
    def det_to_trk_data_conversion(detection_result, frame_size):
        detection_result = detection_result
        boxes_tmp_list = []
        boxes_list = []
        scores_tmp_list = []
        scores_list = []
        for info_ in detection_result:
            detection_size = (info_[2] - info_[0]) * (info_[3] - info_[1])
            width_height_ratio = (info_[2] - info_[0]) / (info_[3] - info_[1])
            if detection_size < (frame_size / 25) and width_height_ratio < 2:
                boxes_tmp_list.append(info_[0]) # lt_x
                boxes_tmp_list.append(info_[1]) # lt_y
                boxes_tmp_list.append(info_[2]) # br_x
                boxes_tmp_list.append(info_[3]) # br_y
                scores_tmp_list.append(info_[4]) # score
                boxes_list.append(boxes_tmp_list)
                scores_list.append(scores_tmp_list)
                boxes_tmp_list = []
                scores_tmp_list = []
        boxes_list_array = np.array(boxes_list)
        scores_list_array = np.array(scores_list)

        return boxes_list_array, scores_list_array

    def update(self, detection_result, frame_size):
        bboxes, scores = self.det_to_trk_data_conversion(detection_result, frame_size)
        classes = np.zeros_like(scores)

        output = []
        self.frame_id += 1
        scores=scores.reshape(-1)
        classes=classes.reshape(-1) 

        tracked_stracks = []
        lost_stracks = []
        removed_stracks = [] 
        unconfirmed_stracks = []
        activated_starcks = []
        refind_stracks = [] 

        for track in self.tracked_stracks:
            if not track.is_activated:
                unconfirmed_stracks.append(track)
            else:
                tracked_stracks.append(track)
        strack_pool = joint_stracks(tracked_stracks, self.lost_stracks)
        
        is_human = classes == 0
        low_idxes_low_limit = 0.01 < scores
        low_idxes_high_limit = scores <= self.track_thresh
        det_low_idxes = np.logical_and(low_idxes_low_limit, low_idxes_high_limit)
        det_low_human_idxes = np.logical_and(det_low_idxes, is_human)
        det_high_idxes = scores > self.track_thresh
        det_high_human_idxes = np.logical_and(det_high_idxes, is_human)

        bboxes_high = bboxes[det_high_human_idxes]
        scores_high = scores[det_high_human_idxes]
        classes_high = classes[det_high_human_idxes]

        bboxes_low = bboxes[det_low_human_idxes]
        scores_low = scores[det_low_human_idxes]
        classes_low = classes[det_low_human_idxes]

        STrack.multi_predict(strack_pool)

        if len(bboxes_high) > 0:
            detections_high = [STrack(STrack.tlbr_to_tlwh(tlbr), s, cls) for (tlbr, s, cls) in zip(bboxes_high, scores_high, classes_high)]
        else:
            detections_high = []

        dists_first = matching.iou_distance(strack_pool, detections_high)
        dists_first = matching.fuse_score(dists_first, detections_high)
        matches_first, track_remain_idxes, detection_remain_idxes = matching.linear_assignment(dists_first, thresh=self.match_thresh)

        for track_idx, det_idx in matches_first:
            matched_track_high = strack_pool[track_idx]
            matched_det_high = detections_high[det_idx]
            if matched_track_high.state == TrackState.Tracked:
                matched_track_high.update(matched_det_high, self.frame_id)
                activated_starcks.append(matched_track_high)
            else:
                matched_track_high.re_activate(matched_det_high, self.frame_id, new_id=False)
                refind_stracks.append(matched_track_high)

        if len(bboxes_low) > 0:
            detections_low = [STrack(STrack.tlbr_to_tlwh(tlbr), s, cls) for (tlbr, s, cls) in zip(bboxes_low, scores_low, classes_low)]
        else:
            detections_low = []
        
        stracks_remain = [strack_pool[idx] for idx in track_remain_idxes if strack_pool[idx].state == TrackState.Tracked]
        dists_second = matching.iou_distance(stracks_remain, detections_low)
        matches_second, track_re_remain_idxes, detection_re_remain_idxes = matching.linear_assignment(dists_second, thresh=0.5)

        for track_idx, det_idx in matches_second:
            matched_track_remain = stracks_remain[track_idx]
            matched_det_low = detections_low[det_idx]
            if matched_track_remain.state == TrackState.Tracked:
                matched_track_remain.update(matched_det_low, self.frame_id)
                activated_starcks.append(matched_track_remain)
            else:
                matched_track_remain.re_activate(matched_det_low, self.frame_id, new_id=False)
                refind_stracks.append(matched_track_remain)

        for idx in track_re_remain_idxes:
            track_re_remain = stracks_remain[idx]
            if not track_re_remain.state == TrackState.Lost:
                track_re_remain.mark_lost()
                lost_stracks.append(track_re_remain)

        for track in self.lost_stracks:
            if self.frame_id - track.end_frame > self.max_time_lost:
                track.mark_removed()
                removed_stracks.append(track)

        detections_remain = [detections_high[idx] for idx in detection_remain_idxes]
        dists_unconfirm = matching.iou_distance(unconfirmed_stracks, detections_remain)
        dists_unconfirm = matching.fuse_score(dists_unconfirm, detections_remain)
        matches_begin, u_unconfirmed, u_detection = matching.linear_assignment(dists_unconfirm, thresh=0.7)

        for track_idx, det_idx in matches_begin:
            matched_track_begin = unconfirmed_stracks[track_idx]
            matched_det_begin = detections_remain[det_idx]
            matched_track_begin.update(matched_det_begin, self.frame_id)
            activated_starcks.append(matched_track_begin)

        for it in u_unconfirmed:
            track = unconfirmed_stracks[it]
            track.mark_removed()
            removed_stracks.append(track)

        for inew in u_detection:
            track = detections_remain[inew]
            if track.score < self.det_thresh:
                continue
            track.activate(self.kalman_filter, self.frame_id)
            activated_starcks.append(track)

        self.tracked_stracks = [t for t in self.tracked_stracks if t.state == TrackState.Tracked]
        self.tracked_stracks = joint_stracks(self.tracked_stracks, activated_starcks)
        self.tracked_stracks = joint_stracks(self.tracked_stracks, refind_stracks)
        self.lost_stracks = sub_stracks(self.lost_stracks, self.tracked_stracks)
        self.lost_stracks.extend(lost_stracks)
        self.lost_stracks = sub_stracks(self.lost_stracks, self.removed_stracks)
        self.removed_stracks.extend(removed_stracks)
        self.tracked_stracks, self.lost_stracks = remove_duplicate_stracks(self.tracked_stracks, self.lost_stracks)

        STrack.record_center_point(self.frame_id, self.tracked_stracks)
        STrack.record_acceleration(self.tracked_stracks)
        STrack.init_switch_action_state(self.tracked_stracks)
        STrack.init_overlap(self.tracked_stracks)
        STrack.check_overlap(self.tracked_stracks)
        
        output += self.tracked_stracks
        
        return output