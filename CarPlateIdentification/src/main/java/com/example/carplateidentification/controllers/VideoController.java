package com.example.carplateidentification.controllers;

import com.example.carplateidentification.pojo.OcrResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.client.RestTemplate;

import java.util.Objects;

@Controller
public class VideoController {


    private final RestTemplate restTemplate;

    @Autowired
    public VideoController(RestTemplateBuilder builder) {
        this.restTemplate = builder.build();
    }


    @GetMapping("/testVideo")
    public String testVideo(Model model) {
        model.addAttribute("videoUrl","http://localhost:5001/testVideo");
        return "testVideo";
    }

    @RequestMapping("/test")
    public String test(Model model) {
        model.addAttribute("hello","Hello tof");
        return "test";
    }


    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("title","Raw Video");
        model.addAttribute("showResult",false);

        model.addAttribute("rawUrl","http://localhost:5001/testVideo");
        return "result";
    }




    @GetMapping("/result")
    public String result(Model model) {
        model.addAttribute("title","Result");
        model.addAttribute("showResult",true);

        model.addAttribute("rawUrl","http://localhost:5001/testVideo");
        model.addAttribute("preUrl","http://localhost:5001/preResult");
        model.addAttribute("yoloUrl","http://localhost:5001/yoloResult");

        String ocrUrl = "http://localhost:5001/ocrResult";
        OcrResult ocrResult = restTemplate.getForObject(ocrUrl,OcrResult.class);
        model.addAttribute("ocrResult", Objects.requireNonNull(ocrResult).getResult());
        return "result";
    }

    @GetMapping("/reset")
    public String reset(Model model) {
        return "redirect:/";
    }

}
