package com.insurance.qa.controller;

import com.insurance.qa.dto.ApiResponse;
import com.insurance.qa.dto.ModelCreateRequest;
import com.insurance.qa.dto.ModelDto;
import com.insurance.qa.dto.ModelUpdateRequest;
import com.insurance.qa.entity.ModelConfig;
import com.insurance.qa.exception.BadRequestException;
import com.insurance.qa.exception.ResourceNotFoundException;
import com.insurance.qa.repository.ModelConfigRepository;
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
@RequestMapping("/api/v1/models")
public class ModelController {
  private final ModelConfigRepository modelRepository;

  public ModelController(ModelConfigRepository modelRepository) {
    this.modelRepository = modelRepository;
  }

  @GetMapping
  public ApiResponse<List<ModelDto>> getModels() {
    List<ModelDto> models = modelRepository.findAll().stream().map(this::toDto).collect(Collectors.toList());
    return ApiResponse.success(models);
  }

  @GetMapping("/{id}")
  public ApiResponse<ModelDto> getModel(@PathVariable("id") Long id) {
    ModelConfig modelConfig = modelRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Model config not found"));
    return ApiResponse.success(toDto(modelConfig));
  }

  @PostMapping
  public ApiResponse<ModelDto> createModel(@Valid @RequestBody ModelCreateRequest request) {
    if (modelRepository.findByModelName(request.getModelName()).isPresent()) {
      throw new BadRequestException("Model name already exists");
    }

    if (request.isActive()) {
      modelRepository.findAll().forEach(model -> {
        model.setActive(false);
        modelRepository.save(model);
      });
    }

    ModelConfig modelConfig = new ModelConfig();
    modelConfig.setModelName(request.getModelName());
    modelConfig.setProvider(request.getProvider());
    modelConfig.setApiKey(request.getApiKey());
    modelConfig.setApiBase(request.getApiBase());
    modelConfig.setActive(request.isActive());

    return ApiResponse.success(toDto(modelRepository.save(modelConfig)));
  }

  @PutMapping("/{id}")
  public ApiResponse<ModelDto> updateModel(@PathVariable("id") Long id, @RequestBody ModelUpdateRequest request) {
    ModelConfig modelConfig = modelRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Model config not found"));

    if (request.getModelName() != null) {
      modelConfig.setModelName(request.getModelName());
    }
    if (request.getProvider() != null) {
      modelConfig.setProvider(request.getProvider());
    }
    if (request.getApiKey() != null) {
      modelConfig.setApiKey(request.getApiKey());
    }
    if (request.getApiBase() != null) {
      modelConfig.setApiBase(request.getApiBase());
    }
    if (request.getIsActive() != null && request.getIsActive()) {
      modelRepository.findAll().forEach(model -> {
        model.setActive(false);
        modelRepository.save(model);
      });
      modelConfig.setActive(true);
    } else if (request.getIsActive() != null) {
      modelConfig.setActive(false);
    }

    return ApiResponse.success(toDto(modelRepository.save(modelConfig)));
  }

  @DeleteMapping("/{id}")
  public ApiResponse<Void> deleteModel(@PathVariable("id") Long id) {
    ModelConfig modelConfig = modelRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Model config not found"));
    modelRepository.delete(modelConfig);
    return ApiResponse.success(null, "Deleted");
  }

  @PostMapping("/{id}/activate")
  public ApiResponse<Void> activateModel(@PathVariable("id") Long id) {
    ModelConfig modelConfig = modelRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Model config not found"));

    modelRepository.findAll().forEach(model -> {
      model.setActive(false);
      modelRepository.save(model);
    });

    modelConfig.setActive(true);
    modelRepository.save(modelConfig);

    return ApiResponse.success(null, "Activated");
  }

  private ModelDto toDto(ModelConfig modelConfig) {
    ModelDto dto = new ModelDto();
    dto.setId(modelConfig.getId());
    dto.setModelName(modelConfig.getModelName());
    dto.setProvider(modelConfig.getProvider());
    dto.setApiKey(modelConfig.getApiKey());
    dto.setApiBase(modelConfig.getApiBase());
    dto.setActive(modelConfig.isActive());
    return dto;
  }
}
