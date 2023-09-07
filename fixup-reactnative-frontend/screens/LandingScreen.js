import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import CustomButton from '../components/CustomButtonForLandingPage';
import { useNavigation } from '@react-navigation/native';
import useCustomFonts from '../components/CustomFonts';

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
    <View style={styles.container}>
      <Text style={styles.title}>FixUp</Text>
      <Text style={styles.subtitle}>Workout Tracker Powered By GPT-3</Text>
      <CustomButton title="Sign Up" onPress={handleSignUp} />
      <CustomButton title="Sign In" onPress={handleSignIn} />
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
    fontFamily: 'Montserrat',
    fontSize: 24,
    marginBottom: 20,
  },
  subtitle: {
    fontFamily: 'Montserrat',
    fontSize: 18,
    marginBottom: 20,
  },
});

export default LandingScreen;