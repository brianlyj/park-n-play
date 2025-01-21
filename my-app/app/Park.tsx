import React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import { WebView } from 'react-native-webview';

const { width, height } = Dimensions.get('window');

export default function ParkRight() {
  return (
    <View style={styles.container}>
      <WebView
        source={{ uri: 'http://192.168.79.20:5000/video_feed' }} // Update IP address if needed
        style={styles.webview}
        javaScriptEnabled={true}
        domStorageEnabled={true}
      />
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
});
