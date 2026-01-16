import 'package:flutter/material.dart';
import 'package:frontend/utils/app_theme.dart';

class FillerWordsScreen extends StatefulWidget {
  const FillerWordsScreen({Key? key}) : super(key: key);

  @override
  State<FillerWordsScreen> createState() => _FillerWordsScreenState();
}

class _FillerWordsScreenState extends State<FillerWordsScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('filler words screen')),
      body: const Center(child: Text('Screen Implementation')),
    );
  }
}
