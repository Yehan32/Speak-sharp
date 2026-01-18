import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:provider/provider.dart';
import 'package:frontend/providers/auth_provider.dart';
import 'package:frontend/providers/speech_provider.dart';
import 'package:frontend/utils/app_theme.dart';
import 'package:frontend/screens/splash_screen.dart';
import 'package:frontend/screens/onboarding/welcome_screen.dart';
import 'package:frontend/screens/onboarding/features_screen.dart';
import 'package:frontend/screens/onboarding/ready_screen.dart';
import 'package:frontend/screens/onboarding/tutorial_screen.dart';
import 'package:frontend/screens/onboarding/startup_config_screen.dart';
import 'package:frontend/screens/auth/login_screen.dart';
import 'package:frontend/screens/auth/register_screen.dart';
import 'package:frontend/screens/home/home_screen.dart';
import 'package:frontend/screens/recording/speech_details_dialog.dart';
import 'package:frontend/screens/recording/recording_screen.dart';
import 'package:frontend/screens/recording/playback_screen.dart';
import 'package:frontend/screens/analysis/feedback_screen.dart';
import 'package:frontend/screens/analysis/filler_words_screen.dart';
import 'package:frontend/screens/analysis/advanced_analysis_screen.dart';
import 'package:frontend/screens/history/history_screen.dart';
import 'package:frontend/screens/history/search_screen.dart';
import 'package:frontend/screens/profile/profile_screen.dart';
import 'package:frontend/screens/profile/progress_dashboard_screen.dart';
import 'package:frontend/screens/settings/settings_screen.dart';
import 'package:frontend/screens/settings/notification_center_screen.dart';
import 'package:frontend/screens/settings/payment_screen.dart';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => SpeechProvider()),
      ],
      child: MaterialApp(
        title: 'Speak Sharp',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        initialRoute: '/splash',
        routes: {
          '/splash': (context) => const SplashScreen(),
          '/onboarding/welcome': (context) => const WelcomeScreen(),
          '/onboarding/features': (context) => const FeaturesScreen(),
          '/onboarding/ready': (context) => const ReadyScreen(),
          '/onboarding/tutorial': (context) => const TutorialScreen(),
          '/onboarding/startup': (context) => const StartupConfigScreen(),
          '/auth/login': (context) => const LoginScreen(),
          '/auth/register': (context) => const RegisterScreen(),
          '/home': (context) => const HomeScreen(),
          '/recording': (context) => const RecordingScreen(),
          '/playback': (context) => const PlaybackScreen(),
          '/feedback': (context) => const FeedbackScreen(),
          '/filler-words': (context) => const FillerWordsScreen(),
          '/advanced-analysis': (context) => const AdvancedAnalysisScreen(),
          '/history': (context) => const HistoryScreen(),
          '/search': (context) => const SearchScreen(),
          '/profile': (context) => const ProfileScreen(),
          '/progress': (context) => const ProgressDashboardScreen(),
          '/settings': (context) => const SettingsScreen(),
          '/notifications': (context) => const NotificationCenterScreen(),
          '/payment': (context) => const PaymentScreen(),
        },
      ),
    );
  }
}
