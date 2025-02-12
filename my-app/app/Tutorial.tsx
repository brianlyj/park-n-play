import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import {Lesson} from '@/components/Lesson';

// Get screen dimensions
const { width } = Dimensions.get('window');

export default function Tutorial() {
  return (
    <View style={styles.root}>
      <View style={styles.rectangle1}></View>
      <Text style={styles.letsGetStarted}>
        {`Let’s Get Started!`}
      </Text>
      <Text
        style={
          styles.welcomeText
        }
      >
        {`Welcome to the Anywheel Tutorial\n\nBe familiar with the basic knowledge to have an enjoyable ride!`}
      </Text>
      <View style={styles.lessonList}>
        <Lesson title="Park Right" duration="2 mins" linkTarget='Park'/>
        <Lesson title="Park Master" duration="1 min" linkTarget='Park2'/>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    width: '100%', // Match parent container width
    height: 225,
    position: 'relative',
    alignItems: 'center', // Center horizontally
  },
  rectangle1: {
    width: '100%', // Responsive width
    height: 225,
    position: 'absolute',
    top: 0,
    backgroundColor: 'rgba(171, 220, 32, 1)', // Green background
  },
  letsGetStarted: {
    marginTop: 20,
    color: 'rgba(245, 245, 245, 1)', // White color
    fontFamily: 'SF Pro Display',
    fontSize: 36,
    fontWeight: '700',
    lineHeight: 42, // Adjusted for better spacing
    textAlign: 'center', // Center align text
  },
  welcomeText: {
    marginTop: 10,
    paddingHorizontal: 20,
    color: 'rgba(245, 245, 245, 1)', // White color
    fontFamily: 'SF Pro Display',
    fontSize: 19,
    fontWeight: '400',
    lineHeight: 28, // Adjusted for better readability
    textAlign: 'center', // Center align text
  },
  lessonList: {
    flex: 1,
    marginTop: 50,
    padding: 16, // Add padding to the container
  },
});
