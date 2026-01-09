package com.insurance.qa.service;

import com.insurance.qa.dto.ChatMessageDto;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class DialogueSession {
  private final String sessionId;
  private final Long roleId;
  private final Long productId;
  private final String roleName;
  private final String productName;
  private final String rolePrompt;
  private final String productInfo;
  private final List<ChatMessageDto> dialogueHistory = new CopyOnWriteArrayList<>();

  public DialogueSession(
      String sessionId,
      Long roleId,
      Long productId,
      String roleName,
      String productName,
      String rolePrompt,
      String productInfo) {
    this.sessionId = sessionId;
    this.roleId = roleId;
    this.productId = productId;
    this.roleName = roleName;
    this.productName = productName;
    this.rolePrompt = rolePrompt;
    this.productInfo = productInfo;
  }

  public void addMessage(String role, String content) {
    dialogueHistory.add(new ChatMessageDto(role, content));
  }

  public String getSessionId() {
    return sessionId;
  }

  public Long getRoleId() {
    return roleId;
  }

  public Long getProductId() {
    return productId;
  }

  public String getRoleName() {
    return roleName;
  }

  public String getProductName() {
    return productName;
  }

  public String getRolePrompt() {
    return rolePrompt;
  }

  public String getProductInfo() {
    return productInfo;
  }

  public List<ChatMessageDto> getDialogueHistory() {
    return dialogueHistory;
  }
}
