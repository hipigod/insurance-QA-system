package com.insurance.qa;

import com.insurance.qa.entity.CustomerRole;
import com.insurance.qa.entity.InsuranceProduct;
import com.insurance.qa.repository.CustomerRoleRepository;
import com.insurance.qa.repository.InsuranceProductRepository;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
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
class RoleProductControllerTest {
  @LocalServerPort
  private int port;

  @Autowired
  private TestRestTemplate restTemplate;

  @Autowired
  private CustomerRoleRepository roleRepository;

  @Autowired
  private InsuranceProductRepository productRepository;

  @BeforeEach
  void setUp() {
    roleRepository.deleteAll();
    productRepository.deleteAll();

    CustomerRole role = new CustomerRole();
    role.setName("Test Role");
    role.setSystemPrompt("Test prompt");
    roleRepository.save(role);

    InsuranceProduct product = new InsuranceProduct();
    product.setName("Test Product");
    productRepository.save(product);
  }

  @Test
  void rolesListReturnsData() {
    ResponseEntity<Map> response = restTemplate.getForEntity(
        "http://localhost:" + port + "/api/v1/roles", Map.class);

    Map body = response.getBody();
    if (body == null || !Boolean.TRUE.equals(body.get("success"))) {
      throw new AssertionError("Expected success response");
    }

    List data = (List) body.get("data");
    if (data == null || data.isEmpty()) {
      throw new AssertionError("Expected roles data");
    }
  }

  @Test
  void productsListReturnsData() {
    ResponseEntity<Map> response = restTemplate.getForEntity(
        "http://localhost:" + port + "/api/v1/products", Map.class);

    Map body = response.getBody();
    if (body == null || !Boolean.TRUE.equals(body.get("success"))) {
      throw new AssertionError("Expected success response");
    }

    List data = (List) body.get("data");
    if (data == null || data.isEmpty()) {
      throw new AssertionError("Expected products data");
    }
  }
}
