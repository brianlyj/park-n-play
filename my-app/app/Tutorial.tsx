import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';

// Get screen dimensions
const { width } = Dimensions.get('window');

export default function Tutorial() {
  return (
    <View style={styles.root}>
      <View style={styles.background}></View>
      <View style={styles.rectangle1}></View>
      <Text style={styles.letsGetStarted}>
        {`Let’s Get Started!`}
      </Text>
      <Text
        style={
          styles.welcomeText
        }
        testID="436:297"
      >
        {`Welcome to the Anywheel Tutorial\n\nBe familiar with the basic knowledge to have an enjoyable ride!`}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    width: '100%', // Match parent container width
    height: 293,
    position: 'relative',
    alignItems: 'center', // Center horizontally
  },
  background: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    opacity: 0.1,
    backgroundColor: 'rgba(0, 0, 0, 1)', // Black background with opacity
  },
  rectangle1: {
    width: '100%', // Responsive width
    height: 293,
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
    fontSize: 22,
    fontWeight: '400',
    lineHeight: 28, // Adjusted for better readability
    textAlign: 'center', // Center align text
  },
});
