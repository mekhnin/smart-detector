package com.example.detection.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Slf4j
@ControllerAdvice
class ExceptionsHandler {
    @ExceptionHandler({Exception.class})
    public String handler(RedirectAttributes attributes, Exception ex) {
        attributes.addFlashAttribute("error", ex.getMessage());
        log.error(ex.getMessage());
        return "redirect:/";
    }
}
