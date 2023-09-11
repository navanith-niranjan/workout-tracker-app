import React, { useState } from 'react';
import { View, Text, TextInput, ScrollView, StyleSheet, KeyboardAvoidingView } from 'react-native';
import AuthService from '../services/AuthService';
import { useNavigation } from '@react-navigation/native';
import CustomButton from '../components/CustomButtonForLandingPage';
import { StatusBar } from 'expo-status-bar';
import CustomBackButton from '../components/CustomBackButton';

const RegistrationScreen = () => {
  const navigation = useNavigation();
  const [error, setError] = useState('');

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSignup = async () => {
    if (!username || !email || !password || !confirmPassword) {
      setError('Please fill in all required fields');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const signupResult = await AuthService.signup(
        username,
        email,
        password,
        confirmPassword,
        firstName,
        lastName
      );

      if (signupResult.success) {
        navigation.navigate('OTPVerify', { email: email, password: password });
      } else {
          setError(signupResult.error || 'Signup failed. Please try again.');
      }
    } catch (error) {
        setError('An error occurred during signup. Please try again later.');
        console.error(error); 
    }
  };

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      enabled
    >
      <ScrollView
      contentContainerStyle={styles.container}
      keyboardDismissMode="on-drag"
      >
      <CustomBackButton iconStyle={{position: 'absolute', right: 140, bottom: 60}}/>
        <StatusBar barStyle="dark-content" />
        <Text style={styles.title}>Create an account</Text>
        <View style={styles.inputContent}>
          <TextInput
            style={styles.input}
            placeholder="First Name"
            onChangeText={(text) => setFirstName(text)}
            value={firstName}
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Last Name"
            onChangeText={(text) => setLastName(text)}
            value={lastName}
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Username"
            onChangeText={(text) => setUsername(text)}
            value={username}
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Email"
            onChangeText={(text) => setEmail(text)}
            value={email}
            keyboardType='email-address'
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Password"
            secureTextEntry
            onChangeText={(text) => setPassword(text)}
            value={password}
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Confirm Password"
            secureTextEntry
            onChangeText={(text) => setConfirmPassword(text)}
            value={confirmPassword}
            autoCapitalize="none"
          />
          </View>
        <CustomButton title="Sign Up" onPress={handleSignup} />
        {error ? <Text style={styles.error}>{error}</Text> : null}
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    marginTop: 70,
  },
  title: {
    fontSize: 24,
    marginBottom: 40,
    fontFamily: 'Montserrat',
  },
  inputContent: {
    width: '80%',
    marginBottom: 40,
  },
  input: {
    height: 50,
    backgroundColor: 'white',
    borderColor: 'white',
    borderBottomColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingLeft: 10,
  },
  error: {
    color: 'red',
    fontSize: 14,
    marginTop: 10,
  },
});

export default RegistrationScreen;


