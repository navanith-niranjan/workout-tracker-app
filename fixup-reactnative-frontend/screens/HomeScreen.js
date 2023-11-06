import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import MainService from '../services/MainService';
import StartWorkoutButton from '../components/StartWorkoutButton';

const HomeScreen = () => {
  const currentHour = new Date().getHours();

  let greeting = 'Good Morning';

  if (currentHour >= 12 && currentHour < 16) {
    greeting = 'Good Afternoon';
  } else if (currentHour >= 16) {
    greeting = 'Good Evening';
  }

  const [userFirstName, setUserFirstName] = useState('');

  useEffect(() => {
    const fetchUserFirstName = async () => {
      try {
        const userInfo = await MainService.getUserInfo();
        setUserFirstName(userInfo.first_name);
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    };

    fetchUserFirstName();
  }, []);

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <Text style={styles.title}>{greeting}, {userFirstName}</Text>
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
