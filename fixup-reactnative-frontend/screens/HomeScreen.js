import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import MainService from '../services/MainService';
import StartWorkoutButton from '../components/StartWorkoutButton';
import { useSelector } from 'react-redux';

const HomeScreen = () => {
  const currentHour = new Date().getHours();

  let greeting = 'Good Morning';

  if (currentHour >= 12 && currentHour < 16) {
    greeting = 'Good Afternoon';
  } else if (currentHour >= 16) {
    greeting = 'Good Evening';
  }

  const user = useSelector((state) => state.user.user);

  useEffect(() => {
    async function fetchUserInfo() {
      try {
        await MainService.getUserInfo();
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    }

    fetchUserInfo();
  }, []);

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <Text style={styles.title}>{greeting}, {user?.first_name || ""}</Text>
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
    },
});

export default HomeScreen;
