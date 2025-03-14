import React, { useState } from 'react';
import { View, StyleSheet, Dimensions, Image, Text, Alert, Pressable } from 'react-native';
import { WebView } from 'react-native-webview';
import { Exit } from '@/components/Exit';

const { width, height } = Dimensions.get('window');

export default function ParkRight() {
    const [isExpanded, setIsExpanded] = useState(true); // Track expanded state
    // Function to handle button press
    const handlePress = () => {
      Alert.alert("Proceed to play game on laptop", "You can now start the game on your laptop.", [
        { text: "OK", onPress: () => console.log("OK Pressed") },
      ]);
    };

  
  return (
    <View style={styles.container}>
      <Image
        source={require('./gamepic.png')} // Path to your image
        style={styles.image} // Apply styles to scale the image
        resizeMode="cover" // Scale image to cover the entire screen
      />
      <WebView
        source={{ uri: 'http://192.168.79.20:5000/video_feed' }} // Update IP address if needed
        style={styles.webview}
        javaScriptEnabled={true}
        domStorageEnabled={true}
      />
      {/* ParkRight Section */}
      <Pressable
        style={[styles.rectangle1, isExpanded ? styles.expanded : styles.collapsed]} // Adjust styles dynamically
        onPress={() => setIsExpanded(!isExpanded)} // Toggle expanded state on press
      >
        <Text style={styles.letsGetStarted}>{`Park Right`}</Text>
        {isExpanded && (
          <Text style={styles.welcomeText}>
            {`Share the road responsibly!\nPlay the fun strategy game and master the art of efficient bicycle parking to optimise parking space.`}
          </Text>
        )}
      </Pressable>
      <Exit linkTarget="Tutorial" />
      {/* Button */}
      <Pressable style={styles.button} onPress={handlePress}></Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  webview: {
    width: width,
    height: height,
  },
  rectangle1: {
    width: width, // Responsive width
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
    fontSize: 19,
    fontWeight: '400',
    lineHeight: 28, // Adjusted for better readability
    textAlign: 'center', // Center align text
  },
  image: {
    width: width, // Match screen width
    height: height, // Match screen height
  },
  button: {
    position: 'absolute',
    bottom: 100, // Position the button at the bottom
    alignSelf: 'center', // Center the button horizontally
    backgroundColor: 'rgba(0, 255, 255, 0)', // White with 20% opacity
    paddingVertical: 75,
    paddingHorizontal: 120,
    borderRadius: 10,
  },
});
