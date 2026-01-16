import 'package:flutter/material.dart';
import 'package:frontend/utils/app_theme.dart';

class PlaybackScreen extends StatefulWidget {
  const PlaybackScreen({Key? key}) : super(key: key);

  @override
  State<PlaybackScreen> createState() => _PlaybackScreenState();
}

class _PlaybackScreenState extends State<PlaybackScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Playback')),
      body: Center(
        child: Text('Playback Screen'),
      ),
    );
  }
}
