package com.tensquare.sms.listener;

import org.springframework.amqp.rabbit.annotation.RabbitHandler;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

import java.util.Map;


//可以去调阿里云的短信服务模板来发送短信
@Component
@RabbitListener(queues = "sms")
public class SmsListener {
    @RabbitHandler
    public void executeSms(Map<String, String> map) {
        System.out.println("手机号：" + map.get("mobile"));
        System.out.println("验证码：" + map.get("checkcode"));
    }
}
