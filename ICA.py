import cv2
import numpy as np
import argparse

def load_images(path_to_first_image, path_to_second_image):
    first_image = cv2.imread(path_to_first_image).astype(np.float32)
    second_image = cv2.imread(path_to_second_image).astype(np.float32)
    return first_image, second_image

argument_parser = argparse.ArgumentParser(description='Process image paths.')
argument_parser.add_argument('-img1', '--imagepath1', required=True, help='Path to the first input image')
argument_parser.add_argument('-img2', '--imagepath2', required=True, help='Path to the second input image')
arguments = argument_parser.parse_args()

def main():
    first_image_path = arguments.imagepath1
    second_image_path = arguments.imagepath2
    first_image, second_image = load_images(first_image_path, second_image_path)

    first_image = cv2.resize(first_image, (1024, 1024))
    second_image = cv2.resize(second_image, (1024, 1024))

    def calculate_theta(radius, angle, order):
        component_x = (radius ** 2) * np.sin(order * angle)
        component_y = (radius ** 2) * np.cos(order * angle)
        sum_x = component_x.sum()
        sum_y = component_y.sum()
        theta = (1 / order) * np.arctan2(sum_x, sum_y)
        return theta

    def calculate_scale(theta, img1, img2):
        scale_x = img1 * np.cos(theta) + img2 * np.sin(theta)
        scale_y = img1 * np.cos(theta - np.pi / 2) + img2 * np.sin(theta - np.pi / 2)
        sum_x = (scale_x ** 2).sum()
        sum_y = (scale_y ** 2).sum()
        scale_matrix = np.diag([1. / sum_x, 1. / sum_y])
        return scale_matrix

    def analyze_images(image1, image2):
        image1 -= image1.mean()
        image2 -= image2.mean()

        magnitude = image1 ** 2 + image2 ** 2
        phase = np.arctan2(image2, image1)

        theta_initial = calculate_theta(magnitude, phase, 2)
        inverse_rotation1 = np.array([[np.cos(theta_initial), -np.sin(theta_initial)],
                                      [np.sin(theta_initial), np.cos(theta_initial)]]).T

        scale_inverse = calculate_scale(theta_initial, image1, image2)

        theta_final = calculate_theta(magnitude, phase, 4)
        inverse_rotation2 = np.array([[np.cos(theta_final), -np.sin(theta_final)],
                                      [np.sin(theta_final), np.cos(theta_final)]]).T

        transformation_matrix = np.matmul(inverse_rotation2, np.matmul(scale_inverse, inverse_rotation1))

        return inverse_rotation1, scale_inverse, inverse_rotation2, transformation_matrix

    inverse_rotation1, scale_inverse, inverse_rotation2, transformation_matrix = analyze_images(first_image, second_image)
    combined_images = np.concatenate([first_image.reshape(1, -1), second_image.reshape(1, -1)], axis=0)
    transformed_images = np.matmul(transformation_matrix, combined_images)

    img1_transformed = transformed_images[0, :]
    img2_transformed = transformed_images[1, :]

    # Normalize and convert to 8-bit format
    img1_normalized, img2_normalized = img1_transformed - img1_transformed.min(), img2_transformed - img2_transformed.min()
    img1_normalized, img2_normalized = img1_normalized * 255. / img1_normalized.max(), img2_normalized * 255. / img2_normalized.max()

    final_img1 = img1_normalized.reshape(first_image.shape).clip(0, 255).astype(np.uint8)
    final_img2 = img2_normalized.reshape(second_image.shape).clip(0, 255).astype(np.uint8)

    cv2.imwrite('output-first.png', final_img1)
    cv2.imwrite('output-second.png', final_img2)

if __name__ == "__main__":
    main()
