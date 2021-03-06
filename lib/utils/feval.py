#!/usr/bin/env python

# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
#
# --------------------------------------------------------

import datasets.imdb
from utils.cython_bbox import bbox_overlaps
import numpy as np

DEBUG = True

def proposal_recall(imdb, proposals, num, threds=0.5):
	"""
	Get recall with numbers of rpn proposals
	"""
	roidb = imdb.gt_roidb()
	num_images = len(roidb)

	if DEBUG:
		print "{} images are involved in evaluation.".format(num_images)

	num_match = np.zeros((num,1),dtype=np.float32)
	num_gt = np.zeros((num,1),dtype=np.float32)
	print num_images

	for i in xrange(num_images):
		gt_boxes = roidb[i]['boxes'].copy()
		gt_classes =  roidb[i]['gt_classes'].copy()
		for j in xrange(num):
			kind = np.where(gt_classes ==(j+1))[0]
			matches = _match(proposals[i][j],gt_boxes[kind,:],threds)
			num_match[j] += matches
			num_gt[j]    += len(kind)

	#print num_match
	#print num_gt
	print num_match/num_gt


def _match(pr_rois,gt_rois,threds):

	# overlaps between the proposals and the gt boxes
    # overlaps (pr, gt)

    overlaps = bbox_overlaps(
    np.ascontiguousarray(pr_rois, dtype=np.float),
    np.ascontiguousarray(gt_rois, dtype=np.float))

    gt_argmax_overlaps = overlaps.argmax(axis=0) # ind of anchors
    gt_max_overlaps = overlaps[gt_argmax_overlaps,
                               np.arange(overlaps.shape[1])] # overlap of each groud truth

    # print gt_max_overlaps
    assert(len(gt_max_overlaps) == gt_rois.shape[0])

    num_match = np.sum(gt_max_overlaps >= threds)

    return num_match





