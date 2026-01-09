package com.insurance.qa.controller;

import com.insurance.qa.config.AppProperties;
import com.insurance.qa.dto.ApiResponse;
import java.util.HashMap;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1")
public class HealthController {
  private final AppProperties appProperties;

  public HealthController(AppProperties appProperties) {
    this.appProperties = appProperties;
  }

  @GetMapping("/health")
  public ApiResponse<Map<String, String>> health() {
    Map<String, String> data = new HashMap<>();
    data.put("status", "healthy");
    data.put("app", appProperties.getName());
    data.put("version", appProperties.getVersion());
    return ApiResponse.success(data);
  }
}
