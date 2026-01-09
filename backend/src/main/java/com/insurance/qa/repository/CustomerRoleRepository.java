package com.insurance.qa.repository;

import com.insurance.qa.entity.CustomerRole;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CustomerRoleRepository extends JpaRepository<CustomerRole, Long> {
}
