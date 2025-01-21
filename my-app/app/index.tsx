import React, { useEffect } from 'react';
import { View, Text, Dimensions, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';

// Define your navigation type
type RootStackParamList = {
  Index: undefined;
  Tutorial: undefined;
};

const { width, height } = Dimensions.get('window');

export default function Index() {
  // Specify the correct navigation type
  const navigation = useNavigation<StackNavigationProp<RootStackParamList, 'Index'>>();

  useEffect(() => {
    const timeout = setTimeout(() => {
      navigation.replace('Tutorial'); // Now 'replace' will work correctly
    }, 3000); // Delay in milliseconds

    return () => clearTimeout(timeout); // Cleanup timeout on component unmount
  }, [navigation]);
  
  return (
    <View style={styles.container}>
      <View style={styles.contents}>
        <View style={styles.contentArea}>
          <View style={styles.titleContainer}>
            <Text style={styles.title}>anywheel</Text>
          </View>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  titleContainer: {
    flex: 1, // Take up remaining space to center the title vertically
    justifyContent: 'center', // Center title vertically
    alignItems: 'center', // Center title horizontally
  },
  title: {
    fontSize: 42, // Adjust size as needed
    fontWeight: 'bold',
    fontFamily: 'SFProDisplay', // Custom font name
    color: '#FFFFFF', // Text color
  },
  contents: {
    width: width,
    height: height,
    flexDirection: 'column',
    alignItems: 'center',
    backgroundColor: '#ABDC20', // Replace with your desired color
  },
  contentArea: {
    flexGrow: 1,
    flexShrink: 0,
    flexBasis: 0,
    alignSelf: 'stretch',
  },
});
