package com.insurance.qa.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.OffsetDateTime;
import org.hibernate.annotations.CreationTimestamp;

@Entity
@Table(name = "excellent_cases")
public class ExcellentCase {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false, length = 100)
  private String weaknessType;

  @Column(nullable = false, columnDefinition = "TEXT")
  private String caseContent;

  @Column(length = 50)
  private String dialogueNode;

  @CreationTimestamp
  private OffsetDateTime createdAt;

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

  public OffsetDateTime getCreatedAt() {
    return createdAt;
  }
}
