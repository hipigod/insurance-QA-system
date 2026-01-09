package com.insurance.qa.controller;

import com.insurance.qa.dto.ApiResponse;
import com.insurance.qa.dto.DimensionCreateRequest;
import com.insurance.qa.dto.DimensionDto;
import com.insurance.qa.dto.DimensionUpdateRequest;
import com.insurance.qa.entity.ScoringDimension;
import com.insurance.qa.exception.ResourceNotFoundException;
import com.insurance.qa.repository.ScoringDimensionRepository;
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
@RequestMapping("/api/v1/dimensions")
public class DimensionController {
  private final ScoringDimensionRepository dimensionRepository;

  public DimensionController(ScoringDimensionRepository dimensionRepository) {
    this.dimensionRepository = dimensionRepository;
  }

  @GetMapping
  public ApiResponse<List<DimensionDto>> getDimensions() {
    List<DimensionDto> dimensions = dimensionRepository.findAll().stream()
        .map(this::toDto).collect(Collectors.toList());
    return ApiResponse.success(dimensions);
  }

  @GetMapping("/{id}")
  public ApiResponse<DimensionDto> getDimension(@PathVariable("id") Long id) {
    ScoringDimension dimension = dimensionRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Dimension not found"));
    return ApiResponse.success(toDto(dimension));
  }

  @PostMapping
  public ApiResponse<DimensionDto> createDimension(@Valid @RequestBody DimensionCreateRequest request) {
    ScoringDimension dimension = new ScoringDimension();
    dimension.setName(request.getName());
    dimension.setDescription(request.getDescription());
    if (request.getWeight() != null) {
      dimension.setWeight(request.getWeight());
    }
    dimension.setEvaluationPrompt(request.getEvaluationPrompt());
    return ApiResponse.success(toDto(dimensionRepository.save(dimension)));
  }

  @PutMapping("/{id}")
  public ApiResponse<DimensionDto> updateDimension(
      @PathVariable("id") Long id,
      @RequestBody DimensionUpdateRequest request) {
    ScoringDimension dimension = dimensionRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Dimension not found"));

    if (request.getName() != null) {
      dimension.setName(request.getName());
    }
    if (request.getDescription() != null) {
      dimension.setDescription(request.getDescription());
    }
    if (request.getWeight() != null) {
      dimension.setWeight(request.getWeight());
    }
    if (request.getEvaluationPrompt() != null) {
      dimension.setEvaluationPrompt(request.getEvaluationPrompt());
    }

    return ApiResponse.success(toDto(dimensionRepository.save(dimension)));
  }

  @DeleteMapping("/{id}")
  public ApiResponse<Void> deleteDimension(@PathVariable("id") Long id) {
    ScoringDimension dimension = dimensionRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Dimension not found"));
    dimensionRepository.delete(dimension);
    return ApiResponse.success(null, "Deleted");
  }

  private DimensionDto toDto(ScoringDimension dimension) {
    DimensionDto dto = new DimensionDto();
    dto.setId(dimension.getId());
    dto.setName(dimension.getName());
    dto.setDescription(dimension.getDescription());
    dto.setWeight(dimension.getWeight());
    dto.setEvaluationPrompt(dimension.getEvaluationPrompt());
    return dto;
  }
}
