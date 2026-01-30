package com.insurance.qa.ws;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.insurance.qa.dto.ScoringResponse;
import com.insurance.qa.dto.WsMessage;
import com.insurance.qa.entity.ScoringDimension;
import com.insurance.qa.repository.ScoringDimensionRepository;
import com.insurance.qa.service.AiService;
import com.insurance.qa.service.DialogueSession;
import com.insurance.qa.service.DialogueSessionManager;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

@Component
public class DialogueWebSocketHandler extends TextWebSocketHandler {
  private final DialogueSessionManager sessionManager;
  private final ScoringDimensionRepository dimensionRepository;
  private final AiService aiService;
  private final ObjectMapper objectMapper;

  public DialogueWebSocketHandler(
      DialogueSessionManager sessionManager,
      ScoringDimensionRepository dimensionRepository,
      AiService aiService,
      ObjectMapper objectMapper) {
    this.sessionManager = sessionManager;
    this.dimensionRepository = dimensionRepository;
    this.aiService = aiService;
    this.objectMapper = objectMapper;
  }

  @Override
  public void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
    WsMessage inbound = objectMapper.readValue(message.getPayload(), WsMessage.class);
    if (inbound.getType() == null) {
      sendError(session, inbound.getSessionId(), "Missing message type");
      return;
    }

    switch (inbound.getType()) {
      case "subscribe" -> handleSubscribe(session, inbound);
      case "chat" -> handleChat(session, inbound);
      case "end" -> handleEnd(session, inbound);
      case "ping" -> handlePing(session, inbound);
      default -> sendError(session, inbound.getSessionId(), "Unknown message type");
    }
  }

  @Override
  public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
    sessionManager.getSessionIds().forEach(sessionId -> {
      if (session.equals(sessionManager.getSocket(sessionId))) {
        sessionManager.removeSession(sessionId);
      }
    });
  }

  private void handlePing(WebSocketSession socket, WsMessage inbound) throws Exception {
    // 心跳检测，简单返回 pong 响应
    WsMessage pong = new WsMessage();
    pong.setType("pong");
    pong.setSessionId(inbound.getSessionId());
    pong.setTimestamp(inbound.getTimestamp());
    socket.sendMessage(new TextMessage(objectMapper.writeValueAsString(pong)));
  }

  private void handleSubscribe(WebSocketSession socket, WsMessage inbound) throws Exception {
    if (inbound.getSessionId() == null || inbound.getSessionId().isBlank()) {
      sendError(socket, null, "Missing sessionId");
      return;
    }
    DialogueSession dialogueSession = sessionManager.getSession(inbound.getSessionId());
    if (dialogueSession == null) {
      sendError(socket, inbound.getSessionId(), "Session not found");
      return;
    }
    sessionManager.attachSocket(inbound.getSessionId(), socket);
    WsMessage status = new WsMessage();
    status.setType("status");
    status.setSessionId(inbound.getSessionId());
    status.setStatus("subscribed");
    socket.sendMessage(new TextMessage(objectMapper.writeValueAsString(status)));
  }

  private void handleChat(WebSocketSession socket, WsMessage inbound) throws Exception {
    DialogueSession dialogueSession = getSessionOrError(socket, inbound.getSessionId());
    if (dialogueSession == null) {
      return;
    }

    String userMessage = inbound.getMessage() == null ? "" : inbound.getMessage();
    dialogueSession.addMessage("user", userMessage);

    sendStatus(socket, inbound.getSessionId(), "thinking");
    try {
      String reply = aiService.generateDialogueResponse(
          dialogueSession.getRolePrompt(),
          dialogueSession.getProductInfo(),
          dialogueSession.getDialogueHistory(),
          userMessage);
      dialogueSession.addMessage("assistant", reply);
      WsMessage outgoing = new WsMessage();
      outgoing.setType("message");
      outgoing.setSessionId(inbound.getSessionId());
      outgoing.setRole("assistant");
      outgoing.setContent(reply);
      socket.sendMessage(new TextMessage(objectMapper.writeValueAsString(outgoing)));
    } catch (Exception ex) {
      sendError(socket, inbound.getSessionId(), "AI service error");
    }
  }

  private void handleEnd(WebSocketSession socket, WsMessage inbound) throws Exception {
    DialogueSession dialogueSession = getSessionOrError(socket, inbound.getSessionId());
    if (dialogueSession == null) {
      return;
    }

    sendStatus(socket, inbound.getSessionId(), "scoring");

    try {
      List<ScoringDimension> dimensions = dimensionRepository.findAll();
      Map<String, Map<String, Object>> scoringDimensions = new HashMap<>();
      for (ScoringDimension dimension : dimensions) {
        Map<String, Object> config = new HashMap<>();
        config.put("weight", dimension.getWeight());
        config.put("prompt", dimension.getEvaluationPrompt() != null ? dimension.getEvaluationPrompt() : dimension.getDescription());
        scoringDimensions.put(dimension.getName(), config);
      }

      String dialogueText = dialogueSession.getDialogueHistory().stream()
          .map(item -> item.getRole() + ": " + item.getContent())
          .collect(Collectors.joining("\n"));

      ScoringResponse score = aiService.generateScoring(
          dialogueText,
          dialogueSession.getRoleName(),
          dialogueSession.getProductName(),
          scoringDimensions);

      WsMessage response = new WsMessage();
      response.setType("score");
      response.setSessionId(inbound.getSessionId());
      response.setData(score);
      socket.sendMessage(new TextMessage(objectMapper.writeValueAsString(response)));
      sessionManager.removeSession(inbound.getSessionId());
    } catch (Exception ex) {
      sendError(socket, inbound.getSessionId(), "Scoring failed");
    }
  }

  private DialogueSession getSessionOrError(WebSocketSession socket, String sessionId) throws Exception {
    if (sessionId == null || sessionId.isBlank()) {
      sendError(socket, null, "Missing sessionId");
      return null;
    }
    DialogueSession dialogueSession = sessionManager.getSession(sessionId);
    if (dialogueSession == null) {
      sendError(socket, sessionId, "Session not found");
      return null;
    }
    return dialogueSession;
  }

  private void sendStatus(WebSocketSession socket, String sessionId, String status) throws Exception {
    WsMessage message = new WsMessage();
    message.setType("status");
    message.setSessionId(sessionId);
    message.setStatus(status);
    socket.sendMessage(new TextMessage(objectMapper.writeValueAsString(message)));
  }

  private void sendError(WebSocketSession socket, String sessionId, String error) throws Exception {
    WsMessage message = new WsMessage();
    message.setType("error");
    message.setSessionId(sessionId);
    message.setMessage(error);
    socket.sendMessage(new TextMessage(objectMapper.writeValueAsString(message)));
  }
}
