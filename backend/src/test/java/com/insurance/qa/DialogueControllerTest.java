package com.insurance.qa;

import com.insurance.qa.dto.ScoringResponse;
import com.insurance.qa.entity.CustomerRole;
import com.insurance.qa.entity.InsuranceProduct;
import com.insurance.qa.repository.CustomerRoleRepository;
import com.insurance.qa.repository.InsuranceProductRepository;
import com.insurance.qa.repository.ScoringDimensionRepository;
import com.insurance.qa.service.AiService;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.TestPropertySource;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:sqlite:target/test.db",
    "spring.jpa.hibernate.ddl-auto=create-drop",
    "app.ai.api-key=test-key"
})
class DialogueControllerTest {
  @LocalServerPort
  private int port;

  @Autowired
  private TestRestTemplate restTemplate;

  @Autowired
  private CustomerRoleRepository roleRepository;

  @Autowired
  private InsuranceProductRepository productRepository;

  @Autowired
  private ScoringDimensionRepository dimensionRepository;

  @MockBean
  private AiService aiService;

  private CustomerRole role;
  private InsuranceProduct product;

  @BeforeEach
  void setUp() {
    dimensionRepository.deleteAll();
    roleRepository.deleteAll();
    productRepository.deleteAll();

    role = new CustomerRole();
    role.setName("Test Role");
    role.setSystemPrompt("Test prompt");
    roleRepository.save(role);

    product = new InsuranceProduct();
    product.setName("Test Product");
    productRepository.save(product);

    Mockito.when(aiService.generateDialogueResponse(
        Mockito.anyString(),
        Mockito.anyString(),
        Mockito.anyList(),
        Mockito.anyString()))
        .thenReturn("Hello");

    ScoringResponse scoringResponse = new ScoringResponse();
    scoringResponse.setTotalScore(90);
    scoringResponse.setDimensionScores(Collections.emptyMap());
    scoringResponse.setObjectionTags(Collections.emptyList());
    scoringResponse.setOverallEvaluation("Good job");

    Mockito.when(aiService.generateScoring(
        Mockito.anyString(),
        Mockito.anyString(),
        Mockito.anyString(),
        Mockito.anyMap()))
        .thenReturn(scoringResponse);
  }

  @Test
  void startDialogueReturnsSession() {
    Map<String, Object> payload = new HashMap<>();
    payload.put("role_id", role.getId());
    payload.put("product_id", product.getId());

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);

    ResponseEntity<Map> response = restTemplate.postForEntity(
        "http://localhost:" + port + "/api/v1/dialogues",
        new HttpEntity<>(payload, headers),
        Map.class);

    Map body = response.getBody();
    if (body == null || !Boolean.TRUE.equals(body.get("success"))) {
      throw new AssertionError("Expected success response");
    }

    Map data = (Map) body.get("data");
    if (data == null || data.get("session_id") == null) {
      throw new AssertionError("Expected session_id");
    }
  }

  @Test
  void scoreDialogueReturnsScore() {
    Map<String, Object> payload = new HashMap<>();
    payload.put("role_id", role.getId());
    payload.put("product_id", product.getId());
    payload.put("history", List.of());

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);

    ResponseEntity<Map> response = restTemplate.postForEntity(
        "http://localhost:" + port + "/api/v1/dialogues/score",
        new HttpEntity<>(payload, headers),
        Map.class);

    Map body = response.getBody();
    if (body == null || !Boolean.TRUE.equals(body.get("success"))) {
      throw new AssertionError("Expected success response");
    }

    Map data = (Map) body.get("data");
    if (data == null || data.get("total_score") == null) {
      throw new AssertionError("Expected total_score");
    }
  }
}
