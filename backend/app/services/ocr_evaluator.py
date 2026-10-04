from typing import Any

import jiwer


class OCREvaluator:
    """
    Evaluates OCR accuracy comparing ground truth reference against
    predicted texts using industry standard Word Error Rate (WER)
    and Character Error Rate (CER) metrics from Section 24 of DocVision report.
    """

    @staticmethod
    def calculate_metrics(ground_truth: str, predicted_text: str) -> dict[str, Any]:
        gt_clean = ground_truth.strip()
        pred_clean = predicted_text.strip()

        if not gt_clean:
            return {
                "cer": 0.0 if not pred_clean else 1.0,
                "wer": 0.0 if not pred_clean else 1.0,
                "accuracy_char_percent": 100.0 if not pred_clean else 0.0,
                "accuracy_word_percent": 100.0 if not pred_clean else 0.0
            }

        # Calculate Character Error Rate (CER)
        cer = jiwer.cer(gt_clean, pred_clean)
        # Calculate Word Error Rate (WER)
        wer = jiwer.wer(gt_clean, pred_clean)

        # Accuracy percentage approximations bounded at 0-100%
        char_acc = max(0.0, min(100.0, (1.0 - cer) * 100.0))
        word_acc = max(0.0, min(100.0, (1.0 - wer) * 100.0))

        return {
            "cer": round(float(cer), 4),
            "wer": round(float(wer), 4),
            "accuracy_char_percent": round(char_acc, 2),
            "accuracy_word_percent": round(word_acc, 2),
            "ground_truth_len": len(gt_clean),
            "predicted_len": len(pred_clean)
        }

    def benchmark_comparison(
        self,
        ground_truth: str,
        raw_image_ocr: str,
        processed_image_ocr: str,
        processing_time_ms: float = 0.0
    ) -> dict[str, Any]:
        """
        Generates comparative evaluation report comparing raw un-processed image
        against CV-enhanced document scan.
        """
        raw_eval = self.calculate_metrics(ground_truth, raw_image_ocr)
        proc_eval = self.calculate_metrics(ground_truth, processed_image_ocr)

        # Error rate reduction percentage
        cer_reduction = raw_eval["cer"] - proc_eval["cer"]
        wer_reduction = raw_eval["wer"] - proc_eval["wer"]

        return {
            "raw_metrics": raw_eval,
            "processed_metrics": proc_eval,
            "improvement": {
                "cer_reduction": round(float(cer_reduction), 4),
                "wer_reduction": round(float(wer_reduction), 4),
                "char_accuracy_gain": round(proc_eval["accuracy_char_percent"] - raw_eval["accuracy_char_percent"], 2),
                "word_accuracy_gain": round(proc_eval["accuracy_word_percent"] - raw_eval["accuracy_word_percent"], 2)
            },
            "processing_time_ms": round(processing_time_ms, 2)
        }
