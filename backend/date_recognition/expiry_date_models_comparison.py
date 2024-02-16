import os
from expiry_date import Expiry_Date_Recognition, date_patterns  # Import the necessary class and variables

# Function to calculate recognition accuracy
def calculate_accuracy(predictions, labels):
    correct_count = sum(pred == label for pred, label in zip(predictions, labels))
    total_count = len(labels)
    accuracy = correct_count / total_count * 100
    return accuracy

# List of variations for recog and detect
recog_variations = ['crnn_vgg16_bn', 'crnn_mobilenet_v3_small', 'crnn_mobilenet_v3_large']
detect_variations = ['db_resnet50', 'db_mobilenet_v3_large']

# Directory containing image and label files
dataset_dir = "expiry_date_dataset" # this is incorrect path 20231125, so:
dataset_dir = os.path.join(os.getcwd(), '..', '..', 'demo/expiry_date_dataset')

# Create a table to store accuracy results
accuracy_table = {}

# Iterate through each combination of recog and detect
for recog in recog_variations:
    for detect in detect_variations:
        # List all image files in the dataset directory
        image_files = [f for f in os.listdir(dataset_dir) if f.endswith(".jpg")]

        # List to store predictions and labels
        predictions = []
        labels = []

        # List to store incorrectly recognized images
        incorrectly_recognized_images = []

        # Iterate through each image file
        for image_file in image_files:
            # Construct the file paths for the image and label
            image_path = os.path.join(dataset_dir, image_file)
            label_path = os.path.join(dataset_dir, image_file.replace(".jpg", ".txt"))

            # Read the label from the corresponding text file
            with open(label_path, 'r') as label_file:
                true_label = label_file.read().strip()

            # Create an instance of Expiry_Date_Recognition for the current image
            exp_date_rec = Expiry_Date_Recognition(image_path, detect, recog, date_patterns)

            # Extract the date from the image
            predicted_date = exp_date_rec.extract_dates()

            # Append the true label and predicted date to the lists
            labels.append(true_label)
            predictions.append(predicted_date)

            # Check if the prediction does not match the true label
            if predicted_date != true_label:
                incorrectly_recognized_images.append({
                    "image_file": image_file,
                    "true_label": true_label,
                    "predicted_date": predicted_date
                })

        # Calculate recognition accuracy for the current combination
        accuracy = calculate_accuracy(predictions, labels)

        # Store accuracy in the table
        accuracy_table[(recog, detect)] = accuracy

# Print the accuracy table
print("\nAccuracy Table:")
print("Recog \t\t Detect \t Accuracy")
for (recog, detect), accuracy in accuracy_table.items():
    print(f"{recog} \t {detect} \t {accuracy:.2f}%")


# Print the incorrectly recognized images
#print("Incorrectly Recognized Images:")
#for img_info in incorrectly_recognized_images:
#    print(f"Image: {img_info['image_file']}, True Label: {img_info['true_label']}, Predicted Date: {img_info['predicted_date']}")
