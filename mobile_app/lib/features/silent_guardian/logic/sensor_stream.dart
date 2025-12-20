import 'dart:async';
import 'dart:math';
import 'package:sensors_plus/sensors_plus.dart';

class SensorStream {
  // We use the UserAccelerometer (excludes gravity) for movement
  StreamSubscription? _accelSubscription;
  
  // Callback function to send data back to the detector
  final Function(double) onMovementDetected;

  SensorStream({required this.onMovementDetected});

  void startListening() {
    // Set update interval (Game interval is approx 20ms)
    // sensors_plus handles this automatically on most devices
    
    _accelSubscription = userAccelerometerEvents.listen((UserAccelerometerEvent event) {
      // Calculate total movement magnitude
      // Formula: sqrt(x^2 + y^2 + z^2)
      double magnitude = sqrt(pow(event.x, 2) + pow(event.y, 2) + pow(event.z, 2));
      
      // Send the magnitude to our detector
      onMovementDetected(magnitude);
    });
  }

  void stopListening() {
    _accelSubscription?.cancel();
  }
}