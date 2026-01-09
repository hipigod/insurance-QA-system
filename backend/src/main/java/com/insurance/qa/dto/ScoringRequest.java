package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import jakarta.validation.constraints.NotNull;

public class ScoringRequest {
  @NotNull
  @JsonProperty("role_id")
  private Long roleId;
  @NotNull
  @JsonProperty("product_id")
  private Long productId;
  private List<ChatMessageDto> history;

  public Long getRoleId() {
    return roleId;
  }

  public void setRoleId(Long roleId) {
    this.roleId = roleId;
  }

  public Long getProductId() {
    return productId;
  }

  public void setProductId(Long productId) {
    this.productId = productId;
  }

  public List<ChatMessageDto> getHistory() {
    return history;
  }

  public void setHistory(List<ChatMessageDto> history) {
    this.history = history;
  }
}
