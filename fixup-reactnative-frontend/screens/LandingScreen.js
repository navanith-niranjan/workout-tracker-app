import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import CustomButton from '../components/CustomButtonForLandingPage';
import { useNavigation } from '@react-navigation/native';
import useCustomFonts from '../components/CustomFonts';
import { StatusBar } from 'expo-status-bar';

const LandingScreen = () => {

  const navigation = useNavigation();

  const { fontsLoaded, fontError } = useCustomFonts();

  if (!fontsLoaded && !fontError) {
    return null; 
  }

  const handleSignUp = () => {
    navigation.navigate('SignUp');
  };

  const handleSignIn = () => {
    navigation.navigate('SignIn'); 
  };

  return (
      <View style={styles.content}>
        <StatusBar barStyle="dark-content" />
        <Text style={styles.title}>FIXUP</Text>
        <Text style={styles.subtitle}>Workout Tracker Powered By GPT-3 AI</Text>
        <View style={styles.buttonContainer}>
          <CustomButton title="Sign in" onPress={handleSignIn} />
          <CustomButton title="Get started" onPress={handleSignUp} />
        </View>
      </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonContainer: {
    position: 'absolute',
    alignItems: 'center',
    width: '100%',
    bottom: 100,
  },
  title: {
    fontFamily: 'Montserrat',
    fontSize: 24,
    marginBottom: 10,
  },
  subtitle: {
    fontFamily: 'Montserrat',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 16,
    marginBottom: 20,
  },
});

export default LandingScreen;