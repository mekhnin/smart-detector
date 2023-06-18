package com.example.detection.service;

import org.apache.commons.lang3.tuple.Pair;
import org.opencv.core.Mat;

public interface DetectionService {
    Pair<Integer, Mat> analyze(byte[] payload);
}
