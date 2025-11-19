"""
生成测试数据脚本
用于快速测试训练流程（仅用于测试，不推荐用于生产环境）
"""
import os
from PIL import Image, ImageDraw, ImageFont
import random


def generate_test_image(class_name, index, output_dir):
    """生成一张简单的测试图片"""
    # 创建图片
    img = Image.new('RGB', (224, 224), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加一些文本和形状来模拟不同类型的文档
    colors = {
        'identity_card': (100, 150, 200),
        'utility_bill': (150, 200, 100),
        'bank_statement': (200, 100, 150),
        'address_proof': (200, 150, 100),
        'lease_agreement': (150, 100, 200),
        'other': (180, 180, 180)
    }
    
    color = colors.get(class_name, (128, 128, 128))
    
    # 绘制一些简单的形状和文本
    draw.rectangle([20, 20, 204, 204], outline=color, width=3)
    draw.rectangle([30, 30, 194, 194], fill=color, width=1)
    
    # 添加类别标签文本
    try:
        # 尝试使用默认字体
        font = ImageFont.load_default()
    except:
        font = None
    
    text = f"{class_name}\n#{index}"
    draw.text((60, 100), text, fill='white', font=font, align='center')
    
    # 添加一些随机变化
    for i in range(5):
        x1 = random.randint(40, 184)
        y1 = random.randint(50, 174)
        x2 = x1 + random.randint(10, 30)
        y2 = y1 + random.randint(5, 15)
        draw.rectangle([x1, y1, x2, y2], fill='white', outline='gray')
    
    # 保存图片
    filename = f"test_{class_name}_{index:03d}.png"
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, 'PNG')
    return filepath


def generate_test_dataset(output_dir='../data/processed', samples_per_class=10):
    """
    生成测试数据集
    
    Args:
        output_dir: 输出目录
        samples_per_class: 每个类别的样本数量
    """
    classes = [
        'identity_card',
        'utility_bill',
        'bank_statement',
        'address_proof',
        'lease_agreement',
        'other'
    ]
    
    print("生成测试数据...")
    print(f"每个类别生成 {samples_per_class} 张图片")
    print("⚠️  注意：这些是合成测试数据，仅用于验证训练流程")
    print()
    
    total = 0
    for class_name in classes:
        class_dir = os.path.join(output_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)
        
        for i in range(1, samples_per_class + 1):
            generate_test_image(class_name, i, class_dir)
            total += 1
        
        print(f"  ✓ {class_name:20s}: {samples_per_class} 张图片")
    
    print()
    print(f"总计生成: {total} 张测试图片")
    print(f"输出目录: {output_dir}")
    print()
    print("⚠️  警告：这些数据是合成的，仅用于测试训练流程！")
    print("   实际训练需要使用真实的文档图片数据。")


if __name__ == '__main__':
    import sys
    
    # 检查是否提供了参数
    if len(sys.argv) > 1:
        try:
            samples = int(sys.argv[1])
        except:
            samples = 10
    else:
        samples = 10
    
    generate_test_dataset(samples_per_class=samples)

