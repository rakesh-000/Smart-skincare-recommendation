# Smart Skincare Recommendation and Routine Checker

## Overview

**Smart Skincare Recommendation and Routine Checker** is an AI-powered application designed to help users identify their skin type through image classification and receive personalized skincare recommendations. The system uses a Convolutional Neural Network (CNN) to classify skin images into four categories: Normal, Dry, Oily, and Acne-prone.

Based on the predicted skin type, the application provides suitable skincare suggestions to help users build a personalized skincare routine.

## Key Features

- **AI-Based Skin Classification:** Uses a trained CNN model to classify skin images.
- **Four Skin Categories:** Identifies Normal, Dry, Oily, and Acne-prone skin types.
- **Personalized Recommendations:** Provides skincare suggestions based on the predicted skin category.
- **Routine Checker:** Helps users review skincare routines based on their identified skin type.
- **Interactive User Interface:** Provides a user-friendly interface developed with React.js.
- **Image Processing:** Processes RGB images resized to 50 × 50 pixels before classification.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js |
| Programming Language | Python, JavaScript |
| Machine Learning | Convolutional Neural Network (CNN) |
| Image Processing | Image resizing and RGB preprocessing |
| Model File | `CNNF.model` |
| Development Tools | Git, GitHub, npm |

## How It Works

1. **Image Input:** The user provides a skin image through the application.
2. **Image Preprocessing:** The image is converted to RGB format and resized to 50 × 50 pixels.
3. **CNN Prediction:** The trained CNN model analyzes the processed image.
4. **Skin Type Classification:** The model predicts one of four skin categories.
5. **Recommendation Generation:** The application displays skincare suggestions based on the predicted category.
6. **Routine Checking:** Users can review their skincare routine against the suggested recommendations.

## Model Development

The project uses a Convolutional Neural Network (CNN) for image-based skin type classification.

### Model Details

- **Model Architecture:** Convolutional Neural Network
- **Input Image Size:** 50 × 50 pixels
- **Input Format:** RGB images
- **Classification Categories:**
  - Normal
  - Dry
  - Oily
  - Acne-prone
- **Data Augmentation:** Used to expand the training dataset and improve model generalization.
- **Saved Model:** `CNNF.model`

The model is trained to identify visual patterns in the input images and predict the corresponding skin category.

## Project Structure

The following is a suggested structure. Adjust the filenames and folders to match your actual repository.

```text
Smart-Skincare-Recommendation/
│
├── public/
│   └── assets/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── App.js
│   └── index.js
│
├── model/
│   └── CNNF.model
│
├── requirements.txt
├── package.json
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

Ensure the following tools are installed:

- Node.js and npm
- Python 3.x
- Git

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Smart-Skincare-Recommendation
```

Replace `<your-repository-url>` with your actual GitHub repository URL.

### 2. Install Frontend Dependencies

```bash
npm install
```

### 3. Install Python Dependencies

If your project includes a Python-based model inference module, install its dependencies using:

```bash
pip install -r requirements.txt
```

Ensure the required machine learning and image-processing libraries are listed in `requirements.txt`.

### 4. Run the Application

Start the React development server:

```bash
npm start
```

If the project uses Vite, run:

```bash
npm run dev
```

Use the command supported by your `package.json`. Start any separate model inference service if your project requires one.

## Example Use Case

A user uploads a skin image through the application.

- The image is preprocessed into the required input format.
- The CNN model predicts a skin category.
- The application displays the predicted category.
- Relevant skincare recommendations are presented to the user.
- The user can review the suggested routine and make informed skincare choices.

*Note: Predictions depend on image quality, lighting, dataset coverage, and model performance.*

## Potential Future Enhancements

- Integrate product recommendations based on skin type and user preferences.
- Add user profiles to save skincare routines and track changes over time.
- Improve classification accuracy using a larger and more diverse dataset.
- Add multilingual support for better accessibility.
- Deploy the application to a cloud platform for public access.
- Add model evaluation metrics such as accuracy, precision, recall, and F1-score.

## Limitations

- Image-based predictions may be affected by lighting, image quality, and other visual factors.
- The model classifies images into predefined categories and may not identify every individual's skin characteristics accurately.
- Recommendations are general informational suggestions and are not a substitute for professional dermatological advice.
- Model performance should be evaluated on independent test data before making accuracy claims.

## Disclaimer

This application is intended for educational and informational purposes only. It does not provide medical diagnoses or replace consultation with a qualified dermatologist.

## Author

**Rakesh Kumar V S**

B.Tech — Artificial Intelligence and Data Science

Sri Krishna College of Technology, Coimbatore

## License

Add an appropriate open-source license, such as the MIT License, if you intend to distribute the project under those terms.
