import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import CustomButton from '../components/CustomButtonForLandingPage';
import { useNavigation } from '@react-navigation/native';
import useCustomFonts from '../components/CustomFonts';
import { LinearGradient } from 'expo-linear-gradient';

const LandingScreen = () => {

  const { fontsLoaded, fontError } = useCustomFonts();

  if (!fontsLoaded && !fontError) {
    return null; 
  }

  const navigation = useNavigation();

  const handleSignUp = () => {
    navigation.navigate('SignUp');
  };

  const handleSignIn = () => {
    navigation.navigate('SignIn'); 
  };

  return (
    <LinearGradient
      colors={['#6800B4', '#36004E']}
      style={styles.container}
    >
      <View style={styles.content}>
        <Text style={styles.title}>FIXUP</Text>
        <Text style={styles.subtitle}>Workout Tracker Powered By GPT-3 AI</Text>
        <View style={styles.buttonContainer}>
          <CustomButton title="Sign in" onPress={handleSignIn} />
          <CustomButton title="Get started" onPress={handleSignUp} />
        </View>
      </View>
    </LinearGradient>
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
    bottom: 40,
  },
  title: {
    fontFamily: 'Montserrat',
    fontSize: 24,
    color: 'white',
    marginBottom: 10,
  },
  subtitle: {
    fontFamily: 'Montserrat',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 16,
    color: 'white',
    marginBottom: 20,
  },
});

export default LandingScreen;