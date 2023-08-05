'''
compute Precision, Recall, F-Score, VOC 2012 mAP, COCO AP, P-R Curve
Source : **https://github.com/rafaelpadilla/Object-Detection-Metrics**
         https://github.com/WongKinYiu/PyTorch_YOLOv4
         https://github.com/rbgirshick/py-faster-rcnn
         https://github.com/argusswift/YOLOv4-pytorch

author: xujing
date: 2020-10-19

'''
import os
import sys
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import random
import cv2
from tqdm import tqdm
# from scipy.interpolate import make_interp_spline
from decimal import *

from BoundingBox import *
from BoundingBoxes import *
from detutils import *


class DetMetric:
    def GetDetMetrics(self,
                    boundingboxes,
                    IOUThreshold=0.5,
                    beta = 1,
                    method=MethodAveragePrecision.COCOInterpolation,
                    getpredimg=False,
                    imgdir=None,
                    numerical=2):
        """Get the metrics used by the VOC Pascal 2012 challenge and COCO AP
        Source: https://github.com/rafaelpadilla/Object-Detection-Metrics
        Get
        Args:
            boundingboxes: Object of the class BoundingBoxes representing ground truth and detected
            bounding boxes;
            IOUThreshold: IOU threshold indicating which detections will be considered TP or FP
            (default value = 0.5);
            beta: F-beta score,(default = 1) ;
            method (default = MethodAveragePrecision.COCOInterpolated): It can be calculated as the implementation
            in the official COCO toolkit (101-PointInterpolation), or applying the 11-point
            interpolatio as described in the paper "The PASCAL Visual Object Classes(VOC) Challenge"
            or EveryPointInterpolation"  (ElevenPointInterpolation);
            getpredimg: Whether to generate prediction image, default is False;
            imgdir: image storage file, if `getpredimg` is True, this args. must be specified;
            numerical: numerical accuracy of drawing;
        Returns:
            A list of dictionaries. Each dictionary contains information and metrics of each class.
            The keys of each dictionary are:
            dict['class']: class representing the current dictionary;
            dict['precision']: array with the precision values;
            dict['recall']: array with the recall values;
            dict['AP']: average precision based on the map method,but this AP is not coco style AP, if your method=COCOInterpolatedAP,you should calculate the average for all categories,that is IOUThreshold's coco AP eg. COCO AP@50;
            dict['f-score']: F-score,default F1-score;
            dict['interpolated precision']: interpolated precision values;
            dict['interpolated recall']: interpolated recall values;
            dict['total positives']: total number of ground truth positives;
            dict['total TP']: total number of True Positive detections;
            dict['total FP']: total number of False Positive detections;
        """

        if getpredimg and (imgdir is None):
            raise "[detmet Error] You must specify a valid file path for image storage!!!"

        ret = []  # list containing metrics (precision, recall, average precision) of each class
        # List with all ground truths (Ex: [imageName,class,confidence=1, (bb coordinates XYX2Y2)])
        groundTruths = []
        # List with all detections (Ex: [imageName,class,confidence,(bb coordinates XYX2Y2)])
        detections = []
        # Get all classes
        classes = []
        # Loop through all bounding boxes and separate them into GTs and detections
        for bb in boundingboxes.getBoundingBoxes():
            # [imageName, class, confidence, (bb coordinates XYX2Y2)]
            if bb.getBBType() == BBType.GroundTruth:
                groundTruths.append([
                    bb.getImageName(),
                    bb.getClassId(), 1,
                    bb.getAbsoluteBoundingBox(BBFormat.XYX2Y2)
                ])
            else:
                detections.append([
                    bb.getImageName(),
                    bb.getClassId(),
                    bb.getConfidence(),
                    bb.getAbsoluteBoundingBox(BBFormat.XYX2Y2)
                ])
            # get class
            if bb.getClassId() not in classes:
                classes.append(bb.getClassId())
        classes = sorted(classes)
        # Precision x Recall is obtained individually by each class
        # Loop through by classes

        n_class = len(classes)
        total_prec = 0.0
        total_recall = 0.0
        total_f_score = 0.0
        total_map = 0.0

        new_detection = []  # use to plot image
        for c in classes:
            # Get only detection of class c
            dects = []
            [dects.append(d) for d in detections if d[1] == c]
            # Get only ground truths of class c
            gts = []
            [gts.append(g) for g in groundTruths if g[1] == c]
            npos = len(gts)
            # sort detections by decreasing confidence
            dects = sorted(dects, key=lambda conf: conf[2], reverse=True)
            TP = np.zeros(len(dects))
            FP = np.zeros(len(dects))

            # create dictionary with amount of gts for each image
            det = Counter([cc[0] for cc in gts])
            # det_pred = Counter([cc[0] for cc in gts])
            for key, val in det.items():
                det[key] = np.zeros(val)  # key: image_name, val: frequency
            # print("Evaluating class: %s (%d detections)" % (str(c), len(dects)))
            # Loop through detections
            for d in range(len(dects)):
                # print('dect %s => %s' % (dects[d][0], dects[d][3],))
                # Find ground truth image
                temp_det = dects[d]
                fportp = "FP:"  # default FP
                gt = [gt for gt in gts if gt[0] == dects[d][0]]  
                # NO GT
                if len(gt) == 0:
                    FP[d] = 1
                    continue

                iouMax = sys.float_info.min
                for j in range(len(gt)):
                    # print('Ground truth gt => %s' % (gt[j][3],))
                    iou = DetMetric.iou(dects[d][3], gt[j][3])
                    if iou > iouMax:
                        iouMax = iou
                        jmax = j
                # Assign detection as true positive/don't care/false positive
                if iouMax >= IOUThreshold:
                    if det[dects[d][0]][jmax] == 0:
                        TP[d] = 1  # count as true positive
                        det[dects[d][0]][jmax] = 1  # flag as already 'seen'
                        fportp = 'TP:'
                        # print("TP")
                    else:
                        FP[d] = 1  # count as false positive
                        # print("FP")
                # - A detected "cat" is overlaped with a GT "cat" with IOU >= IOUThreshold.
                else:
                    FP[d] = 1  # count as false positive
                    # print("FP")
                temp_det.append(fportp)
                new_detection.append(temp_det)
            
            # compute precision, recall and average precision
            acc_FP = np.cumsum(FP)
            acc_TP = np.cumsum(TP)
            rec = acc_TP / npos
            prec = np.divide(acc_TP, (acc_FP + acc_TP))
            # Depending on the method, call the right implementation
            if method == MethodAveragePrecision.EveryPointInterpolation:
                [ap, mpre, mrec, ii] = DetMetric.CalculateAveragePrecision(rec, prec)
            elif method == MethodAveragePrecision.ElevenPointInterpolation:
                [ap, mpre, mrec, _] = DetMetric.ElevenPointInterpolatedAP(rec, prec)
            else:
                [ap, mpre, mrec, _] = DetMetric.COCOInterpolatedAP(rec, prec)
            # add class result in the dictionary to be returned

            f_score = (1 + beta**2) * prec[-1] * rec[-1] / ((beta**2 * prec[-1]) + rec[-1] + 1e-16)
            total_prec += prec[-1]
            total_recall += rec[-1]
            total_f_score += f_score

            total_map += ap

            r = {
                'class': c,
                'precision': prec,
                'recall': rec,
                'f_score':f_score,
                'AP': ap,
                'interpolated precision': mpre,
                'interpolated recall': mrec,
                'total positives': npos,
                'total TP': np.sum(TP),
                'total FP': np.sum(FP)
            }
            ret.append(r)

        all_precision = total_prec / n_class
        all_recall = total_recall / n_class
        all_f_score = total_f_score / n_class
        all_ap = total_map / n_class

        # plot image detection
        if getpredimg:
            DetMetric.plotimg(imgdir,groundTruths,new_detection,numerical)

        return ret, {"all_precision":all_precision, "all_recall": all_recall, "all_f_score": all_f_score,"total_map": all_ap}

    def PlotPRCurve(self,
                     boundingBoxes,
                     IOUThreshold=0.5,
                     beta=1,
                     method=MethodAveragePrecision.EveryPointInterpolation,
                     showAP=False,
                     showInterpolatedPrecision=False,
                     savePath=None,
                     showGraphic=True,
                     numerical=3,
                     color=None,
                     linestyle=None):
        """PlotPrecisionRecallCurve
        Plot the Precision x Recall curve for a given class.
        Source: https://github.com/rafaelpadilla/Object-Detection-Metrics
        
        Args:
            boundingBoxes: Object of the class BoundingBoxes representing ground truth and detected
            bounding boxes;
            IOUThreshold (optional): IOU threshold indicating which detections will be considered
            TP or FP (default value = 0.5);
            method (default = EveryPointInterpolation): It can be calculated as the implementation
            in the official PASCAL VOC toolkit (EveryPointInterpolation), or applying the 11-point
            interpolatio as described in the paper "The PASCAL Visual Object Classes(VOC) Challenge"
            or EveryPointInterpolation"  (ElevenPointInterpolation).
            showAP (optional): if True, the average precision value will be shown in the title of
            the graph (default = False);
            showInterpolatedPrecision (optional): if True, it will show in the plot the interpolated
             precision (default = False);
            savePath (optional): if informed, the plot will be saved as an image in this path
            (ex: /home/mywork/ap.png) (default = None);
            showGraphic (optional): if True, the plot will be shown (default = True)
            numerical: numerical accuracy of drawing
            color: plot line color.
            linestyle: plot line style
        Returns:
            A list of dictionaries. Each dictionary contains information and metrics of each class.
            The keys of each dictionary are:
            dict['class']: class representing the current dictionary;
            dict['precision']: array with the precision values;
            dict['recall']: array with the recall values;
            dict['AP']: average precision;
            dict['interpolated precision']: interpolated precision values;
            dict['interpolated recall']: interpolated recall values;
            dict['total positives']: total number of ground truth positives;
            dict['total TP']: total number of True Positive detections;
            dict['total FP']: total number of False Negative detections;
        """
        jingdu = "0.{}".format("0"*numerical)

        results, _ = self.GetDetMetrics(boundingBoxes, IOUThreshold,beta, method)
        result = None
        # Each resut represents a class

        if color is None:
            color = ["#0000FF","#DC143C","#FF00FF","#9932CC","#00BFFF","#00FFFF","#00FF7F","#000000","#FF00FF","#7B68EE"]
        if linestyle is None:
            linestyle = ['-','--','-.',':']
        for result in results:
            if result is None:
                raise IOError('Error: Class %d could not be found.' % classId)

            classId = result['class']
            precision = result['precision']
            recall = result['recall']
            average_precision = result['AP']
            mpre = result['interpolated precision']
            mrec = result['interpolated recall']
            npos = result['total positives']
            total_tp = result['total TP']
            total_fp = result['total FP']

            # plt.close()
            if showInterpolatedPrecision:
                if method == MethodAveragePrecision.EveryPointInterpolation:
                    plt.plot(mrec, mpre, '--r', label='Interpolated precision (every point)')
                elif method == MethodAveragePrecision.ElevenPointInterpolation:
                    # Uncomment the line below if you want to plot the area
                    # plt.plot(mrec, mpre, 'or', label='11-point interpolated precision')
                    # Remove duplicates, getting only the highest precision of each recall value
                    nrec = []
                    nprec = []
                    for idx in range(len(mrec)):
                        r = mrec[idx]
                        if r not in nrec:
                            idxEq = np.argwhere(mrec == r)
                            nrec.append(r)
                            nprec.append(max([mpre[int(id)] for id in idxEq]))
                    plt.plot(nrec, nprec, 'or', label='11-point interpolated precision')
                else:
                    nrec = []
                    nprec = []
                    for idx in range(len(mrec)):
                        r = mrec[idx]
                        if r not in nrec:
                            idxEq = np.argwhere(mrec == r)
                            nrec.append(r)
                            nprec.append(max([mpre[int(id)] for id in idxEq]))
                    plt.plot(nrec, nprec, 'or', label='COCO interpolated precision')

            # new_recall = np.linspace(np.array(recall).min(),np.array(recall).max(),150)
            # new_precision = make_interp_spline(np.array(recall),np.array(precision))(new_recall)
            # plt.plot(new_recall, new_precision, c=random.choice(color), ls=random.choice(linestyle),
            #     label='{}:AP@{}={}'.format(classId, int(IOUThreshold*100),round(average_precision,3)))
            plt.plot(recall, precision, c=random.choice(color), ls=random.choice(linestyle),
                label='{} AP@{}={}'.format(classId, int(IOUThreshold*100),Decimal(str(average_precision)).quantize(Decimal(jingdu))))
            plt.xlabel(r'$Recall=\frac{TP}{TP+FN}=\frac{TP}{all\; ground\; truths}$')
            plt.ylabel(r'$Precision=\frac{TP}{TP+FP}=\frac{TP}{all\; detections}$')
            plt.xlim(0, 1.01)
            plt.ylim(0, 1.01)
            plt.title('Precision x Recall Curve')
            # if showAP:
            #     ap_str = "{0:.2f}%".format(average_precision * 100)
            #     # ap_str = "{0:.4f}%".format(average_precision * 100)
            #     plt.title('Precision x Recall Curve \nClass: %s, AP: %s' % (str(classId), ap_str))
            # else:
            #     plt.title('Precision x Recall Curve \nClass: %s' % str(classId))
            # plt.legend(shadow=True)
            plt.legend()

            # plt.grid()
            ############################################################
            # Uncomment the following block to create plot with points #
            ############################################################
            # plt.plot(recall, precision, 'bo')
            # labels = ['R', 'Y', 'J', 'A', 'U', 'C', 'M', 'F', 'D', 'B', 'H', 'P', 'E', 'X', 'N', 'T',
            # 'K', 'Q', 'V', 'I', 'L', 'S', 'G', 'O']
            # dicPosition = {}
            # dicPosition['left_zero'] = (-30,0)
            # dicPosition['left_zero_slight'] = (-30,-10)
            # dicPosition['right_zero'] = (30,0)
            # dicPosition['left_up'] = (-30,20)
            # dicPosition['left_down'] = (-30,-25)
            # dicPosition['right_up'] = (20,20)
            # dicPosition['right_down'] = (20,-20)
            # dicPosition['up_zero'] = (0,30)
            # dicPosition['up_right'] = (0,30)
            # dicPosition['left_zero_long'] = (-60,-2)
            # dicPosition['down_zero'] = (-2,-30)
            # vecPositions = [
            #     dicPosition['left_down'],
            #     dicPosition['left_zero'],
            #     dicPosition['right_zero'],
            #     dicPosition['right_zero'],  #'R', 'Y', 'J', 'A',
            #     dicPosition['left_up'],
            #     dicPosition['left_up'],
            #     dicPosition['right_up'],
            #     dicPosition['left_up'],  # 'U', 'C', 'M', 'F',
            #     dicPosition['left_zero'],
            #     dicPosition['right_up'],
            #     dicPosition['right_down'],
            #     dicPosition['down_zero'],  #'D', 'B', 'H', 'P'
            #     dicPosition['left_up'],
            #     dicPosition['up_zero'],
            #     dicPosition['right_up'],
            #     dicPosition['left_up'],  # 'E', 'X', 'N', 'T',
            #     dicPosition['left_zero'],
            #     dicPosition['right_zero'],
            #     dicPosition['left_zero_long'],
            #     dicPosition['left_zero_slight'],  # 'K', 'Q', 'V', 'I',
            #     dicPosition['right_down'],
            #     dicPosition['left_down'],
            #     dicPosition['right_up'],
            #     dicPosition['down_zero']
            # ]  # 'L', 'S', 'G', 'O'
            # for idx in range(len(labels)):
            #     box = dict(boxstyle='round,pad=.5',facecolor='yellow',alpha=0.5)
            #     plt.annotate(labels[idx],
            #                 xy=(recall[idx],precision[idx]), xycoords='data',
            #                 xytext=vecPositions[idx], textcoords='offset points',
            #                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
            #                 bbox=box)
        if savePath is not None:
            plt.savefig(savePath)
        if showGraphic is True:
            plt.show()
            # plt.waitforbuttonpress()
            plt.pause(0.05)
        return results

    @staticmethod
    def CalculateAveragePrecision(rec, prec):
        mrec = []
        mrec.append(0)
        [mrec.append(e) for e in rec]
        mrec.append(1)
        mpre = []
        mpre.append(0)
        [mpre.append(e) for e in prec]
        mpre.append(0)
        for i in range(len(mpre) - 1, 0, -1):
            mpre[i - 1] = max(mpre[i - 1], mpre[i])
        ii = []
        for i in range(len(mrec) - 1):
            if mrec[1:][i] != mrec[0:-1][i]:
                ii.append(i + 1)
        ap = 0
        for i in ii:
            ap = ap + np.sum((mrec[i] - mrec[i - 1]) * mpre[i])
        # return [ap, mpre[1:len(mpre)-1], mrec[1:len(mpre)-1], ii]
        return [ap, mpre[0:len(mpre) - 1], mrec[0:len(mpre) - 1], ii]

    @staticmethod
    # 11-point interpolated average precision
    def ElevenPointInterpolatedAP(rec, prec):
        # def CalculateAveragePrecision2(rec, prec):
        mrec = []
        # mrec.append(0)
        [mrec.append(e) for e in rec]
        # mrec.append(1)
        mpre = []
        # mpre.append(0)
        [mpre.append(e) for e in prec]
        # mpre.append(0)
        recallValues = np.linspace(0, 1, 11)
        recallValues = list(recallValues[::-1])
        rhoInterp = []
        recallValid = []
        # For each recallValues (0, 0.1, 0.2, ... , 1)
        for r in recallValues:
            # Obtain all recall values higher or equal than r
            argGreaterRecalls = np.argwhere(mrec[:] >= r)
            pmax = 0
            # If there are recalls above r
            if argGreaterRecalls.size != 0:
                pmax = max(mpre[argGreaterRecalls.min():])
            recallValid.append(r)
            rhoInterp.append(pmax)
        # By definition AP = sum(max(precision whose recall is above r))/11
        ap = sum(rhoInterp) / 11
        # Generating values for the plot
        rvals = []
        rvals.append(recallValid[0])
        [rvals.append(e) for e in recallValid]
        rvals.append(0)
        pvals = []
        pvals.append(0)
        [pvals.append(e) for e in rhoInterp]
        pvals.append(0)
        # rhoInterp = rhoInterp[::-1]
        cc = []
        for i in range(len(rvals)):
            p = (rvals[i], pvals[i - 1])
            if p not in cc:
                cc.append(p)
            p = (rvals[i], pvals[i])
            if p not in cc:
                cc.append(p)
        recallValues = [i[0] for i in cc]
        rhoInterp = [i[1] for i in cc]
        return [ap, rhoInterp, recallValues, None]

    
    @staticmethod
    # coco 101 interpolated average precision
    def COCOInterpolatedAP(rec, prec):
        # def CalculateAveragePrecision2(rec, prec):
        mrec = []
        # mrec.append(0)
        [mrec.append(e) for e in rec]
        # mrec.append(1)
        mpre = []
        # mpre.append(0)
        [mpre.append(e) for e in prec]
        # mpre.append(0)
        recallValues = np.linspace(0, 1, 100)
        recallValues = list(recallValues[::-1])
        rhoInterp = []
        recallValid = []
        # For each recallValues (0, 0.1, 0.2, ... , 1)
        for r in recallValues:
            # Obtain all recall values higher or equal than r
            argGreaterRecalls = np.argwhere(mrec[:] >= r)
            pmax = 0
            # If there are recalls above r
            if argGreaterRecalls.size != 0:
                pmax = max(mpre[argGreaterRecalls.min():])
            recallValid.append(r)
            rhoInterp.append(pmax)
        # By definition AP = sum(max(precision whose recall is above r))/11
        ap = sum(rhoInterp) / 101
        # Generating values for the plot
        rvals = []
        rvals.append(recallValid[0])
        [rvals.append(e) for e in recallValid]
        rvals.append(0)
        pvals = []
        pvals.append(0)
        [pvals.append(e) for e in rhoInterp]
        pvals.append(0)
        # rhoInterp = rhoInterp[::-1]
        cc = []
        for i in range(len(rvals)):
            p = (rvals[i], pvals[i - 1])
            if p not in cc:
                cc.append(p)
            p = (rvals[i], pvals[i])
            if p not in cc:
                cc.append(p)
        recallValues = [i[0] for i in cc]
        rhoInterp = [i[1] for i in cc]
        return [ap, rhoInterp, recallValues, None]


    # For each detections, calculate IOU with reference
    @staticmethod
    def _getAllIOUs(reference, detections):
        ret = []
        bbReference = reference.getAbsoluteBoundingBox(BBFormat.XYX2Y2)
        # img = np.zeros((200,200,3), np.uint8)
        for d in detections:
            bb = d.getAbsoluteBoundingBox(BBFormat.XYX2Y2)
            iou = DetMetric.iou(bbReference, bb)
            # Show blank image with the bounding boxes
            # img = add_bb_into_image(img, d, color=(255,0,0), thickness=2, label=None)
            # img = add_bb_into_image(img, reference, color=(0,255,0), thickness=2, label=None)
            ret.append((iou, reference, d))  # iou, reference, detection
        # cv2.imshow("comparing",img)
        # cv2.waitKey(0)
        # cv2.destroyWindow("comparing")
        return sorted(ret, key=lambda i: i[0], reverse=True)  # sort by iou (from highest to lowest)

    @staticmethod
    def iou(boxA, boxB):
        # if boxes dont intersect
        if DetMetric._boxesIntersect(boxA, boxB) is False:
            return 0
        interArea = DetMetric._getIntersectionArea(boxA, boxB)
        union = DetMetric._getUnionAreas(boxA, boxB, interArea=interArea)
        # intersection over union
        iou = interArea / union
        assert iou >= 0
        return iou

    # boxA = (Ax1,Ay1,Ax2,Ay2)
    # boxB = (Bx1,By1,Bx2,By2)
    @staticmethod
    def _boxesIntersect(boxA, boxB):
        if boxA[0] > boxB[2]:
            return False  # boxA is right of boxB
        if boxB[0] > boxA[2]:
            return False  # boxA is left of boxB
        if boxA[3] < boxB[1]:
            return False  # boxA is above boxB
        if boxA[1] > boxB[3]:
            return False  # boxA is below boxB
        return True

    @staticmethod
    def _getIntersectionArea(boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        # intersection area
        return (xB - xA + 1) * (yB - yA + 1)

    @staticmethod
    def _getUnionAreas(boxA, boxB, interArea=None):
        area_A = DetMetric._getArea(boxA)
        area_B = DetMetric._getArea(boxB)
        if interArea is None:
            interArea = DetMetric._getIntersectionArea(boxA, boxB)
        return float(area_A + area_B - interArea)

    @staticmethod
    def _getArea(box):
        return (box[2] - box[0] + 1) * (box[3] - box[1] + 1)


    @staticmethod
    def plotimg(imgdir,gt,det,numerical=2):
        jingdu = "0.{}".format("0"*numerical)

        files = os.listdir(imgdir)
        if not os.path.exists(imgdir+"_detect"):
            os.makedirs(imgdir+"_detect")

        save_path = imgdir+"_detect"

        pfiles = tqdm(files)
        for file in pfiles:
            file_name = ".".join(file.split(".")[:-1])
            # get file gt and det
            pred_boxs = [det[i] for i in range(len(det)) if det[i][0] == file_name]
            gt_boxs = [gt[i] for i in range(len(gt)) if gt[i][0] == file_name]

            img = cv2.imread(os.path.join(imgdir,file))
            img_w = img.shape[1]
            img_h = img.shape[0]

            tl_ = int(round(0.002 * img_h))  # line thickness
            tf_ = max(tl_ - 1, 1)

            # plot mask
            mask_threth = 50
            for j in range(len(gt_boxs)):
                (x1, y1, x2, y2) = gt_boxs[j][3]
                gt_label = "GT:"+gt_boxs[j][1]

                if y2+20 > img_h:
                    cv2.putText(img, gt_label, (int(x1+10), int(y2-20)), 0, float(tl_) / 2, (0, 0, 0), thickness=tf_, lineType=cv2.LINE_AA)
                else:
                    cv2.putText(img, gt_label, (int(x1+10), int(y2+20)), 0, float(tl_) / 2, (0, 215, 255), thickness=tf_, lineType=cv2.LINE_AA)
                # cv2.putText(img, gt_label, (int(x1+10), int(y2+20)), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 215, 255), thickness=1)

                # binary mask
                coordinates = [[[int(x1),int(y1)], [int(x2),int(y1)], [int(x2),int(y2)], [int(x1),int(y2)]]]
                coordinates = np.array(coordinates)
                mask = np.zeros(img.shape[:2], dtype=np.int8)
                mask = cv2.fillPoly(mask, coordinates, 255)

                bbox_mask = (mask > mask_threth).astype(np.uint8)
                bbox_mask = bbox_mask.astype(np.bool)

                # draw the masked image
                # color_mask = np.random.randint(0, 256, (1, 3), dtype=np.uint8) #(255,0,0)
                color_mask = np.array([0, 215, 255], dtype=np.uint8)
                # color_mask = np.array([0, 255, 0], dtype=np.uint8)

                img[bbox_mask] = img[bbox_mask] * 0.8 + color_mask * 0.2


            # plot detect box
            for j in range(len(pred_boxs)):
                (x1, y1, x2, y2) = pred_boxs[j][3]

                if int(x1) < 0:
                    x1 = 0
                if int(x2) > img_w:
                    x2 = img_w
                if int(y1) < 0:
                    y1 = 0
                if int(y2) > img_h:
                    y2 = img_h

                prob = pred_boxs[j][2]
                label = pred_boxs[j][1]
                tporfp = pred_boxs[j][4]

                prob_ = Decimal(str(prob*100)).quantize(Decimal(jingdu))

                text_label = tporfp + label + ":" + str(prob_) + "%"
                c1, c2 = [int(x1), int(y1)], [int(x2), int(y2)]

                if tporfp == "TP:":
                    color = (255, 255, 0)
                else:
                    color = (147, 20, 255)  

               
                cv2.rectangle(img, (c1[0],c1[1]), (c2[0],c2[1]), color, thickness=tl_)
                t_size = cv2.getTextSize(text_label, 0, fontScale=float(tl_) / 2, thickness=tf_)[0]

                c2 = [int(x1 + t_size[0]), int(y1 - t_size[1] - 3)]
                if c2[0] > img_w:
                    c2[0] = int(x2)
                    c1[0] = int(x2-t_size[0])
                if c2[1] < 0:
                    c2[1] = int(y1)
                    c1[1] = int(y1 + t_size[1] + 3)

                cv2.rectangle(img, (c1[0],c1[1]), (c2[0],c2[1]), color, -1)  # filled

                cv2.putText(img, text_label,
                            (c1[0], c1[1] - 2), 0, float(tl_) / 2, 
                            (0, 0, 0), thickness=tf_, lineType=cv2.LINE_AA)

            cv2.imwrite(os.path.join(save_path,file), img)
            pfiles.set_description("Saved the detected image: %s" % file)















