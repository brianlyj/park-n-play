import React, { useState } from 'react';
import { View, Text, StyleSheet, Dimensions, Pressable } from 'react-native';
import { Exit } from '@/components/Exit';

// Get screen dimensions
const { width } = Dimensions.get('window');

export default function ParkRight() {
  const [isExpanded, setIsExpanded] = useState(true); // Track expanded state

  return (
    <View style={styles.root}>
      <Pressable
        style={[styles.rectangle1, isExpanded ? styles.expanded : styles.collapsed]} // Adjust styles dynamically
        onPress={() => setIsExpanded(!isExpanded)} // Toggle expanded state on press
      >
        <Text style={styles.letsGetStarted}>{`Park Right II`}</Text>
        {isExpanded && (
          <Text style={styles.welcomeText}>
            {`Be a considerate rider!\n\nPark your bicycle responsibly at a designated location so others can easily access and enjoy the service.`}
          </Text>
        )}
      </Pressable>
      <Exit linkTarget="Tutorial" />
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
    backgroundColor: 'rgba(171, 220, 32, 1)', // Green background
  },
  expanded: {
    height: 225, // Expanded height
  },
  collapsed: {
    height: 80, // Collapsed height to show only title and icon
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
