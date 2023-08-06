from torchcv.preprocessing import ResizeImages, CreateCsv, CreateLabelMap, CalculateStats

PREPROCESS_ENGINE = {
    "resize": ResizeImages,
    "csv": CreateCsv,
    "label_map": CreateLabelMap,
    "stats": CalculateStats
}
