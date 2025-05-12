from PIL import Image, ImageOps
import numpy as np

def find_black_shadow_position(image, threshold=50):
    """
    找到主要图片中黑色阴影的中心位置。

    :param image: 主要图片的 PIL 图像对象
    :param threshold: 阈值，用于检测黑色区域
    :return: 黑色阴影的中心位置 (x, y)
    """
    # 转换为灰度图像
    grayscale_image = ImageOps.grayscale(image)
    grayscale_array = np.array(grayscale_image)

    # 找到低于阈值的黑色区域
    black_mask = grayscale_array < threshold
    black_indices = np.argwhere(black_mask)

    if black_indices.size == 0:
        print("未找到黑色阴影区域，使用默认位置 (0, 0)")
        return (0, 0)

    # 计算黑色区域的中心点
    center_y, center_x = black_indices.mean(axis=0).astype(int)
    return (center_x, center_y)

def merge_images(main_image_path, icon_image_path, output_path, position=None):
    """
    合并主要图片和小图标，并导出结果。

    :param main_image_path: 主要图片的路径
    :param icon_image_path: 小图标的路径
    :param output_path: 导出图片的路径
    :param position: 小图标在主要图片上的位置 (x, y)，如果为 None，则自动检测黑色阴影位置
    """
    # 打开主要图片和小图标
    main_image = Image.open(main_image_path).convert("RGBA")
    icon_image = Image.open(icon_image_path).convert("RGBA")

    # 调整小图标大小（可选）
    icon_image = icon_image.resize((30, 30))  # 调整为 30x30 大小

    # 自动检测黑色阴影位置
    if position is None:
        shadow_center = find_black_shadow_position(main_image)
        # 调整位置，使小图标的中心对齐到黑色阴影的中心
        position = (shadow_center[0] - icon_image.size[0] // 2, shadow_center[1] - icon_image.size[1] // 2)
        print(f"检测到的黑色阴影位置: {shadow_center}, 调整后的小图标粘贴位置: {position}")

    # 检查粘贴位置是否在主要图片范围内
    if position[0] < 0 or position[1] < 0 or position[0] + icon_image.size[0] > main_image.size[0] or position[1] + icon_image.size[1] > main_image.size[1]:
        print("警告：小图标粘贴位置超出主要图片范围！")
        return

    # 创建一个新的空白图层用于合并
    combined_image = Image.new("RGBA", main_image.size)
    combined_image.paste(main_image, (0, 0))  # 先粘贴主要图片
    combined_image.paste(icon_image, position, icon_image)  # 再粘贴小图标

    # 保存合并后的图片
    combined_image.save(output_path, format="PNG")
    print(f"图片已成功保存到 {output_path}")

if __name__ == "__main__":
    # 示例用法
    main_image_path = "1.png"  # 替换为干员合同图片路径
    icon_image_path = "2.png"  # 替换为你的干员小图标路径
    output_path = "3.png"    # 导出图片的路径

    # 自动检测黑色阴影位置
    merge_images(main_image_path, icon_image_path, output_path)
