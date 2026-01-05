#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本 - 验证后端API功能
"""
import requests
import json
import sys
import io

# 设置stdout编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def test_api(endpoint, name):
    """测试API端点"""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ {name}: PASS (状态码: {response.status_code}, 数据条数: {len(data)})")
            return data, True
        else:
            print(f"✗ {name}: FAIL (状态码: {response.status_code})")
            return None, False
    except Exception as e:
        print(f"✗ {name}: FAIL (错误: {str(e)})")
        return None, False

def main():
    print("="*60)
    print("保险销售智能陪练系统 - API测试")
    print("="*60)

    results = {}

    # TC001: 后端启动测试
    print("\n【TC001: 后端启动测试】")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ 后端服务运行正常")
            results['TC001'] = 'PASS'
        else:
            print(f"✗ 后端服务异常 (状态码: {response.status_code})")
            results['TC001'] = 'FAIL'
    except Exception as e:
        print(f"✗ 后端服务无法访问 (错误: {str(e)})")
        results['TC001'] = 'FAIL'

    # TC003: 角色API测试
    print("\n【TC003: 角色API测试】")
    roles, passed = test_api("/api/roles/", "角色API")
    results['TC003'] = 'PASS' if passed else 'FAIL'
    if passed and roles:
        print(f"  角色列表:")
        for role in roles[:4]:
            print(f"    - {role['name']} ({role['difficulty']})")

    # TC004: 产品API测试
    print("\n【TC004: 产品API测试】")
    products, passed = test_api("/api/products/", "产品API")
    results['TC004'] = 'PASS' if passed else 'FAIL'
    if passed and products:
        print(f"  产品列表:")
        for product in products[:3]:
            print(f"    - {product['name']}")

    # TC009: 评分维度API测试 (Bug#1修复验证)
    print("\n【TC009: 评分维度API测试 - Bug#1修复验证】")
    dimensions, passed = test_api("/api/dimensions/", "评分维度API")
    results['TC009'] = 'PASS' if passed else 'FAIL'

    if passed and dimensions:
        print(f"  评分维度列表 (共{len(dimensions)}个):")
        expected_dimensions = ["需求挖掘", "产品说明", "异议处理", "促成能力"]
        actual_dimensions = [d['name'] for d in dimensions]

        for dim in dimensions:
            print(f"    - {dim['name']} (权重: {dim['weight']}%)")

        # 验证维度名称是否正确
        if set(actual_dimensions) == set(expected_dimensions):
            print("  ✓ Bug#1修复验证通过: 评分维度显示正确")
        else:
            print(f"  ✗ Bug#1修复验证失败: 预期维度 {expected_dimensions}, 实际 {actual_dimensions}")

    # TC010: 模型配置API测试 (Bug#2新增功能)
    print("\n【TC010: 模型配置API测试 - Bug#2新增功能】")
    try:
        # 尝试不同的路径
        urls_to_try = [
            "/api/models/",
            "/api/models/models/",
        ]

        model_response = None
        for url in urls_to_try:
            try:
                model_response = requests.get(f"{BASE_URL}{url}", timeout=5)
                if model_response.status_code == 200:
                    print(f"✓ 模型配置API路径: {url}")
                    break
            except:
                continue

        if model_response and model_response.status_code == 200:
            models = model_response.json()
            print(f"✓ 模型配置API: PASS (找到 {len(models)} 个模型)")
            results['TC010'] = 'PASS'

            if models:
                print(f"  模型列表:")
                for model in models:
                    status = "启用" if model.get('is_active') else "禁用"
                    print(f"    - {model['model_name']} ({model.get('provider', 'N/A')}) - {status}")
        else:
            print(f"✗ 模型配置API: FAIL (无法访问模型配置)")
            print("  原因: 后端路由配置问题 (main.py第47行)")
            results['TC010'] = 'FAIL'
    except Exception as e:
        print(f"✗ 模型配置API: FAIL (错误: {str(e)})")
        results['TC010'] = 'FAIL'

    # TC015: 优秀案例API测试
    print("\n【优秀案例API测试】")
    cases, passed = test_api("/api/cases/", "优秀案例API")
    results['TC015_API'] = 'PASS' if passed else 'FAIL'
    if passed and cases:
        print(f"  优秀案例数量: {len(cases)}")

    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    passed_count = sum(1 for v in results.values() if v == 'PASS')
    total_count = len(results)

    for test_id, result in results.items():
        status = "✓ PASS" if result == 'PASS' else "✗ FAIL"
        print(f"{test_id}: {status}")

    print(f"\n总计: {passed_count}/{total_count} 通过")

    # 返回退出码
    sys.exit(0 if passed_count == total_count else 1)

if __name__ == "__main__":
    main()
