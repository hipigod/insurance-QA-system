package com.insurance.qa;

import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.TestPropertySource;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:sqlite:target/test.db",
    "spring.jpa.hibernate.ddl-auto=create-drop",
    "app.ai.api-key=test-key"
})
class HealthControllerTest {
  @LocalServerPort
  private int port;

  @Autowired
  private TestRestTemplate restTemplate;

  @Test
  void healthReturnsOk() {
    ResponseEntity<Map> response = restTemplate.getForEntity(
        "http://localhost:" + port + "/api/v1/health", Map.class);

    if (!response.getStatusCode().is2xxSuccessful()) {
      throw new AssertionError("Expected 200 but got " + response.getStatusCode());
    }

    Map body = response.getBody();
    if (body == null || !Boolean.TRUE.equals(body.get("success"))) {
      throw new AssertionError("Expected success response");
    }

    Map data = (Map) body.get("data");
    if (data == null || !"healthy".equals(data.get("status"))) {
      throw new AssertionError("Expected healthy status");
    }
  }
}
