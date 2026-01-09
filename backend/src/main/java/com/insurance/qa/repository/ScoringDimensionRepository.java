package com.insurance.qa.repository;

import com.insurance.qa.entity.ScoringDimension;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ScoringDimensionRepository extends JpaRepository<ScoringDimension, Long> {
}
