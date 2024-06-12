package com.example.carplateidentification.pojo;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class VideoStatus {
    private boolean finish;
    private String baseImg;

    public VideoStatus(boolean finish, String baseImg) {
        this.finish = finish;
        this.baseImg = baseImg;
    }

    public VideoStatus() {}
}
