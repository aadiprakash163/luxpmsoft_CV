import cv2
import numpy as np



def opencv_rotation(image, height, width, rot_angle):
    """
        This function returns left and right rotated images using 
        opencv library functions.
    """

    # Get rotation matrices for rotations
    center = (width/2, height/2)
    first_rotation_matrix = cv2.getRotationMatrix2D(center = center, angle = rot_angle, scale = 1)
    second_rotation_matrix = cv2.getRotationMatrix2D(center = center, angle = -1*rot_angle, scale = 1)

    # Get rotated images
    left_rotated_image = cv2.warpAffine(src = image, M = first_rotation_matrix, dsize = (width, height))
    right_rotated_image = cv2.warpAffine(src = image, M = second_rotation_matrix, dsize = (width, height))

    return left_rotated_image, right_rotated_image

def opencv_translation(image, height, width, x_shift, y_shift):
    """
        This function performs linear translation using opencv library functions
    """
    # Get the transformation matrices
    M_x = np.float32(([1, 0, x_shift], [0, 1, 0]))
    M_y = np.float32(([1, 0, 0], [0, 1, y_shift]))

    # Perform the shift
    x_shifted_image = cv2.warpAffine(image, M_x, (width, height))
    y_shifted_image = cv2.warpAffine(image, M_y, (width, height))

    return x_shifted_image, y_shifted_image


def modify_intensity(image, height, width):
    """
        This fucntion modifies the intensity of the image as per instructions
    """
    img = np.copy(image)
    # img = np.ones_like(image[:, :, 0])*150.0
    
    max_change = 50

    center_x = int(width/2)
    center_y = int(height/2)
    
    if center_x > max_change and center_y > max_change:
        # Get the extremes of the region
        x_min = center_x - max_change
        x_max = center_x + max_change
        y_min = center_y - max_change
        y_max = center_y + max_change                

        for i in range( y_min + 1, y_max):            
            for j in range(x_min + 1, x_max):
            	change_x = abs(center_x - j)
            	change_y = abs(center_y - i)
            	change = max_change-max(change_x, change_y)
            	img[i][j] = img[i][j] * (1+(change/100))            	
        return img
    else: 
        print("The image is not big enough to perform this operation!!!!")
        return img

    

    




if __name__ == "__main__":
    # Read the image
    image = cv2.imread('image.jpg')

    # Get height, width and center of the image
    height, width = image.shape[:2]
    
    print("Shape of the  given image is: ", height, width )    
    x_shift = int(width*0.25)
    y_shift = int(height*0.25)
    rot_angle = 90

    # Get the rotated images
    left_rot_image, right_rot_image = opencv_rotation(image, height, width, rot_angle)

    # Get the shifted images
    x_shifted_image, y_shifted_image = opencv_translation(image, height, width, x_shift, y_shift)

    # Get the images with modified intensity
    modified_intensity_image = modify_intensity(image, height, width)

    # Save the images obtained
    cv2.imwrite("left_rotation_image.jpg", left_rot_image)
    cv2.imwrite("right_rotation_image.jpg", right_rot_image)
    cv2.imwrite("x_shifted_image.jpg", x_shifted_image)
    cv2.imwrite("y_shifted_image.jpg", y_shifted_image)    
    cv2.imwrite("Modified_intensity.jpg", modified_intensity_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
