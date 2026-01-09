package com.insurance.qa.repository;

import com.insurance.qa.entity.ModelConfig;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ModelConfigRepository extends JpaRepository<ModelConfig, Long> {
  Optional<ModelConfig> findByModelName(String modelName);

  Optional<ModelConfig> findByIsActiveTrue();
}
