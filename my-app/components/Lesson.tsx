import React from 'react';
import { View, Text, StyleSheet, Pressable} from 'react-native';
import { PressableLink } from './PressableLink';

export interface LessonProps {
  title: string; // Title text
  duration: string; // Duration text
  linkTarget: string; // Target screen for the PressableLink
}

export function Lesson({ title, duration, linkTarget }: LessonProps) {
    return (
      <View style={styles.lessonContainer}>
        <View style={styles.rectangle3} />
        <PressableLink 
          target={linkTarget} 
          iconName="play-circle" 
          iconSize={48} 
          iconColor='rgba(171, 220, 32, 1)' 
          style={styles.playContainer} 
        />
        <Text style={styles.safetyFirst}>
          {title}
        </Text>
        <Text style={styles.timeText}>
          {duration}
        </Text>
      </View>
    );
  }
const styles = StyleSheet.create({
  lessonContainer: {
    width: 350,
    height: 80,
    backgroundColor: 'rgba(255, 255, 255, 1)',
    borderRadius: 15,
    overflow: 'hidden',
    marginBottom: 16, // Add spacing between lessons
  },
  rectangle3: {
    width: '100%',
    height: '100%',
    borderRadius: 15,
    backgroundColor: 'rgba(245, 245, 245, 1)',
    elevation: 4, // Shadow for Android
    shadowColor: 'rgba(0, 0, 0, 0.25)', // Shadow for iOS
    shadowOffset: { width: 0, height: 4 },
    shadowRadius: 4,
  },
  playContainer: {
    position: 'absolute',
    top: 12,
    left: 12,
    width: 55,
    height: 55,
    justifyContent: 'center',
    alignItems: 'center',
  },
  safetyFirst: {
    position: 'absolute',
    top: 20,
    left: 80,
    color: 'rgba(0, 0, 0, 1)',
    fontFamily: 'SF Pro Display',
    fontSize: 22,
    fontWeight: '500',
    lineHeight: 24,
  },
  timeText: {
    position: 'absolute',
    top: 45,
    left: 80,
    color: 'rgba(0, 0, 0, 1)',
    fontFamily: 'SF Pro Display',
    fontSize: 16,
    fontWeight: '500',
    lineHeight: 24,
  },
});
