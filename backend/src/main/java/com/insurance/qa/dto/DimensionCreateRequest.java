package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;

public class DimensionCreateRequest {
  @NotBlank
  private String name;
  private String description;
  private Double weight;
  @JsonProperty("evaluation_prompt")
  private String evaluationPrompt;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public Double getWeight() {
    return weight;
  }

  public void setWeight(Double weight) {
    this.weight = weight;
  }

  public String getEvaluationPrompt() {
    return evaluationPrompt;
  }

  public void setEvaluationPrompt(String evaluationPrompt) {
    this.evaluationPrompt = evaluationPrompt;
  }
}
