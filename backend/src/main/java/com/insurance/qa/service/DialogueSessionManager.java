package com.insurance.qa.service;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;
import org.springframework.web.socket.WebSocketSession;

@Service
public class DialogueSessionManager {
  private final Map<String, DialogueSession> sessions = new ConcurrentHashMap<>();
  private final Map<String, WebSocketSession> sockets = new ConcurrentHashMap<>();

  public DialogueSession createSession(
      Long roleId,
      Long productId,
      String roleName,
      String productName,
      String rolePrompt,
      String productInfo) {
    String sessionId = UUID.randomUUID().toString();
    DialogueSession session = new DialogueSession(
        sessionId,
        roleId,
        productId,
        roleName,
        productName,
        rolePrompt,
        productInfo);
    sessions.put(sessionId, session);
    return session;
  }

  public DialogueSession getSession(String sessionId) {
    return sessions.get(sessionId);
  }

  public Iterable<String> getSessionIds() {
    return sessions.keySet();
  }

  public void attachSocket(String sessionId, WebSocketSession webSocketSession) {
    sockets.put(sessionId, webSocketSession);
  }

  public WebSocketSession getSocket(String sessionId) {
    return sockets.get(sessionId);
  }

  public void removeSession(String sessionId) {
    sessions.remove(sessionId);
    sockets.remove(sessionId);
  }
}
