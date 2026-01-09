package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;

public class CaseCreateRequest {
  @NotBlank
  @JsonProperty("weakness_type")
  private String weaknessType;
  @NotBlank
  @JsonProperty("case_content")
  private String caseContent;
  @JsonProperty("dialogue_node")
  private String dialogueNode;

  public String getWeaknessType() {
    return weaknessType;
  }

  public void setWeaknessType(String weaknessType) {
    this.weaknessType = weaknessType;
  }

  public String getCaseContent() {
    return caseContent;
  }

  public void setCaseContent(String caseContent) {
    this.caseContent = caseContent;
  }

  public String getDialogueNode() {
    return dialogueNode;
  }

  public void setDialogueNode(String dialogueNode) {
    this.dialogueNode = dialogueNode;
  }
}
