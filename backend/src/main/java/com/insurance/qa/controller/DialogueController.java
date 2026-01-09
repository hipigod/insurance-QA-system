package com.insurance.qa.controller;

import com.insurance.qa.dto.ApiResponse;
import com.insurance.qa.dto.DialogueStartRequest;
import com.insurance.qa.dto.DialogueStartResponse;
import com.insurance.qa.dto.ScoringRequest;
import com.insurance.qa.dto.ScoringResponse;
import com.insurance.qa.entity.CustomerRole;
import com.insurance.qa.entity.InsuranceProduct;
import com.insurance.qa.entity.ScoringDimension;
import com.insurance.qa.exception.ResourceNotFoundException;
import com.insurance.qa.repository.CustomerRoleRepository;
import com.insurance.qa.repository.InsuranceProductRepository;
import com.insurance.qa.repository.ScoringDimensionRepository;
import com.insurance.qa.service.AiService;
import com.insurance.qa.service.DialogueSession;
import com.insurance.qa.service.DialogueSessionManager;
import jakarta.validation.Valid;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/dialogues")
public class DialogueController {
  private final CustomerRoleRepository roleRepository;
  private final InsuranceProductRepository productRepository;
  private final ScoringDimensionRepository dimensionRepository;
  private final DialogueSessionManager sessionManager;
  private final AiService aiService;

  public DialogueController(
      CustomerRoleRepository roleRepository,
      InsuranceProductRepository productRepository,
      ScoringDimensionRepository dimensionRepository,
      DialogueSessionManager sessionManager,
      AiService aiService) {
    this.roleRepository = roleRepository;
    this.productRepository = productRepository;
    this.dimensionRepository = dimensionRepository;
    this.sessionManager = sessionManager;
    this.aiService = aiService;
  }

  @PostMapping
  public ApiResponse<DialogueStartResponse> startDialogue(@Valid @RequestBody DialogueStartRequest request) {
    CustomerRole role = roleRepository.findById(request.getRoleId())
        .orElseThrow(() -> new ResourceNotFoundException("Role not found"));
    InsuranceProduct product = productRepository.findById(request.getProductId())
        .orElseThrow(() -> new ResourceNotFoundException("Product not found"));

    String productInfo = buildProductInfo(product);
    DialogueSession session = sessionManager.createSession(
        role.getId(),
        product.getId(),
        role.getName(),
        product.getName(),
        role.getSystemPrompt(),
        productInfo);

    String greeting = aiService.generateDialogueResponse(
        role.getSystemPrompt(),
        productInfo,
        session.getDialogueHistory(),
        "");
    session.addMessage("assistant", greeting);

    DialogueStartResponse response = new DialogueStartResponse();
    response.setSessionId(session.getSessionId());
    response.setGreeting(greeting);
    response.setRoleName(role.getName());
    response.setProductName(product.getName());

    return ApiResponse.success(response);
  }

  @PostMapping("/score")
  public ApiResponse<ScoringResponse> scoreDialogue(@Valid @RequestBody ScoringRequest request) {
    CustomerRole role = roleRepository.findById(request.getRoleId())
        .orElseThrow(() -> new ResourceNotFoundException("Role not found"));
    InsuranceProduct product = productRepository.findById(request.getProductId())
        .orElseThrow(() -> new ResourceNotFoundException("Product not found"));

    List<ScoringDimension> dimensions = dimensionRepository.findAll();
    Map<String, Map<String, Object>> scoringDimensions = new HashMap<>();
    for (ScoringDimension dimension : dimensions) {
      Map<String, Object> config = new HashMap<>();
      config.put("weight", dimension.getWeight());
      config.put("prompt", dimension.getEvaluationPrompt() != null ? dimension.getEvaluationPrompt() : dimension.getDescription());
      scoringDimensions.put(dimension.getName(), config);
    }

    String dialogueText = "";
    if (request.getHistory() != null) {
      dialogueText = request.getHistory().stream()
          .map(item -> item.getRole() + ": " + item.getContent())
          .collect(Collectors.joining("\n"));
    }

    ScoringResponse result = aiService.generateScoring(
        dialogueText,
        role.getName(),
        product.getName(),
        scoringDimensions);

    return ApiResponse.success(result);
  }

  private String buildProductInfo(InsuranceProduct product) {
    StringBuilder builder = new StringBuilder();
    builder.append("Name: ").append(product.getName()).append("\n");
    if (product.getProductType() != null) {
      builder.append("Type: ").append(product.getProductType()).append("\n");
    }
    if (product.getDescription() != null) {
      builder.append("Description: ").append(product.getDescription()).append("\n");
    }
    if (product.getCoverage() != null) {
      builder.append("Coverage: ").append(product.getCoverage()).append("\n");
    }
    if (product.getPremiumRange() != null) {
      builder.append("Premium range: ").append(product.getPremiumRange()).append("\n");
    }
    if (product.getTargetAudience() != null) {
      builder.append("Target audience: ").append(product.getTargetAudience()).append("\n");
    }
    return builder.toString();
  }
}
