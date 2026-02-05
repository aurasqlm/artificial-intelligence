import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_openml
from tensorflow.keras import layers, models

print("Loading MNIST dataset...")

mnist = fetch_openml('mnist_784', version=1)
X = mnist['data'].values.astype('float32') / 255.0
y = mnist['target'].astype(int)

X = X.reshape(-1, 28, 28, 1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Building CNN model...")

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("Training model...")
model.fit(
    X_train,
    y_train,
    epochs=5,
    batch_size=64,
    validation_split=0.1
)

test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_acc}")


def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.resize((28, 28))
    img_array = np.array(img)

    if img_array.mean() > 127:
        img_array = 255 - img_array

    img_array = img_array.astype('float32') / 255.0
    img_array = img_array.reshape(1, 28, 28, 1)

    return img_array, img


def predict_image(image_path):
    img_array, img_display = preprocess_image(image_path)

    prediction = np.argmax(model.predict(img_array), axis=1)[0]

    plt.imshow(img_display, cmap='gray')
    plt.title(f'Predicted Digit: {prediction}')
    plt.axis('off')
    plt.show()

    return prediction


def main():
    while True:
        img_path = input("Enter image file path or 'quit' to exit: ").strip()

        if img_path.lower() == 'quit':
            break

        try:
            predicted_digit = predict_image(img_path)
            print(f"The predicted digit is: {predicted_digit}")
        except Exception as e:
            print(f"Error processing image: {e}")


if __name__ == "__main__":
    main()
