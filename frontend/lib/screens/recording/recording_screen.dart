import 'package:flutter/material.dart';
import 'package:frontend/utils/app_theme.dart';

class RecordingScreen extends StatefulWidget {
  const RecordingScreen({Key? key}) : super(key: key);

  @override
  State<RecordingScreen> createState() => _RecordingScreenState();
}

class _RecordingScreenState extends State<RecordingScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.primaryColor,
      body: Center(
        child: Text(
          'Recording Screen - Implement circular timer UI here',
          style: TextStyle(color: Colors.white),
        ),
      ),
    );
  }
}
