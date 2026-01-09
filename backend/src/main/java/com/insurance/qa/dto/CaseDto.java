package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class CaseDto {
  private Long id;
  @JsonProperty("weakness_type")
  private String weaknessType;
  @JsonProperty("case_content")
  private String caseContent;
  @JsonProperty("dialogue_node")
  private String dialogueNode;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

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
