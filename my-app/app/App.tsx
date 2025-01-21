import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Index from './index';
import Tutorial from './Tutorial'; // Make sure to create this screen component

// Define your navigation structure
export type RootStackParamList = {
  Index: undefined;
  Tutorial: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Index">
        <Stack.Screen name="Index" component={Index} />
        <Stack.Screen name="Tutorial" component={Tutorial} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
