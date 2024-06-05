package com.example.carplateidentification.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * @author Tofweod
 */
@Controller
@RequestMapping("/test")
public class TestController {

	@RequestMapping("/hello")
	public String hello(Model model) {
		model.addAttribute("hello","hello welcome");
		return "tem1";
	}
}
