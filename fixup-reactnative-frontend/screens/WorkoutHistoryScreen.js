import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import StartWorkoutButton from '../components/StartWorkoutButton';

const WorkoutHistoryScreen = () => {

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <StartWorkoutButton />
    </View>
  );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    title: {
        fontSize: 24,
        marginBottom: 20,
    },
});

export default WorkoutHistoryScreen;
