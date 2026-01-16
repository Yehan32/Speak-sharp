import 'package:flutter/material.dart';
import 'package:frontend/utils/app_theme.dart';

class FeedbackScreen extends StatefulWidget {
  const FeedbackScreen({Key? key}) : super(key: key);

  @override
  State<FeedbackScreen> createState() => _FeedbackScreenState();
}

class _FeedbackScreenState extends State<FeedbackScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('feedback screen')),
      body: const Center(child: Text('Screen Implementation')),
    );
  }
}
