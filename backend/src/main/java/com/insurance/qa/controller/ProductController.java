package com.insurance.qa.controller;

import com.insurance.qa.dto.ApiResponse;
import com.insurance.qa.dto.ProductCreateRequest;
import com.insurance.qa.dto.ProductDto;
import com.insurance.qa.dto.ProductUpdateRequest;
import com.insurance.qa.entity.InsuranceProduct;
import com.insurance.qa.exception.ResourceNotFoundException;
import com.insurance.qa.repository.InsuranceProductRepository;
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
@RequestMapping("/api/v1/products")
public class ProductController {
  private final InsuranceProductRepository productRepository;

  public ProductController(InsuranceProductRepository productRepository) {
    this.productRepository = productRepository;
  }

  @GetMapping
  public ApiResponse<List<ProductDto>> getProducts() {
    List<ProductDto> products = productRepository.findAll().stream().map(this::toDto).collect(Collectors.toList());
    return ApiResponse.success(products);
  }

  @GetMapping("/{id}")
  public ApiResponse<ProductDto> getProduct(@PathVariable("id") Long id) {
    InsuranceProduct product = productRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Product not found"));
    return ApiResponse.success(toDto(product));
  }

  @PostMapping
  public ApiResponse<ProductDto> createProduct(@Valid @RequestBody ProductCreateRequest request) {
    InsuranceProduct product = new InsuranceProduct();
    product.setName(request.getName());
    product.setDescription(request.getDescription());
    product.setProductType(request.getProductType());
    product.setCoverage(request.getCoverage());
    product.setPremiumRange(request.getPremiumRange());
    product.setTargetAudience(request.getTargetAudience());
    product.setDetailedInfo(request.getDetailedInfo());
    return ApiResponse.success(toDto(productRepository.save(product)));
  }

  @PutMapping("/{id}")
  public ApiResponse<ProductDto> updateProduct(@PathVariable("id") Long id, @RequestBody ProductUpdateRequest request) {
    InsuranceProduct product = productRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Product not found"));

    if (request.getName() != null) {
      product.setName(request.getName());
    }
    if (request.getDescription() != null) {
      product.setDescription(request.getDescription());
    }
    if (request.getProductType() != null) {
      product.setProductType(request.getProductType());
    }
    if (request.getCoverage() != null) {
      product.setCoverage(request.getCoverage());
    }
    if (request.getPremiumRange() != null) {
      product.setPremiumRange(request.getPremiumRange());
    }
    if (request.getTargetAudience() != null) {
      product.setTargetAudience(request.getTargetAudience());
    }
    if (request.getDetailedInfo() != null) {
      product.setDetailedInfo(request.getDetailedInfo());
    }

    return ApiResponse.success(toDto(productRepository.save(product)));
  }

  @DeleteMapping("/{id}")
  public ApiResponse<Void> deleteProduct(@PathVariable("id") Long id) {
    InsuranceProduct product = productRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Product not found"));
    productRepository.delete(product);
    return ApiResponse.success(null, "Deleted");
  }

  private ProductDto toDto(InsuranceProduct product) {
    ProductDto dto = new ProductDto();
    dto.setId(product.getId());
    dto.setName(product.getName());
    dto.setDescription(product.getDescription());
    dto.setProductType(product.getProductType());
    dto.setCoverage(product.getCoverage());
    dto.setPremiumRange(product.getPremiumRange());
    dto.setTargetAudience(product.getTargetAudience());
    dto.setDetailedInfo(product.getDetailedInfo());
    return dto;
  }
}
