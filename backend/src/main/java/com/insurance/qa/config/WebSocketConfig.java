package com.insurance.qa.config;

import com.insurance.qa.ws.DialogueWebSocketHandler;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {
  private final DialogueWebSocketHandler dialogueWebSocketHandler;
  private final CorsConfig corsConfig;

  public WebSocketConfig(DialogueWebSocketHandler dialogueWebSocketHandler, CorsConfig corsConfig) {
    this.dialogueWebSocketHandler = dialogueWebSocketHandler;
    this.corsConfig = corsConfig;
  }

  @Override
  public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
    registry
        .addHandler(dialogueWebSocketHandler, "/ws/dialogue")
        .setAllowedOrigins(corsConfig.getAllowedOrigins());
  }
}
