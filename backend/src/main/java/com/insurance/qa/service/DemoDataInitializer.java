package com.insurance.qa.service;

import com.insurance.qa.entity.CustomerRole;
import com.insurance.qa.entity.InsuranceProduct;
import com.insurance.qa.entity.ScoringDimension;
import com.insurance.qa.repository.CustomerRoleRepository;
import com.insurance.qa.repository.InsuranceProductRepository;
import com.insurance.qa.repository.ScoringDimensionRepository;
import java.util.Arrays;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DemoDataInitializer implements CommandLineRunner {
  private final CustomerRoleRepository roleRepository;
  private final InsuranceProductRepository productRepository;
  private final ScoringDimensionRepository dimensionRepository;

  public DemoDataInitializer(
      CustomerRoleRepository roleRepository,
      InsuranceProductRepository productRepository,
      ScoringDimensionRepository dimensionRepository) {
    this.roleRepository = roleRepository;
    this.productRepository = productRepository;
    this.dimensionRepository = dimensionRepository;
  }

  @Override
  public void run(String... args) {
    if (roleRepository.count() == 0) {
      roleRepository.saveAll(Arrays.asList(
          createRole(
              "Beginner Customer",
              "Needs simple explanations and reassurance.",
              "Easy",
              "You are a new customer with limited insurance knowledge. Ask basic questions and express mild price concerns."),
          createRole(
              "Analytical Customer",
              "Asks detailed questions and compares products.",
              "Hard",
              "You are an analytical customer. Ask for coverage details, exclusions, and comparisons."),
          createRole(
              "Skeptical Customer",
              "Distrustful and raises multiple objections.",
              "Expert",
              "You are skeptical and distrustful. Raise objections about price, trust, and claims."),
          createRole(
              "Indecisive Customer",
              "Interested but hesitant to decide.",
              "Medium",
              "You are interested but hesitant. Ask for time to think and request more reassurance.")
      ));
    }

    if (productRepository.count() == 0) {
      productRepository.saveAll(Arrays.asList(
          createProduct(
              "Critical Illness Plan",
              "Covers major critical illnesses with lump-sum payout.",
              "Critical",
              "Covers 120 critical illnesses, lump-sum on diagnosis.",
              "3000-10000 per year",
              "Adults 18-50",
              "Includes waiver of premiums after diagnosis."),
          createProduct(
              "Medical Expense Plan",
              "High coverage medical plan with reimbursement.",
              "Medical",
              "General and serious illness medical reimbursements.",
              "300-1000 per year",
              "All ages 0-60",
              "Covers imported drugs and inpatient fees."),
          createProduct(
              "Term Life Plan",
              "Affordable term life coverage.",
              "Life",
              "Pays 100 percent sum assured on death or total disability.",
              "500-2000 per year",
              "Working adults 20-50",
              "Simple underwriting and flexible term options.")
      ));
    }

    if (dimensionRepository.count() == 0) {
      dimensionRepository.saveAll(Arrays.asList(
          createDimension(
              "Communication",
              "Clarity, listening, empathy, and responsiveness.",
              25.0,
              "Evaluate clarity, listening, empathy, and responsiveness."),
          createDimension(
              "Sales Effectiveness",
              "Needs discovery, value delivery, objection handling, closing.",
              25.0,
              "Evaluate discovery, value delivery, objection handling, and closing."),
          createDimension(
              "Product Knowledge",
              "Accuracy and ability to explain terms.",
              25.0,
              "Evaluate accuracy and clarity of product explanation."),
          createDimension(
              "Objection Handling",
              "Ability to identify and resolve objections.",
              25.0,
              "Evaluate identification and handling of objections.")
      ));
    }
  }

  private CustomerRole createRole(String name, String description, String difficulty, String prompt) {
    CustomerRole role = new CustomerRole();
    role.setName(name);
    role.setDescription(description);
    role.setDifficulty(difficulty);
    role.setSystemPrompt(prompt);
    return role;
  }

  private InsuranceProduct createProduct(
      String name,
      String description,
      String type,
      String coverage,
      String premiumRange,
      String target,
      String details) {
    InsuranceProduct product = new InsuranceProduct();
    product.setName(name);
    product.setDescription(description);
    product.setProductType(type);
    product.setCoverage(coverage);
    product.setPremiumRange(premiumRange);
    product.setTargetAudience(target);
    product.setDetailedInfo(details);
    return product;
  }

  private ScoringDimension createDimension(
      String name,
      String description,
      double weight,
      String prompt) {
    ScoringDimension dimension = new ScoringDimension();
    dimension.setName(name);
    dimension.setDescription(description);
    dimension.setWeight(weight);
    dimension.setEvaluationPrompt(prompt);
    return dimension;
  }
}
