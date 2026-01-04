# Travel-Mate: Mobile App (Tourist Node)

This directory contains the mobile application source code for **Travel-Mate**, built using **Flutter**. This application serves as the "Silent Guardian" for tourists, providing offline AI safety features and real-time connectivity.

## 📋 Recent Changes & Implementation Status

The following changes and implementations have been made to this subfolder:

1.  **Project Scaffolding**: Initialized a new Flutter project targeting Android, iOS, and macOS.
2.  **Architecture Setup**: implemented a **Feature-First** folder structure to ensure scalability.
3.  **Dependency Integration**:
    *   Added `tflite_flutter` for offline Edge AI execution.
    *   Added `sensors_plus` for accessing accelerometer and gyroscope data.
    *   Added `geolocator` for location tracking.
    *   Added `flutter_background_service` for continuous monitoring.
4.  **Asset Configuration**: Configured `assets/` directory for UI images and TensorFlow Lite models.
5.  **Test Configuration**: Updated `test/widget_test.dart` to reflect the actual main entry point (`TravelMateApp`) instead of the default counter app.

## 📂 Folder Structure

The project follows a modular, feature-centric architecture:

### `lib/` (Source Code)
The core logic of the application resides here.

*   **`lib/main.dart`**: The entry point of the application. It initializes the app, themes, and routes to the Home Screen.
*   **`lib/core/`**: Contains shared utilities, constants, and services used globally across the app.
    *   **`lib/core/services/`**: logic for background services (e.g., ongoing safety monitoring) and hardware interfacing.
*   **`lib/features/`**: Contains self-contained modules for specific application features.
    *   **`lib/features/silent_guardian/`**: Logic for the Fall Detection and Safety Monitoring system.
        *   **`screens/`**: UI components specific to this feature (e.g., `SafetyCheckScreen`).

### `assets/` (Static Resources)
Static files bundled with the application.

*   **`assets/images/`**: App icons, logos, and UI graphics.
*   **`assets/tflite_models/`**: Pre-trained Machine Learning models (e.g., `.tflite` files) used by the Silent Guardian feature for offline inference.

### `test/` (Testing)
*   **`widget_test.dart`**: Integration/Widget tests to verify UI components render correctly. (Recently updated to match `TravelMateApp` structure).

### Native Platforms
*   **`android/`**: Android-specific configuration (Manifest, Gradle build scripts).
*   **`ios/`**: iOS-specific configuration (Info.plist, Xcode project).
*   **`macos/`**: macOS-specific configuration.

### Configuration Files
*   **`pubspec.yaml`**: The project manifest. Lists all dependencies, assets, fountains, and project metadata.
*   **`analysis_options.yaml`**: Linter validation rules to ensure code quality.
