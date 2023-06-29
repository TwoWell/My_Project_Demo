package com.tensquare.base.controller;

import entity.Result;
import entity.StatusCode;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class BaseExceptionHandler {
    @ExceptionHandler
    public Result exception(Exception e){
        e.getStackTrace();
        return new Result(false, StatusCode.ERROR,e.getMessage());
    }
}
