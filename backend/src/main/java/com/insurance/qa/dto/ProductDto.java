package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ProductDto {
  private Long id;
  private String name;
  private String description;
  @JsonProperty("product_type")
  private String productType;
  private String coverage;
  @JsonProperty("premium_range")
  private String premiumRange;
  @JsonProperty("target_audience")
  private String targetAudience;
  @JsonProperty("detailed_info")
  private String detailedInfo;

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

  public String getProductType() {
    return productType;
  }

  public void setProductType(String productType) {
    this.productType = productType;
  }

  public String getCoverage() {
    return coverage;
  }

  public void setCoverage(String coverage) {
    this.coverage = coverage;
  }

  public String getPremiumRange() {
    return premiumRange;
  }

  public void setPremiumRange(String premiumRange) {
    this.premiumRange = premiumRange;
  }

  public String getTargetAudience() {
    return targetAudience;
  }

  public void setTargetAudience(String targetAudience) {
    this.targetAudience = targetAudience;
  }

  public String getDetailedInfo() {
    return detailedInfo;
  }

  public void setDetailedInfo(String detailedInfo) {
    this.detailedInfo = detailedInfo;
  }
}
