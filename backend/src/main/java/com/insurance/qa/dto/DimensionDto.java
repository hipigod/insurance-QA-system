package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class DimensionDto {
  private Long id;
  private String name;
  private String description;
  private double weight;
  @JsonProperty("evaluation_prompt")
  private String evaluationPrompt;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

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

  public double getWeight() {
    return weight;
  }

  public void setWeight(double weight) {
    this.weight = weight;
  }

  public String getEvaluationPrompt() {
    return evaluationPrompt;
  }

  public void setEvaluationPrompt(String evaluationPrompt) {
    this.evaluationPrompt = evaluationPrompt;
  }
}
