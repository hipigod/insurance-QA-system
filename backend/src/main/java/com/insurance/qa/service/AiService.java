package com.insurance.qa.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.insurance.qa.config.AppProperties;
import com.insurance.qa.dto.ChatMessageDto;
import com.insurance.qa.dto.ScoringResponse;
import com.insurance.qa.dto.ScoringResponse.DimensionScore;
import com.insurance.qa.entity.ModelConfig;
import com.insurance.qa.repository.ModelConfigRepository;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class AiService {
  private final WebClient webClient;
  private final AppProperties appProperties;
  private final ModelConfigRepository modelConfigRepository;
  private final ObjectMapper objectMapper;

  public AiService(
      WebClient webClient,
      AppProperties appProperties,
      ModelConfigRepository modelConfigRepository,
      ObjectMapper objectMapper) {
    this.webClient = webClient;
    this.appProperties = appProperties;
    this.modelConfigRepository = modelConfigRepository;
    this.objectMapper = objectMapper;
  }

  public String generateDialogueResponse(
      String rolePrompt,
      String productInfo,
      List<ChatMessageDto> history,
      String userMessage) {
    List<ChatMessage> messages = new ArrayList<>();
    messages.add(new ChatMessage("system", buildDialogueSystemPrompt(rolePrompt, productInfo)));

    int start = Math.max(0, history.size() - 5);
    for (int i = start; i < history.size(); i++) {
      ChatMessageDto item = history.get(i);
      if (!"system".equals(item.getRole())) {
        messages.add(new ChatMessage(item.getRole(), item.getContent()));
      }
    }

    String messageToSend = userMessage == null || userMessage.isBlank() ? "Start the conversation." : userMessage;
    messages.add(new ChatMessage("user", messageToSend));

    ChatCompletionRequest request = new ChatCompletionRequest();
    request.setModel(resolveModel());
    request.setMessages(messages);
    request.setTemperature(appProperties.getAi().getTemperature());
    request.setMaxTokens(500);

    try {
      ChatCompletionResponse response = callChatCompletion(request);
      if (response == null || response.getChoices().isEmpty()) {
        return "Sorry, I cannot respond right now. Please try again.";
      }
      return response.getChoices().get(0).getMessage().getContent();
    } catch (Exception ex) {
      return "Sorry, I cannot respond right now. Please try again.";
    }
  }

  public ScoringResponse generateScoring(
      String dialogueText,
      String roleName,
      String productName,
      Map<String, Map<String, Object>> scoringDimensions) {
    String prompt = buildScoringPrompt(dialogueText, roleName, productName, scoringDimensions);

    ChatCompletionRequest request = new ChatCompletionRequest();
    request.setModel(resolveModel());
    List<ChatMessage> messages = new ArrayList<>();
    messages.add(new ChatMessage("system", "You are an expert insurance sales coach."));
    messages.add(new ChatMessage("user", prompt));
    request.setMessages(messages);
    request.setTemperature(0.3);
    request.setMaxTokens(2000);

    try {
      ChatCompletionResponse response = callChatCompletion(request);
      if (response == null || response.getChoices().isEmpty()) {
        throw new IllegalStateException("Empty AI response");
      }
      String raw = response.getChoices().get(0).getMessage().getContent();
      return parseScoringResponse(raw);
    } catch (Exception ex) {
      throw new IllegalStateException("Scoring failed");
    }
  }

  private ChatCompletionResponse callChatCompletion(ChatCompletionRequest request) {
    AiConfig config = resolveAiConfig();
    if (config.apiKey == null || config.apiKey.isBlank()) {
      throw new IllegalStateException("Missing API key");
    }
    return webClient
        .post()
        .uri(config.baseUrl + "/chat/completions")
        .header(HttpHeaders.AUTHORIZATION, "Bearer " + config.apiKey)
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(request)
        .retrieve()
        .bodyToMono(ChatCompletionResponse.class)
        .block(Duration.ofSeconds(appProperties.getAi().getTimeoutSeconds()));
  }

  private AiConfig resolveAiConfig() {
    Optional<ModelConfig> active = modelConfigRepository.findByIsActiveTrue();
    if (active.isPresent()) {
      ModelConfig modelConfig = active.get();
      String apiKey = modelConfig.getApiKey() == null || modelConfig.getApiKey().isBlank()
          ? appProperties.getAi().getApiKey()
          : modelConfig.getApiKey();
      String apiBase = modelConfig.getApiBase() == null || modelConfig.getApiBase().isBlank()
          ? appProperties.getAi().getApiBase()
          : modelConfig.getApiBase();
      String model = modelConfig.getModelName() == null || modelConfig.getModelName().isBlank()
          ? appProperties.getAi().getModel()
          : modelConfig.getModelName();
      return new AiConfig(model, apiKey, apiBase);
    }
    return new AiConfig(appProperties.getAi().getModel(), appProperties.getAi().getApiKey(), appProperties.getAi().getApiBase());
  }

  private String resolveModel() {
    return resolveAiConfig().model;
  }

  private String buildDialogueSystemPrompt(String rolePrompt, String productInfo) {
    return "You are simulating an insurance customer for sales training. "
        + "Stay in character, respond naturally, and raise realistic objections. "
        + "Keep replies under 150 words and respond in Chinese.\n\n"
        + "Role profile:\n" + rolePrompt + "\n\n"
        + "Product info:\n" + productInfo;
  }

  private String buildScoringPrompt(
      String dialogueText,
      String roleName,
      String productName,
      Map<String, Map<String, Object>> scoringDimensions) {
    StringBuilder builder = new StringBuilder();
    builder.append("Evaluate the sales performance.\n\n");
    builder.append("Scoring dimensions and weights:\n");
    int index = 1;
    for (Map.Entry<String, Map<String, Object>> entry : scoringDimensions.entrySet()) {
      builder.append("Dimension ").append(index++).append(": ")
          .append(entry.getKey()).append(" (weight ")
          .append(entry.getValue().get("weight")).append("%)\n");
      Object prompt = entry.getValue().get("prompt");
      if (prompt != null) {
        builder.append(prompt).append("\n");
      }
      builder.append("\n");
    }

    builder.append("Role: ").append(roleName).append("\n");
    builder.append("Product: ").append(productName).append("\n\n");
    builder.append("Dialogue transcript:\n").append(dialogueText).append("\n\n");
    builder.append("Output JSON only with fields: total_score, dimension_scores, objection_tags, overall_evaluation.\n");
    builder.append("dimension_scores should map each dimension name to { score, evaluation }.\n");
    builder.append("objection_tags should be a list of strings.\n");
    return builder.toString();
  }

  private ScoringResponse parseScoringResponse(String rawText) {
    String text = rawText.trim();
    if (text.contains("```")) {
      String[] parts = text.split("```");
      if (parts.length >= 2) {
        text = parts[1].replace("json", "").trim();
      }
    }

    Map<String, Object> result;
    try {
      result = objectMapper.readValue(text, new TypeReference<Map<String, Object>>() {});
    } catch (Exception ex) {
      throw new IllegalStateException("Invalid scoring JSON");
    }

    ScoringResponse response = new ScoringResponse();
    Object totalScore = result.get("total_score");
    if (totalScore instanceof Number) {
      response.setTotalScore(((Number) totalScore).doubleValue());
    }

    Map<String, DimensionScore> dimensionScores = new HashMap<>();
    Object dimensionScoresRaw = result.get("dimension_scores");
    if (dimensionScoresRaw instanceof Map<?, ?> map) {
      for (Map.Entry<?, ?> entry : map.entrySet()) {
        if (!(entry.getKey() instanceof String)) {
          continue;
        }
        DimensionScore score = new DimensionScore();
        if (entry.getValue() instanceof Map<?, ?> scoreMap) {
          Object scoreValue = scoreMap.get("score");
          Object evaluationValue = scoreMap.get("evaluation");
          if (scoreValue instanceof Number) {
            score.setScore(((Number) scoreValue).doubleValue());
          }
          if (evaluationValue != null) {
            score.setEvaluation(String.valueOf(evaluationValue));
          }
        }
        dimensionScores.put((String) entry.getKey(), score);
      }
    }
    response.setDimensionScores(dimensionScores);

    Object objectionTagsRaw = result.get("objection_tags");
    if (objectionTagsRaw instanceof List<?> list) {
      List<String> tags = new ArrayList<>();
      for (Object item : list) {
        tags.add(String.valueOf(item));
      }
      response.setObjectionTags(tags);
    }

    Object overallEvaluation = result.get("overall_evaluation");
    if (overallEvaluation != null) {
      response.setOverallEvaluation(String.valueOf(overallEvaluation));
    }

    return response;
  }

  private static class AiConfig {
    private final String model;
    private final String apiKey;
    private final String baseUrl;

    private AiConfig(String model, String apiKey, String baseUrl) {
      this.model = model;
      this.apiKey = apiKey;
      this.baseUrl = baseUrl;
    }
  }

  public static class ChatCompletionRequest {
    private String model;
    private List<ChatMessage> messages;
    private double temperature;
    private int maxTokens;

    public String getModel() {
      return model;
    }

    public void setModel(String model) {
      this.model = model;
    }

    public List<ChatMessage> getMessages() {
      return messages;
    }

    public void setMessages(List<ChatMessage> messages) {
      this.messages = messages;
    }

    public double getTemperature() {
      return temperature;
    }

    public void setTemperature(double temperature) {
      this.temperature = temperature;
    }

    public int getMaxTokens() {
      return maxTokens;
    }

    public void setMaxTokens(int maxTokens) {
      this.maxTokens = maxTokens;
    }
  }

  public static class ChatCompletionResponse {
    private List<Choice> choices;

    public List<Choice> getChoices() {
      return choices;
    }

    public void setChoices(List<Choice> choices) {
      this.choices = choices;
    }

    public static class Choice {
      private ChatMessage message;

      public ChatMessage getMessage() {
        return message;
      }

      public void setMessage(ChatMessage message) {
        this.message = message;
      }
    }
  }

  public static class ChatMessage {
    private String role;
    private String content;

    public ChatMessage() {
    }

    public ChatMessage(String role, String content) {
      this.role = role;
      this.content = content;
    }

    public String getRole() {
      return role;
    }

    public void setRole(String role) {
      this.role = role;
    }

    public String getContent() {
      return content;
    }

    public void setContent(String content) {
      this.content = content;
    }
  }
}
