package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;

public class ModelCreateRequest {
  @NotBlank
  @JsonProperty("model_name")
  private String modelName;
  private String provider;
  @JsonProperty("api_key")
  private String apiKey;
  @JsonProperty("api_base")
  private String apiBase;
  @JsonProperty("is_active")
  private boolean isActive = true;

  public String getModelName() {
    return modelName;
  }

  public void setModelName(String modelName) {
    this.modelName = modelName;
  }

  public String getProvider() {
    return provider;
  }

  public void setProvider(String provider) {
    this.provider = provider;
  }

  public String getApiKey() {
    return apiKey;
  }

  public void setApiKey(String apiKey) {
    this.apiKey = apiKey;
  }

  public String getApiBase() {
    return apiBase;
  }

  public void setApiBase(String apiBase) {
    this.apiBase = apiBase;
  }

  public boolean isActive() {
    return isActive;
  }

  public void setActive(boolean active) {
    isActive = active;
  }
}
