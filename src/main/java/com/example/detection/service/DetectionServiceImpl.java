package com.example.detection.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.lang3.tuple.ImmutablePair;
import org.apache.commons.lang3.tuple.Pair;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.MatOfRect;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;
import lombok.extern.slf4j.Slf4j;
import lombok.SneakyThrows;

import java.util.Arrays;

import static org.opencv.imgcodecs.Imgcodecs.IMREAD_GRAYSCALE;

@Slf4j
@Service
public class DetectionServiceImpl implements DetectionService {

    private final Scalar rectangleColor;
    private final int imageSize;
    private final String noiseReductionHost;
    private final String noiseReductionPort;
    private final CascadeClassifier faceDetector;
    private final RestTemplate restTemplate;

    public DetectionServiceImpl(RestTemplateBuilder restTemplateBuilder,
                                @Value("${detection-service.image-size:640}") int imageSize,
                                @Value("${detection-service.noise-reduction-server.host}") String noiseReductionHost,
                                @Value("${detection-service.noise-reduction-server.port}") String noiseReductionPort,
                                @Value("${detection-service.cascade}") String cascade) {
        restTemplate = restTemplateBuilder.build();
        this.imageSize = imageSize;
        this.noiseReductionHost = noiseReductionHost;
        this.noiseReductionPort = noiseReductionPort;
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        faceDetector = new CascadeClassifier(cascade);
        rectangleColor = new Scalar(255, 255, 255);
    }

    public Pair<Integer, Mat> analyze(byte[] payload) {
        Mat image = Imgcodecs.imdecode(new MatOfByte(payload), IMREAD_GRAYSCALE);
        int width = image.cols();
        int height = image.rows();
        if (width > imageSize || height > imageSize) {
            double scale = (double) Math.max(width, height) / imageSize;
            Mat buf = new Mat();
            Imgproc.resize(image, buf, new Size(width / scale, height / scale));
            image = buf;
        }
        log.debug(image.toString());
        Rect[] detected = detect(image);
        if (detected.length == 0) {
            detected = decompose(image);
        }
        log.info(String.format("Detected %s object", detected.length));
        for (Rect rect : detected) {
            Imgproc.rectangle(image, new Point(rect.x, rect.y),
                    new Point(rect.x + rect.width, rect.y + rect.height),
                    rectangleColor);
        }
        return new ImmutablePair<>(detected.length, image);
    }

    private Rect[] detect(Mat image) {
        MatOfRect faceDetections = new MatOfRect();
        faceDetector.detectMultiScale(image, faceDetections);
        return faceDetections.toArray();
    }

    @SneakyThrows
    private Rect[] decompose(Mat image) {
        int width = image.cols();
        int height = image.rows();
        HttpHeaders headers = new HttpHeaders();
        headers.set("Accept", "application/json");
        String url = UriComponentsBuilder
                .fromHttpUrl(String.format("http://%s:%s/decompose", noiseReductionHost, noiseReductionPort))
                .queryParam("width", width)
                .queryParam("height", height)
                .encode()
                .toUriString();
        ObjectMapper mapper = new ObjectMapper();
        String json = mapper.writeValueAsString(Arrays.stream(image.dump().split("\\D+")).skip(1).toArray());
        double[][] payload = restTemplate.exchange(
                url, HttpMethod.POST, new HttpEntity<>(json, headers), double[][].class).getBody();
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                image.put(i, j, payload[i][j]);
            }
        }
        return detect(image);
    }
}
