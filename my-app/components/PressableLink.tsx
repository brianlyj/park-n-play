import React from 'react';
import { Pressable, StyleSheet, ViewStyle } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Ionicons from '@expo/vector-icons/Ionicons';

interface PressableLinkProps {
  target: string; // Screen to navigate to
  iconName: string; // Icon name for Ionicons
  iconSize?: number; // Size of the icon
  iconColor?: string; // Color of the icon
  style?: ViewStyle; // Additional styling for the Pressable container
}

export const PressableLink: React.FC<PressableLinkProps> = ({
  target,
  iconName = "play-circle",
  iconSize = 48,
  iconColor = 'rgba(171, 220, 32, 1)',
  style,
}) => {
  const navigation = useNavigation();

  const handlePress = () => {
    navigation.navigate(target); // Navigate to the specified screen
  };

  return (
    <Pressable style={[styles.pressable, style]} onPress={handlePress}>
      <Ionicons name={iconName} size={iconSize} color={iconColor} />
    </Pressable>
  );
};

const styles = StyleSheet.create({
  pressable: {
    justifyContent: 'center',
    alignItems: 'center',
  },
});
