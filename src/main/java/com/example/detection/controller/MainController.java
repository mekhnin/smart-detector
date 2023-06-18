package com.example.detection.controller;

import com.example.detection.service.DetectionServiceImpl;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.tuple.Pair;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.imgcodecs.Imgcodecs;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.io.IOException;
import java.util.Base64;

@Slf4j
@Controller
public class MainController {

    final DetectionServiceImpl service;

    public MainController(DetectionServiceImpl service) {
        this.service = service;
    }

    @GetMapping("/")
    public String home() {
        return "index";
    }

    @PostMapping(
            value = "/detect",
            produces = MediaType.IMAGE_PNG_VALUE)
    public String detect(@RequestParam("file") MultipartFile file,
                         RedirectAttributes attributes) throws IOException {
        if (file.isEmpty()) {
            attributes.addFlashAttribute("error", "File is empty");
            log.info("File is empty");
            return "redirect:/";
        }
        if (!file.getContentType().contains("image")) {
            attributes.addFlashAttribute("error", "File must be image");
            log.info("File is not image");
            return "redirect:/";
        }
        Pair<Integer, Mat> result = service.analyze(file.getBytes());
        int detectedCount = result.getLeft();
        Mat image = result.getRight();
        MatOfByte mb = new MatOfByte();
        Imgcodecs.imencode(".png", image, mb);
        attributes.addFlashAttribute("image", Base64.getEncoder().encodeToString(mb.toArray()));
        if (detectedCount == 0) {
            attributes.addFlashAttribute("error", "Object not found");
        } else {
            attributes.addFlashAttribute("message",
                    String.format("Detected %s object%s", detectedCount, detectedCount == 1 ? "" : "s"));
        }
        return "redirect:/";
    }
}
