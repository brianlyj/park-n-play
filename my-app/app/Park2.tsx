import React, { useState, useEffect } from 'react';
import { View, Text, Button, Image, StyleSheet, Dimensions, Pressable } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';
import { Exit } from '@/components/Exit';

// Get screen dimensions
const { width } = Dimensions.get('window');

export default function App() {
  const [isExpanded, setIsExpanded] = useState(true); // Track expanded state
  const [image, setImage] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);

  // Request camera permissions
  useEffect(() => {
    (async () => {
      const { status } = await ImagePicker.requestCameraPermissionsAsync();
      if (status !== 'granted') {
        alert('Sorry, we need camera permissions to make this work!');
      }
    })();
  }, []);

  const pickImage = async () => {
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images, // Specify only images
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    console.log(result);

    if (!result.canceled) {
      setImage(result.assets[0].uri); // Update state with the captured image URI
    }
  };

  const uploadImage = async () => {
    if (!image) {
      alert('Please take a picture first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', {
      uri: image,
      type: 'image/jpeg', // Adjust if the image type differs
      name: 'image.jpg',
    });

    try {
      const response = await axios.post(
        'http://192.168.79.20:5000/predict', // Replace with your Flask API URL
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setPrediction(response.data.predicted_label);
    } catch (error) {
      console.error('Error uploading image:', error);
      alert('Error uploading image');
    }
  };

  return (
    <View style={styles.container}>
      {/* ParkRight Section */}
      <Pressable
        style={[styles.rectangle1, isExpanded ? styles.expanded : styles.collapsed]} // Adjust styles dynamically
        onPress={() => setIsExpanded(!isExpanded)} // Toggle expanded state on press
      >
        <Text style={styles.letsGetStarted}>{`Park Master`}</Text>
        {isExpanded && (
          <Text style={styles.welcomeText}>
            {`Be a considerate rider!\nPark your bicycle responsibly at a designated location so others can easily access and enjoy the service.`}
          </Text>
        )}
      </Pressable>
      <Exit linkTarget="Tutorial" />

      {/* Image Picker Section - Outside of rectangle1 */}
      <View style={styles.imageSection}>
        <Pressable style={styles.button} onPress={pickImage}>
          <Text style={styles.buttonText}>Take a Picture</Text>
        </Pressable>
        {image && <Image source={{ uri: image }} style={styles.image} />}
        <Pressable style={styles.button} onPress={uploadImage}>
          <Text style={styles.buttonText}>Upload and Predict</Text>
        </Pressable>
        {prediction && <Text style={styles.prediction}>Prediction: {prediction}</Text>}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
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
  imageSection: {
    marginTop: 250,
    alignItems: 'center',
    justifyContent: 'center',
    
  },
  image: {
    width: 200,
    height: 200,
    marginVertical: 20,
  },
  prediction: {
    fontSize: 24,
    color: 'black',
    marginTop: 20,
  },
  button: {
    backgroundColor: 'rgba(171, 220, 32, 1)', // Green button color
    paddingVertical: 20,
    paddingHorizontal: 40,
    borderRadius: 5,
    marginVertical: 2,
  },
  buttonText: {
    color: 'white', // Text color inside the button
    fontSize: 24,
    fontWeight: '500',
    textAlign: 'center',
  },
});