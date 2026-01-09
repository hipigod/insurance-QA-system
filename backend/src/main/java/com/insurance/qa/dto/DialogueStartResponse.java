package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class DialogueStartResponse {
  @JsonProperty("session_id")
  private String sessionId;
  private String greeting;
  @JsonProperty("role_name")
  private String roleName;
  @JsonProperty("product_name")
  private String productName;

  public String getSessionId() {
    return sessionId;
  }

  public void setSessionId(String sessionId) {
    this.sessionId = sessionId;
  }

  public String getGreeting() {
    return greeting;
  }

  public void setGreeting(String greeting) {
    this.greeting = greeting;
  }

  public String getRoleName() {
    return roleName;
  }

  public void setRoleName(String roleName) {
    this.roleName = roleName;
  }

  public String getProductName() {
    return productName;
  }

  public void setProductName(String productName) {
    this.productName = productName;
  }
}
