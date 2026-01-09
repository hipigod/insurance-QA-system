package com.insurance.qa;

import com.insurance.qa.entity.ModelConfig;
import com.insurance.qa.repository.CustomerRoleRepository;
import com.insurance.qa.repository.ExcellentCaseRepository;
import com.insurance.qa.repository.InsuranceProductRepository;
import com.insurance.qa.repository.ModelConfigRepository;
import com.insurance.qa.repository.ScoringDimensionRepository;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
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
class AdminConfigControllerTest {
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

  @Autowired
  private ExcellentCaseRepository caseRepository;

  @Autowired
  private ModelConfigRepository modelRepository;

  @BeforeEach
  void setUp() {
    caseRepository.deleteAll();
    dimensionRepository.deleteAll();
    modelRepository.deleteAll();
    roleRepository.deleteAll();
    productRepository.deleteAll();
  }

  @Test
  void roleCrudFlowWorks() {
    Map<String, Object> payload = new HashMap<>();
    payload.put("name", "Demo Role");
    payload.put("system_prompt", "Prompt");
    payload.put("difficulty", "Easy");

    Map created = requireSuccess(post("/api/v1/roles", payload));
    Map createdData = (Map) created.get("data");
    if (createdData == null || createdData.get("id") == null) {
      throw new AssertionError("Expected role id");
    }

    Long roleId = ((Number) createdData.get("id")).longValue();
    Map updatePayload = new HashMap<>();
    updatePayload.put("description", "Updated");

    requireSuccess(put("/api/v1/roles/" + roleId, updatePayload));

    Map fetched = requireSuccess(get("/api/v1/roles/" + roleId));
    Map fetchedData = (Map) fetched.get("data");
    if (fetchedData == null || !"Updated".equals(fetchedData.get("description"))) {
      throw new AssertionError("Expected updated description");
    }

    Map deleted = requireSuccess(delete("/api/v1/roles/" + roleId));
    if (!Boolean.TRUE.equals(deleted.get("success"))) {
      throw new AssertionError("Expected delete success");
    }
  }

  @Test
  void productCrudFlowWorks() {
    Map<String, Object> payload = new HashMap<>();
    payload.put("name", "Demo Product");
    payload.put("product_type", "Medical");

    Map created = requireSuccess(post("/api/v1/products", payload));
    Map createdData = (Map) created.get("data");
    if (createdData == null || createdData.get("id") == null) {
      throw new AssertionError("Expected product id");
    }

    Long productId = ((Number) createdData.get("id")).longValue();
    Map updatePayload = new HashMap<>();
    updatePayload.put("description", "Updated");

    requireSuccess(put("/api/v1/products/" + productId, updatePayload));

    Map fetched = requireSuccess(get("/api/v1/products/" + productId));
    Map fetchedData = (Map) fetched.get("data");
    if (fetchedData == null || !"Updated".equals(fetchedData.get("description"))) {
      throw new AssertionError("Expected updated description");
    }

    Map deleted = requireSuccess(delete("/api/v1/products/" + productId));
    if (!Boolean.TRUE.equals(deleted.get("success"))) {
      throw new AssertionError("Expected delete success");
    }
  }

  @Test
  void dimensionWeightUpdateWorks() {
    Map<String, Object> payload = new HashMap<>();
    payload.put("name", "Communication");
    payload.put("weight", 25);

    Map created = requireSuccess(post("/api/v1/dimensions", payload));
    Map createdData = (Map) created.get("data");
    Long dimensionId = ((Number) createdData.get("id")).longValue();

    Map updatePayload = new HashMap<>();
    updatePayload.put("weight", 30);

    requireSuccess(put("/api/v1/dimensions/" + dimensionId, updatePayload));

    Map fetched = requireSuccess(get("/api/v1/dimensions/" + dimensionId));
    Map fetchedData = (Map) fetched.get("data");
    if (fetchedData == null || ((Number) fetchedData.get("weight")).intValue() != 30) {
      throw new AssertionError("Expected weight update");
    }
  }

  @Test
  void caseCrudFlowWorks() {
    Map<String, Object> payload = new HashMap<>();
    payload.put("weakness_type", "Opening");
    payload.put("case_content", "Sample case");

    Map created = requireSuccess(post("/api/v1/cases", payload));
    Map createdData = (Map) created.get("data");
    Long caseId = ((Number) createdData.get("id")).longValue();

    Map updatePayload = new HashMap<>();
    updatePayload.put("dialogue_node", "Intro");

    requireSuccess(put("/api/v1/cases/" + caseId, updatePayload));

    Map fetched = requireSuccess(get("/api/v1/cases/" + caseId));
    Map fetchedData = (Map) fetched.get("data");
    if (fetchedData == null || !"Intro".equals(fetchedData.get("dialogue_node"))) {
      throw new AssertionError("Expected dialogue_node update");
    }

    Map deleted = requireSuccess(delete("/api/v1/cases/" + caseId));
    if (!Boolean.TRUE.equals(deleted.get("success"))) {
      throw new AssertionError("Expected delete success");
    }
  }

  @Test
  void modelActivationWorks() {
    Map<String, Object> payload = new HashMap<>();
    payload.put("model_name", "model-a");
    payload.put("provider", "demo");
    payload.put("api_key", "key-a");
    payload.put("api_base", "https://api.example.com");
    payload.put("is_active", true);

    Map createdA = requireSuccess(post("/api/v1/models", payload));
    Map createdAData = (Map) createdA.get("data");
    Long modelAId = ((Number) createdAData.get("id")).longValue();

    Map<String, Object> payloadB = new HashMap<>();
    payloadB.put("model_name", "model-b");
    payloadB.put("provider", "demo");
    payloadB.put("api_key", "key-b");
    payloadB.put("api_base", "https://api.example.com");
    payloadB.put("is_active", true);

    Map createdB = requireSuccess(post("/api/v1/models", payloadB));
    Map createdBData = (Map) createdB.get("data");
    Long modelBId = ((Number) createdBData.get("id")).longValue();

    List<ModelConfig> models = modelRepository.findAll();
    long activeCount = models.stream().filter(ModelConfig::isActive).count();
    if (activeCount != 1) {
      throw new AssertionError("Expected exactly one active model");
    }

    requireSuccess(post("/api/v1/models/" + modelAId + "/activate", new HashMap<>()));

    ModelConfig modelA = modelRepository.findById(modelAId).orElseThrow();
    ModelConfig modelB = modelRepository.findById(modelBId).orElseThrow();
    if (!modelA.isActive() || modelB.isActive()) {
      throw new AssertionError("Expected model A active and model B inactive");
    }
  }

  private Map post(String path, Map<String, Object> payload) {
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    ResponseEntity<Map> response = restTemplate.postForEntity(
        "http://localhost:" + port + path,
        new HttpEntity<>(payload, headers),
        Map.class);
    return response.getBody();
  }

  private Map put(String path, Map<String, Object> payload) {
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    ResponseEntity<Map> response = restTemplate.exchange(
        "http://localhost:" + port + path,
        org.springframework.http.HttpMethod.PUT,
        new HttpEntity<>(payload, headers),
        Map.class);
    return response.getBody();
  }

  private Map get(String path) {
    ResponseEntity<Map> response = restTemplate.getForEntity(
        "http://localhost:" + port + path,
        Map.class);
    return response.getBody();
  }

  private Map delete(String path) {
    ResponseEntity<Map> response = restTemplate.exchange(
        "http://localhost:" + port + path,
        org.springframework.http.HttpMethod.DELETE,
        HttpEntity.EMPTY,
        Map.class);
    return response.getBody();
  }

  private Map requireSuccess(Map response) {
    if (response == null || !Boolean.TRUE.equals(response.get("success"))) {
      throw new AssertionError("Expected success response but got: " + response);
    }
    return response;
  }
}
