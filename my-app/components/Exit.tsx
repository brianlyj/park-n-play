import React from 'react';
import { View, Text, StyleSheet, Pressable} from 'react-native';
import { PressableLink } from './PressableLink';

export interface ExitProps {
  linkTarget: string; // Target screen for the PressableLink
}

export function Exit({linkTarget }: ExitProps) {
    return (
      <View style={styles.lessonContainer}>
        <PressableLink 
          target={linkTarget} 
          iconName="close-circle" 
          iconSize={24} 
          iconColor='white' 
        />
      </View>
    );
  }
const styles = StyleSheet.create({
  lessonContainer: {
    position: 'absolute', // Absolute positioning
    top: 30, // Adjust vertical placement
    right: 20, // Align to the right of the container
  },
});
