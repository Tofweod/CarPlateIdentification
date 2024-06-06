package com.example.carplateidentification.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class VideoController {

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
}
