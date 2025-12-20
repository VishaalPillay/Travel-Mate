import 'package:flutter/material.dart';
import 'package:vibration/vibration.dart';
import '../logic/anomaly_detector.dart';

class SafetyCheckScreen extends StatefulWidget {
  const SafetyCheckScreen({super.key});

  @override
  State<SafetyCheckScreen> createState() => _SafetyCheckScreenState();
}

class _SafetyCheckScreenState extends State<SafetyCheckScreen> {
  late AnomalyDetector _detector;
  bool _isDangerMode = false;

  @override
  void initState() {
    super.initState();
    // Initialize the AI Detector
    _detector = AnomalyDetector(onDangerDetected: _triggerAlert);
    _detector.startMonitoring();
  }

  void _triggerAlert() async {
    setState(() {
      _isDangerMode = true;
    });
    
    // Vibrate phone to wake user up
    if (await Vibration.hasVibrator() ?? false) {
      Vibration.vibrate(pattern: [500, 1000, 500, 1000]);
    }
  }

  void _markSafe() {
    setState(() {
      _isDangerMode = false;
    });
    // Restart monitoring
    _detector.startMonitoring();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Silent Guardian (Active)")),
      body: Center(
        child: _isDangerMode
            ? _buildDangerUI()
            : const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                   Icon(Icons.shield, size: 80, color: Colors.green),
                   SizedBox(height: 20),
                   Text("Monitoring your movement...", style: TextStyle(fontSize: 18)),
                   Text("(Stop moving for 30s to test)", style: TextStyle(color: Colors.grey)),
                ],
              ),
      ),
    );
  }

  Widget _buildDangerUI() {
    return Container(
      color: Colors.red.shade50,
      padding: const EdgeInsets.all(20),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.warning_amber_rounded, size: 100, color: Colors.red),
          const SizedBox(height: 20),
          const Text(
            "ARE YOU OKAY?",
            style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold, color: Colors.red),
          ),
          const SizedBox(height: 10),
          const Text(
            "We detected no movement for a while. Sending SOS in 30 seconds...",
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 40),
          ElevatedButton(
            onPressed: _markSafe,
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green,
              padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 20),
            ),
            child: const Text("I AM SAFE", style: TextStyle(fontSize: 20, color: Colors.white)),
          ),
        ],
      ),
    );
  }
}
