package com.example.carplateidentification.controllers;

import com.example.carplateidentification.config.FlaskConfig;
import com.example.carplateidentification.pojo.OcrResult;
import com.example.carplateidentification.pojo.VideoStatus;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Objects;

@Controller
public class VideoController {


    private final RestTemplate restTemplate;
    private final String flaskUrl;

    private VideoStatus result;
    private boolean hasFinished = false;

    @Autowired
    public VideoController(RestTemplateBuilder builder, FlaskConfig flaskConfig) {
        this.restTemplate = builder.build();
        flaskUrl = "http://" +flaskConfig.getHost()+":"+ flaskConfig.getPort();
    }


    @GetMapping("/testVideo")
    public String testVideo(Model model) {
        model.addAttribute("videoUrl",flaskUrl+"/testVideo");
        return "testVideo";
    }

    @RequestMapping("/test")
    public String test(Model model) {
        model.addAttribute("hello","Hello tof");
        return "test";
    }


    @GetMapping("/")
    public String index(Model model) {
        hasFinished = false;
        model.addAttribute("title","Raw Video");
        model.addAttribute("showResult",false);

        return "result";
    }

    @GetMapping("/startVideo")
    @ResponseBody
    public String startVideo() {
        return flaskUrl+"/rawVideo";
    }


    @GetMapping("/result")
    public String result(Model model) {
        model.addAttribute("title","Result");
        model.addAttribute("showResult",true);

//        model.addAttribute("rawUrl",flaskUrl+"/testVideo");

        model.addAttribute("preUrl",flaskUrl+"/preResult");
        model.addAttribute("yoloUrl",flaskUrl+"/yoloResult");


        String ocrUrl = flaskUrl + "/ocrResult";
        OcrResult ocrResult = restTemplate.getForObject(ocrUrl,OcrResult.class);
        model.addAttribute("ocrResult", Objects.requireNonNull(ocrResult).getResult());
        return "result";
    }

    @GetMapping("/reset")
    public String reset() {
        String url = flaskUrl + "/reset";
        restTemplate.getForObject(url,String.class);
        return "redirect:/";
    }


    @GetMapping("/finish")
    @ResponseBody
    public VideoStatus finish() {
        if(hasFinished) {
            return result;
        }
        String url = flaskUrl+"/sendFinished";
        result =restTemplate.getForObject(url, VideoStatus.class);
        hasFinished =Objects.requireNonNull(result).isFinish();
        return result;
    }


}
