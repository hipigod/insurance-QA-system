package com.insurance.qa.controller;

import com.insurance.qa.dto.ApiResponse;
import com.insurance.qa.dto.CaseCreateRequest;
import com.insurance.qa.dto.CaseDto;
import com.insurance.qa.entity.ExcellentCase;
import com.insurance.qa.exception.ResourceNotFoundException;
import com.insurance.qa.repository.ExcellentCaseRepository;
import jakarta.validation.Valid;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/cases")
public class CaseController {
  private final ExcellentCaseRepository caseRepository;

  public CaseController(ExcellentCaseRepository caseRepository) {
    this.caseRepository = caseRepository;
  }

  @GetMapping
  public ApiResponse<List<CaseDto>> getCases() {
    List<CaseDto> cases = caseRepository.findAll().stream().map(this::toDto).collect(Collectors.toList());
    return ApiResponse.success(cases);
  }

  @GetMapping("/{id}")
  public ApiResponse<CaseDto> getCase(@PathVariable("id") Long id) {
    ExcellentCase caseItem = caseRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Case not found"));
    return ApiResponse.success(toDto(caseItem));
  }

  @PostMapping
  public ApiResponse<CaseDto> createCase(@Valid @RequestBody CaseCreateRequest request) {
    ExcellentCase caseItem = new ExcellentCase();
    caseItem.setWeaknessType(request.getWeaknessType());
    caseItem.setCaseContent(request.getCaseContent());
    caseItem.setDialogueNode(request.getDialogueNode());
    return ApiResponse.success(toDto(caseRepository.save(caseItem)));
  }

  @PutMapping("/{id}")
  public ApiResponse<CaseDto> updateCase(@PathVariable("id") Long id, @RequestBody CaseCreateRequest request) {
    ExcellentCase caseItem = caseRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Case not found"));

    if (request.getWeaknessType() != null) {
      caseItem.setWeaknessType(request.getWeaknessType());
    }
    if (request.getCaseContent() != null) {
      caseItem.setCaseContent(request.getCaseContent());
    }
    if (request.getDialogueNode() != null) {
      caseItem.setDialogueNode(request.getDialogueNode());
    }

    return ApiResponse.success(toDto(caseRepository.save(caseItem)));
  }

  @DeleteMapping("/{id}")
  public ApiResponse<Void> deleteCase(@PathVariable("id") Long id) {
    ExcellentCase caseItem = caseRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Case not found"));
    caseRepository.delete(caseItem);
    return ApiResponse.success(null, "Deleted");
  }

  private CaseDto toDto(ExcellentCase caseItem) {
    CaseDto dto = new CaseDto();
    dto.setId(caseItem.getId());
    dto.setWeaknessType(caseItem.getWeaknessType());
    dto.setCaseContent(caseItem.getCaseContent());
    dto.setDialogueNode(caseItem.getDialogueNode());
    return dto;
  }
}
