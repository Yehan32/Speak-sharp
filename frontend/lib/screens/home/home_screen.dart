import 'package:flutter/material.dart';
import 'package:frontend/utils/app_theme.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(25),
              color: Colors.white,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Good morning,',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: AppTheme.textTertiary,
                    ),
                  ),
                  const SizedBox(height: 5),
                  Text(
                    'John Doe 👋',
                    style: Theme.of(context).textTheme.displaySmall,
                  ),
                ],
              ),
            ),
            
            // Content
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(20),
                child: Column(
                  children: [
                    // Big Action Button
                    InkWell(
                      onTap: () {
                        Navigator.of(context).pushNamed('/recording');
                      },
                      child: Container(
                        padding: const EdgeInsets.all(30),
                        decoration: BoxDecoration(
                          gradient: AppTheme.primaryGradient,
                          borderRadius: BorderRadius.circular(25),
                          boxShadow: [
                            BoxShadow(
                              color: AppTheme.accentColor.withValues(alpha: 0.3),
                              blurRadius: 40,
                              offset: const Offset(0, 10),
                            ),
                          ],
                        ),
                        child: Column(
                          children: [
                            Container(
                              width: 60,
                              height: 60,
                              decoration: BoxDecoration(
                                color: Colors.white.withValues(alpha: 0.2),
                                borderRadius: BorderRadius.circular(30),
                              ),
                              child: const Icon(
                                Icons.mic,
                                color: Colors.white,
                                size: 28,
                              ),
                            ),
                            const SizedBox(height: 15),
                            const Text(
                              'Start Recording',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.w700,
                                color: Colors.white,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Begin a new speech session',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.white.withValues(alpha: 0.8),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    
                    const SizedBox(height: 25),
                    
                    // Metrics Row
                    Row(
                      children: [
                        Expanded(
                          child: _buildMetricCard('24', 'Speeches'),
                        ),
                        const SizedBox(width: 15),
                        Expanded(
                          child: _buildMetricCard('8.2', 'Avg Score'),
                        ),
                      ],
                    ),
                    
                    const SizedBox(height: 25),
                    
                    // Section Title
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'RECENT ACTIVITY',
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          fontWeight: FontWeight.w700,
                          letterSpacing: 1,
                        ),
                      ),
                    ),
                    
                    const SizedBox(height: 15),
                    
                    // Speech Cards
                    _buildSpeechCard(
                      'Public Speaking Tips',
                      '2 days ago • 5 min',
                      '8.5',
                    ),
                    _buildSpeechCard(
                      'Ice Breaker Speech',
                      '5 days ago • 4 min',
                      '7.8',
                    ),
                  ],
                ),
              ),
            ),
            
            // Bottom Navigation
            Container(
              decoration: BoxDecoration(
                color: Colors.white,
                border: Border(
                  top: BorderSide(color: Colors.grey[200]!),
                ),
              ),
              padding: const EdgeInsets.only(
                left: 20,
                right: 20,
                top: 15,
                bottom: 25,
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildNavItem(Icons.home, 'Home', 0),
                  _buildNavItem(Icons.history, 'History', 1),
                  _buildNavItem(Icons.person, 'Profile', 2),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildMetricCard(String value, String label) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: AppTheme.cardShadow,
      ),
      child: Column(
        children: [
          Text(
            value,
            style: const TextStyle(
              fontSize: 32,
              fontWeight: FontWeight.w800,
              color: AppTheme.accentColor,
            ),
          ),
          const SizedBox(height: 5),
          Text(
            label.toUpperCase(),
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
              letterSpacing: 0.5,
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildSpeechCard(String title, String meta, String score) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: AppTheme.cardShadow,
      ),
      child: Row(
        children: [
          Container(
            width: 50,
            height: 50,
            decoration: BoxDecoration(
              gradient: AppTheme.warningGradient,
              borderRadius: BorderRadius.circular(15),
            ),
            child: const Icon(
              Icons.mic,
              color: Colors.white,
              size: 24,
            ),
          ),
          const SizedBox(width: 15),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w700,
                    color: AppTheme.textPrimary,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  meta,
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
          ),
          Text(
            score,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w800,
              color: AppTheme.accentColor,
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildNavItem(IconData icon, String label, int index) {
    final bool isActive = _selectedIndex == index;
    return InkWell(
      onTap: () {
        setState(() => _selectedIndex = index);
        if (index == 1) {
          Navigator.of(context).pushNamed('/history');
        } else if (index == 2) {
          Navigator.of(context).pushNamed('/profile');
        }
      },
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            color: isActive ? AppTheme.accentColor : AppTheme.textTertiary,
            size: 24,
          ),
          const SizedBox(height: 6),
          Text(
            label,
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w600,
              color: isActive ? AppTheme.accentColor : AppTheme.textTertiary,
            ),
          ),
        ],
      ),
    );
  }
}
