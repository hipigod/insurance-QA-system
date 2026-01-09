package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotNull;

public class DialogueStartRequest {
  @NotNull
  @JsonProperty("role_id")
  private Long roleId;
  @NotNull
  @JsonProperty("product_id")
  private Long productId;

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
}
