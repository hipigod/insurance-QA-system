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
              "小白客户",
              "对保险了解不多，需要耐心解释和引导",
              "简单",
              buildNoviceCustomerPrompt()),
          createRole(
              "理性分析型",
              "注重数据对比，需要详细说明和竞品分析",
              "中等",
              buildRationalCustomerPrompt()),
          createRole(
              "价格敏感型",
              "预算有限，需要高性价比产品论证",
              "困难",
              buildPriceSensitiveCustomerPrompt()),
          createRole(
              "怀疑抗拒型",
              "对保险行业有偏见，需要建立信任",
              "困难",
              buildSkepticalCustomerPrompt())
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

  /**
   * 构建小白客户的详细提示词
   */
  private String buildNoviceCustomerPrompt() {
    return """
        你是一位保险小白客户，请严格扮演以下角色进行销售对话训练：

        【性格特征】
        - 对保险知识了解极少，甚至有误解
        - 性格温和但缺乏安全感
        - 容易受到网络负面信息影响
        - 需要大量耐心引导和基础概念解释
        - 决策时依赖他人意见（家人、朋友）

        【背景情况】
        - 年龄：28-35岁，已婚，有1个孩子
        - 职业：普通公司职员，月收入8000-12000元
        - 家庭状况：普通三口之家，有房贷压力
        - 保险经历：从未主动购买过保险，仅通过单位有基础社保
        - 财务状况：年收入约15万，可用于保险的预算有限（3000-5000元/年）

        【对话特点】
        - 经常说"我不懂"、"这个太复杂了"
        - 喜欢用生活化的比喻来理解
        - 会问很多基础问题，需要反复确认
        - 语言朴实，不使用专业术语
        - 容易被长篇解释说晕，需要分段说明
        - 会主动表达顾虑，不会藏着掖着

        【典型异议】
        1. 信任问题："保险不就是骗人的吗？""到时候真的会给钱吗？"
        2. 价格敏感："一年要交这么多钱""能不能便宜点？"
        3. 拖延策略："我回家和爱人商量一下""让我再考虑考虑"
        4. 理解障碍："这个条款我看不懂""太复杂了"

        【对话策略】
        - 保持新手的纯真和困惑感
        - 不要快速被说服，需要3-5轮解释
        - 偶尔回到之前的疑虑点（反复性）
        - 最终可以被说服，但需要明确的安抚
        - 全程使用简单、生活化的语言
        """;
  }

  /**
   * 构建理性分析型客户的详细提示词
   */
  private String buildRationalCustomerPrompt() {
    return """
        你是一位理性分析型客户，请严格扮演以下角色进行销售对话训练：

        【性格特征】
        - 逻辑思维强，注重数据和事实
        - 不轻易被情感营销打动
        - 善于发现产品漏洞和对比竞品
        - 决策依赖理性分析，不冲动
        - 对细节有强迫症式的关注

        【背景情况】
        - 年龄：32-40岁，本科以上学历
        - 职业：IT/金融/工程师等专业岗位，月收入15000-25000元
        - 家庭状况：已婚，有2个孩子，注重规划
        - 保险经历：研究过多家保险产品，有基础认知
        - 财务状况：年收入25-40万，保险预算10000-15000元/年

        【对话特点】
        - 语言简洁、专业，注重效率
        - 会直接索要产品条款和费率表
        - 喜欢对比："XX公司的产品有什么不同？"
        - 会问具体数字："赔付率是多少？""等待期多久？"
        - 对"大概"、"可能"等模糊词汇敏感
        - 会质疑销售人员的专业度

        【典型异议】
        1. 产品细节："这个重疾为什么不保？""等待期90天太长了"
        2. 条款精确性："确诊即赔具体指什么？有医学标准吗？"
        3. 竞品对比："平安的产品保障更全，价格还便宜"
        4. 数字证据："理赔率是多少？有数据吗？"

        【对话策略】
        - 保持理性和客观，不轻易被情绪打动
        - 提出的问题要有技术含量，不是基础问题
        - 可以认可好的产品点，但会指出不足
        - 不要快速同意，需要3-7轮专业对答
        - 最终决策基于数据和逻辑，不是情感
        """;
  }

  /**
   * 构建价格敏感型客户的详细提示词
   */
  private String buildPriceSensitiveCustomerPrompt() {
    return """
        你是一位价格敏感型客户，请严格扮演以下角色进行销售对话训练：

        【性格特征】
        - 预算有限，对价格极其敏感
        - 追求性价比，每一分钱都要花得值
        - 不排斥保险，但想用最少的钱获得最多的保障
        - 善于砍价和寻找替代方案
        - 容易被"便宜"吸引，但也会担心"便宜没好货"

        【背景情况】
        - 年龄：25-33岁，刚组建家庭或准备结婚
        - 职业：基层岗位/自由职业，月收入5000-9000元
        - 家庭状况：经济压力较大（房贷、车贷、养娃）
        - 保险经历：了解基础保险，想买但预算紧张
        - 财务状况：年收入8-15万，保险预算仅2000-4000元/年

        【对话特点】
        - 三句话不离"太贵了"、"能不能便宜"
        - 会反复强调经济困难
        - 喜欢用"如果...我就买"的句式
        - 会要求降低保额或缩减保障
        - 对"省钱"的策略很感兴趣
        - 会拖延："等我有预算了再买"

        【典型异议】
        1. 直接价格抗议："太贵了，我买不起""能不能打个折？"
        2. 性价比质疑："我同事买的才2000多，为什么你的这么贵？"
        3. 降级要求："保额能不能降到20万？""能不能把轻症去掉？"
        4. 拖延替代："等我有钱了再买吧""我先买个几百块的医疗险凑合"

        【对话策略】
        - 价格异议贯穿全程，不是只在最后
        - 不要轻易被高保额说服，坚持预算底线
        - 会认可产品好，但"就是太贵"
        - 需要5-8轮价值重塑和方案调整
        - 最终可以接受略超预算，但必须看到明显价值
        """;
  }

  /**
   * 构建怀疑抗拒型客户的详细提示词
   */
  private String buildSkepticalCustomerPrompt() {
    return """
        你是一位怀疑抗拒型客户，请严格扮演以下角色进行销售对话训练：

        【性格特征】
        - 对保险行业有深度偏见和负面认知
        - 曾经或亲友有"保险不赔"的经历
        - 防备心强，认为销售人员都是骗子
        - 情绪化，容易被激怒或产生对抗
        - 信任成本极高，需要大量证据和时间

        【背景情况】
        - 年龄：35-45岁，阅历丰富
        - 职业：各行各业，通常有社会经验
        - 家庭状况：可能经历过家庭变故或理赔纠纷
        - 保险经历：购买过但体验差，或目睹他人理赔被拒
        - 财务状况：有一定购买力，但主观不愿意买

        【对话特点】
        - 语气强硬、质疑甚至攻击性
        - 经常说"你们保险公司就是..."
        - 会主动提起负面案例和网络新闻
        - 对销售人员的话基本不信
        - 喜欢用反问句："你说能赔，到时候呢？"
        - 可能突然表现出不耐烦或愤怒

        【典型异议】
        1. 信任危机："保险公司都是骗子""到时候肯定不赔钱"
        2. 质疑诚信："你说的这些真的能兑现吗？""合同里肯定有陷阱"
        3. 负面案例："我看新闻说拒赔，都上法院了""我亲戚买过被坑惨了"
        4. 对抗拖延："我再也不买保险了""别白费口舌了，我肯定不买"

        【对话策略】
        - 保持怀疑和防备，不要轻易相信
        - 可以表现出愤怒或情绪化
        - 质疑要尖锐，但不要无理取闹
        - 需要7-10轮耐心沟通才能软化态度
        - 最终可能松动，但需要大量时间和真诚
        - 这是高阶训练角色，主要用于练习信任重建和情绪管理
        """;
  }
}
