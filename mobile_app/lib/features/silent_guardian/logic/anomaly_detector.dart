import 'dart:async';
import 'dart:math';
import 'sensor_stream.dart';

class AnomalyDetector {
  final SensorStream _sensorStream;
  final Function() onDangerDetected;

  // --- CONFIGURATION THRESHOLDS ---
  // 3.5G is a standard threshold for a hard fall
  final double _fallImpactThreshold = 3.5 * 9.8; 
  // If movement is less than this, user is lying still
  final double _motionlessThreshold = 1.5; 
  
  // State Machine variables
  bool _possibleFallDetected = false;
  DateTime? _impactTime;
  Timer? _postFallCheckTimer;
  List<double> _recentReadings = [];

  AnomalyDetector({required this.onDangerDetected}) 
      : _sensorStream = SensorStream(onMovementDetected: (val) {});

  void startMonitoring() {
    print("🛡️ Silent Guardian: Active (Physics Mode)");
    
    final stream = SensorStream(onMovementDetected: (rawMagnitude) {
      _processSensorData(rawMagnitude);
    });
    
    stream.startListening();
  }

  void _processSensorData(double magnitude) {
    // 1. Maintain a buffer to smooth data (Simple Moving Average)
    _recentReadings.add(magnitude);
    if (_recentReadings.length > 10) _recentReadings.removeAt(0);
    double smoothedVal = _recentReadings.reduce((a, b) => a + b) / _recentReadings.length;

    // 2. PHASE 1: IMPACT DETECTION
    // If we see a huge spike (High G-Force)
    if (!_possibleFallDetected && smoothedVal > _fallImpactThreshold) {
      print("⚠️ High Impact Detected! (${smoothedVal.toStringAsFixed(1)})");
      _possibleFallDetected = true;
      _impactTime = DateTime.now();
      
      // Wait 10 seconds to see if they get up
      _schedulePostFallCheck();
    }
  }

  void _schedulePostFallCheck() {
    _postFallCheckTimer?.cancel();
    
    // Check status 10 seconds AFTER the impact
    _postFallCheckTimer = Timer(const Duration(seconds: 10), () {
      if (_isUserMotionless()) {
        print("🚨 CONFIRMED FALL: Impact + No Movement");
        onDangerDetected();
      } else {
        print("✅ False Alarm: User is moving again.");
        _possibleFallDetected = false; // Reset
      }
    });
  }

  // 3. PHASE 2: INACTIVITY CHECK
  // Are they moving right now?
  bool _isUserMotionless() {
    if (_recentReadings.isEmpty) return true;
    double currentAvg = _recentReadings.reduce((a, b) => a + b) / _recentReadings.length;
    
    // If average movement is very low (near gravity 9.8 or 0 depending on sensor type)
    // Note: userAccelerometer usually returns 0 for stillness.
    return currentAvg < _motionlessThreshold;
  }

  void stopMonitoring() {
    _sensorStream.stopListening();
    _postFallCheckTimer?.cancel();
  }
}