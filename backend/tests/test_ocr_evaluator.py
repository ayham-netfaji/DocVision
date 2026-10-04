from app.services.ocr_evaluator import OCREvaluator


def test_ocr_evaluator_exact_match():
    evaluator = OCREvaluator()
    text = "Artificial Intelligence and Computer Vision"
    metrics = evaluator.calculate_metrics(ground_truth=text, predicted_text=text)

    assert metrics["cer"] == 0.0
    assert metrics["wer"] == 0.0
    assert metrics["accuracy_char_percent"] == 100.0
    assert metrics["accuracy_word_percent"] == 100.0

def test_ocr_evaluator_errors():
    evaluator = OCREvaluator()
    gt = "Computer Vision"
    pred = "Computcr Vislon"  # 2 character errors
    metrics = evaluator.calculate_metrics(ground_truth=gt, predicted_text=pred)

    assert metrics["cer"] > 0.0
    assert metrics["wer"] > 0.0
    assert metrics["accuracy_char_percent"] < 100.0

def test_ocr_benchmark_comparison():
    evaluator = OCREvaluator()
    gt = "DocVision Optical Character Recognition"
    raw_ocr = "DocV1s1on 0ptical Charactr Recognit1on"  # noisy
    proc_ocr = "DocVision Optical Character Recognition"  # clean

    report = evaluator.benchmark_comparison(
        ground_truth=gt,
        raw_image_ocr=raw_ocr,
        processed_image_ocr=proc_ocr,
        processing_time_ms=125.4
    )

    assert report["processed_metrics"]["cer"] < report["raw_metrics"]["cer"]
    assert report["improvement"]["char_accuracy_gain"] > 0
    assert report["improvement"]["wer_reduction"] > 0
