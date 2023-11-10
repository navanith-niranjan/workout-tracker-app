import React, { useState } from 'react';
import { View, Text, StyleSheet, Alert } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import CustomButton from '../components/CustomButtonForLandingPage'; 
import AuthService from '../services/AuthService';
import { useNavigation } from '@react-navigation/native';

const ProfileScreen = () => {
  const navigation = useNavigation();

  const handleSignOut = async () => {
    const signoutResult = await AuthService.logout();
    if (signoutResult.success) {
      navigation.navigate('Landing');
    } else {
      Alert.alert('Error', 'Failed to sign out. Please try again.');
    }
  };

  // const handleDeleteAccount = async () => {
  //   const deleteResult = await AuthService.deleteAccount();
  //   if (deleteResult.success) {
  //     navigation.navigate('Landing');
  //   } else {
  //     Alert.alert('Error', 'Failed to delete your account. Please try again.');
  //   }
  // };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <CustomButton title="Sign Out" onPress={handleSignOut} />
      {/* <CustomButton title="Delete Account" onPress={handleDeleteAccount}/> */}
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

export default ProfileScreen;
