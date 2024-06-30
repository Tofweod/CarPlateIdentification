package com.example.carplateidentification.pojo;

import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class OcrResult {
    private String result;
    private Integer status;

    @Override
    public String toString() {
        return "OcrResult [result=" + result + ", status=" + status + "]";
    }
}
