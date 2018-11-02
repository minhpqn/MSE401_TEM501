"""
Evaluation script for the course project
HOW TO USE:
python ./evaluate.py <output_file> <test_file>

References:
    1) https://multimediaeval.github.io/2017-Multimedia-Satellite-Task/
    2) https://www.slideshare.net/multimediaeval/mediaeval-2017-satellite-task-the-multimedia-satellite-task-at-mediaeval-2017-emergence-response-for-flooding-events-overview
    3) https://github.com/benhamner/Metrics/blob/master/Python/ml_metrics/average_precision.py
    4) https://ils.unc.edu/courses/2013_spring/inls509_001/lectures/10-EvaluationMetrics.pdf
"""
import numpy
from sklearn import metrics
from collections import Counter
import pandas as pd
from argparse import ArgumentParser
from unittest import TestCase


def average_precision_at_k(k, doc_labels):
    """Average Precision at k
    """
    k = min(k, len(doc_labels))
    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(doc_labels[:k]):
        if p == 1:
            num_hits += 1
            score += num_hits / (i+1.0)
    if num_hits == 0:
        return 0.0
    return score/num_hits


class TestEvalMeasure(TestCase):

    def test_average_precision(self):
        docs = [1, 0, 0, 1, 1, 0, 0]
        avg_at_2 = average_precision_at_k(2, docs)
        print("AP@2={}".format(avg_at_2))
        print("AP@3={}".format(average_precision_at_k(3, docs)))
        self.assertAlmostEqual(0.5, average_precision_at_k(2, [0,1,0,1,1]))
        print("AP@2={}".format(average_precision_at_k(2,[0,1,0,0])))

        docs = [1,0,1,1,1,1,1,0,1,0,1,0,0,1,0,0,0,0,0,1]
        self.assertEqual(20, len(docs))
        print(average_precision_at_k(20, docs))

        docs = [1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        print(average_precision_at_k(20, docs))

        docs = [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        print(average_precision_at_k(20, docs))

        docs = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]
        print(average_precision_at_k(20, docs))

def main():
    parser = ArgumentParser()
    parser.add_argument("output_file", help="Submission result")
    parser.add_argument("label_file",
                        help="Test ground-truth file")
    args = parser.parse_args()

    id2gt = {}
    test_gt_labels = []
    test_image_ids = []
    df = pd.read_csv(args.label_file, header=None)
    for i in range(len(df)):
        _id, _lb = str(df.iloc[i][0]), df.iloc[i][1]
        id2gt[_id] = _lb
        test_image_ids.append(_id)
        test_gt_labels.append(_lb)

    print("Ground-truth label distribution")
    print(Counter(test_gt_labels))
    print()

    ranked_image_ids = []
    predicted_labels = []
    ranked_gt_labels = []
    with open(args.output_file, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            fields = line.split()
            if len(fields) >= 1:
                img_id = str(fields[0])
                if len(fields) == 2:
                    proba = float(fields[1])
                    lb = 1 if proba > 0.5 else 0
                    predicted_labels.append(lb)
                ranked_image_ids.append(img_id)
                assert img_id in id2gt, "{}".format(img_id)
                ranked_gt_labels.append(id2gt[img_id])
            else:
                raise Exception
    if len(predicted_labels) == len(ranked_gt_labels):
        accuracy = metrics.accuracy_score(ranked_gt_labels, predicted_labels)
        print("Accuracy: {}".format(accuracy))
        print("Detailed classification report")
        print(metrics.classification_report(ranked_gt_labels, predicted_labels))

    cutoff = 480
    cutoff_vals = [50, 100, 250, 480]

    avg_prec_at_k = 100*average_precision_at_k(cutoff, ranked_gt_labels)
    print("AP@{} = {} %".format(cutoff, avg_prec_at_k))

    scores = []
    for k in cutoff_vals:
        avg_prec = 100.0 * average_precision_at_k(k, ranked_gt_labels)
        print('AP@%d = %f' % (k, avg_prec))
        scores.append(avg_prec)
    avg = numpy.mean(scores)
    print("Mean AP@ [{}] = {}".format(", ".join([str(x) for x in cutoff_vals]), avg))


if __name__ == "__main__":
    main()
