package com.insurance.qa.controller;

import com.insurance.qa.dto.ApiResponse;
import com.insurance.qa.dto.RoleCreateRequest;
import com.insurance.qa.dto.RoleDto;
import com.insurance.qa.dto.RoleUpdateRequest;
import com.insurance.qa.entity.CustomerRole;
import com.insurance.qa.exception.ResourceNotFoundException;
import com.insurance.qa.repository.CustomerRoleRepository;
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
@RequestMapping("/api/v1/roles")
public class RoleController {
  private final CustomerRoleRepository roleRepository;

  public RoleController(CustomerRoleRepository roleRepository) {
    this.roleRepository = roleRepository;
  }

  @GetMapping
  public ApiResponse<List<RoleDto>> getRoles() {
    List<RoleDto> roles = roleRepository.findAll().stream().map(this::toDto).collect(Collectors.toList());
    return ApiResponse.success(roles);
  }

  @GetMapping("/{id}")
  public ApiResponse<RoleDto> getRole(@PathVariable("id") Long id) {
    CustomerRole role = roleRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Role not found"));
    return ApiResponse.success(toDto(role));
  }

  @PostMapping
  public ApiResponse<RoleDto> createRole(@Valid @RequestBody RoleCreateRequest request) {
    CustomerRole role = new CustomerRole();
    role.setName(request.getName());
    role.setDescription(request.getDescription());
    role.setDifficulty(request.getDifficulty());
    role.setSystemPrompt(request.getSystemPrompt());
    return ApiResponse.success(toDto(roleRepository.save(role)));
  }

  @PutMapping("/{id}")
  public ApiResponse<RoleDto> updateRole(@PathVariable("id") Long id, @RequestBody RoleUpdateRequest request) {
    CustomerRole role = roleRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Role not found"));

    if (request.getName() != null) {
      role.setName(request.getName());
    }
    if (request.getDescription() != null) {
      role.setDescription(request.getDescription());
    }
    if (request.getDifficulty() != null) {
      role.setDifficulty(request.getDifficulty());
    }
    if (request.getSystemPrompt() != null) {
      role.setSystemPrompt(request.getSystemPrompt());
    }

    return ApiResponse.success(toDto(roleRepository.save(role)));
  }

  @DeleteMapping("/{id}")
  public ApiResponse<Void> deleteRole(@PathVariable("id") Long id) {
    CustomerRole role = roleRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Role not found"));
    roleRepository.delete(role);
    return ApiResponse.success(null, "Deleted");
  }

  private RoleDto toDto(CustomerRole role) {
    RoleDto dto = new RoleDto();
    dto.setId(role.getId());
    dto.setName(role.getName());
    dto.setDescription(role.getDescription());
    dto.setDifficulty(role.getDifficulty());
    dto.setSystemPrompt(role.getSystemPrompt());
    return dto;
  }
}
