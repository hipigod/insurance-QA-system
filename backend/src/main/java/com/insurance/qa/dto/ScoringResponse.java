package com.insurance.qa.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import java.util.Map;

public class ScoringResponse {
  @JsonProperty("total_score")
  private double totalScore;
  @JsonProperty("dimension_scores")
  private Map<String, DimensionScore> dimensionScores;
  @JsonProperty("objection_tags")
  private List<String> objectionTags;
  @JsonProperty("overall_evaluation")
  private String overallEvaluation;

  public double getTotalScore() {
    return totalScore;
  }

  public void setTotalScore(double totalScore) {
    this.totalScore = totalScore;
  }

  public Map<String, DimensionScore> getDimensionScores() {
    return dimensionScores;
  }

  public void setDimensionScores(Map<String, DimensionScore> dimensionScores) {
    this.dimensionScores = dimensionScores;
  }

  public List<String> getObjectionTags() {
    return objectionTags;
  }

  public void setObjectionTags(List<String> objectionTags) {
    this.objectionTags = objectionTags;
  }

  public String getOverallEvaluation() {
    return overallEvaluation;
  }

  public void setOverallEvaluation(String overallEvaluation) {
    this.overallEvaluation = overallEvaluation;
  }

  public static class DimensionScore {
    private double score;
    private String evaluation;

    public double getScore() {
      return score;
    }

    public void setScore(double score) {
      this.score = score;
    }

    public String getEvaluation() {
      return evaluation;
    }

    public void setEvaluation(String evaluation) {
      this.evaluation = evaluation;
    }
  }
}
