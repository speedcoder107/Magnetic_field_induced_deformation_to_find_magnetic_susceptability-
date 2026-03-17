import os
import cv2

def process_images(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get list of image files in input folder
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Process each image
    for image_file in image_files:
        # Read image
        image_path = os.path.join(input_folder, image_file)
        img = cv2.imread(image_path)

        # Check each pixel and set red value to 255 if it's greater than 255
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                if img[y, x][2] > 200 and img[y, x][1] > 82 and img[y,x][0] > 120:  # Check red value
                    counter = 0
                    try:
                        if img[y, x+1][2] > 200 and img[y, x+1][1] > 82 and img[y,x+1][0] > 120:  # Check surrounding value
                            counter += 1
                        if img[y, x-1][2] > 200 and img[y, x-1][1] > 82 and img[y,x-1][0] > 120:  # Check surrounding value
                            counter += 1
                        if img[y+1, x+1][2] > 200 and img[y+1, x+1][1] > 82 and img[y+1,x+1][0] > 120:  # Check surrounding value
                            counter += 1
                        if img[y-1, x+1][2] > 200 and img[y-1, x+1][1] > 82 and img[y-1,x+1][0] > 120:  # Check surrounding value
                            counter += 1
                        if img[y+1, x][2] > 200 and img[y+1, x][1] > 82 and img[y+1,x][0] > 120:  # Check surrounding value
                            counter += 1
                        if img[y-1, x][2] > 200 and img[y-1, x][1] > 82 and img[y-1,x][0] > 120:  # Check surrounding value
                            counter += 1
                        if img[y-1, x-1][2] > 200 and img[y-1, x-1][1] > 82 and img[y-1,x-1][0] > 120:  # Check surrounding value
                            counter += 1
                        if img[y+1, x-1][2] > 200 and img[y+1, x-1][1] > 82 and img[y+1,x-1][0] > 120:  # Check surrounding value
                            counter += 1
                    except:
                        counter = 0
                    if counter > 3:
                            img[y, x] = [0, 0, 255]  # Set pixel to red
 
        # Write processed image to output folder
        output_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_path, img)

        print(f"Processed image: {image_file}")

# Example usage
input_folder = "sample"
output_folder = "output_sample"
process_images(input_folder, output_folder)