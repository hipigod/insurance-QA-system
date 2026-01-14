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
              "新手客户",
              "需要简单解释和安抚。",
              "简单",
              "你是保险知识有限的新客户。请提出基础问题并表达轻微的价格顾虑。"),
          createRole(
              "理性客户",
              "会细问保障细节并比较产品。",
              "困难",
              "你是理性型客户。请询问保障范围、免责条款并进行产品对比。"),
          createRole(
              "质疑客户",
              "不信任并提出多种异议。",
              "专家",
              "你对保险持怀疑态度。请围绕价格、信任和理赔提出异议。"),
          createRole(
              "犹豫客户",
              "有兴趣但迟迟不决定。",
              "普通",
              "你对产品有兴趣但犹豫不决。请要求考虑时间并寻求更多安抚。")
      ));
    }

    if (productRepository.count() == 0) {
      productRepository.saveAll(Arrays.asList(
          createProduct(
              "重疾保障计划",
              "覆盖重大疾病，确诊给付。",
              "重疾",
              "覆盖 120 种重疾，确诊一次性给付。",
              "3000-10000 元/年",
              "18-50 岁成人",
              "确诊后豁免保费。"),
          createProduct(
              "医疗费用计划",
              "高保障医疗报销型产品。",
              "医疗",
              "覆盖普通与重大疾病医疗费用报销。",
              "300-1000 元/年",
              "0-60 岁人群",
              "覆盖进口药与住院费用。"),
          createProduct(
              "定期寿险计划",
              "性价比高的定期寿险。",
              "寿险",
              "身故或全残给付 100% 保额。",
              "500-2000 元/年",
              "20-50 岁在职人群",
              "核保简化，期限灵活。")
      ));
    }

    if (dimensionRepository.count() == 0) {
      dimensionRepository.saveAll(Arrays.asList(
          createDimension(
              "沟通表达",
              "清晰表达、倾听、同理心与响应速度。",
              25.0,
              "评估清晰表达、倾听、同理心与响应速度。"),
          createDimension(
              "销售有效性",
              "需求挖掘、价值传递、异议处理与成交。",
              25.0,
              "评估需求挖掘、价值传递、异议处理与成交。"),
          createDimension(
              "产品知识",
              "准确性与条款解释能力。",
              25.0,
              "评估产品讲解的准确性与清晰度。"),
          createDimension(
              "异议处理",
              "识别并解决异议的能力。",
              25.0,
              "评估异议识别与处理能力。")
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
