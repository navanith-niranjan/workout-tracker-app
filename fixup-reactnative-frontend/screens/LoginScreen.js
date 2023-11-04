import React, { useState } from 'react';
import { View, Text, TextInput, ScrollView, StyleSheet, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
import AuthService from '../services/AuthService';
import { useNavigation } from '@react-navigation/native';
import CustomButton from '../components/CustomButtonForLandingPage';
import { StatusBar } from 'expo-status-bar';
import CustomBackButton from '../components/CustomBackButton';

const LoginScreen = () => {
  const navigation = useNavigation();
  const [error, setError] = useState('');

  const [emailOrUsername, setEmailorUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    if (!emailOrUsername || !password) {
      console.log('Please fill in all fields');
      return;
    }

    const loginResult = await AuthService.login(emailOrUsername, password);

    if (loginResult.success) {
      navigation.navigate('Main');
    } 
    else {
      if (loginResult.error === 'Account is not verified') {
        if (!emailOrUsername.includes('@')) {
          const emailfromUsername = await AuthService.get_email(emailOrUsername);
          navigation.navigate('OTPVerify', { email: emailfromUsername, password: password});
        }
        else {
          navigation.navigate('OTPVerify', { email: emailOrUsername, password: password});
        }
      } 
      else {
        setError(loginResult.error);
      }
    }
  };

  const handleForgotPassword = () => {
    navigation.navigate('ForgotPassword');
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
      <CustomBackButton iconStyle={{position: 'absolute', right: 140, bottom: 160}}/>
        <StatusBar barStyle="dark-content" />
        <Text style={styles.title}>Log in</Text>
        <Text style={styles.subtitle}>Welcome back!</Text>
        <View style={styles.inputContent}>
          <TextInput
            style={styles.input}
            keyboardType='email-address'
            placeholder="Username or Email"
            onChangeText={(text) => setEmailorUsername(text)}
            value={emailOrUsername}
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
        </View>
        <CustomButton title="Login" onPress={handleLogin} />
        <TouchableOpacity onPress={handleForgotPassword}>
          <Text style={styles.forgotPasswordLink}>Forgot Password?</Text>
        </TouchableOpacity>
        {error ? (<Text style={styles.error}>{error}</Text>) : null}
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
    marginBottom: 10,
    fontFamily: 'Montserrat',
  },
  subtitle: {
    fontSize: 14,
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
  forgotPasswordLink: {
    color: 'blue', 
    textDecorationLine: 'underline', 
    marginTop: 10, 
    fontFamily: 'Montserrat',
  },
  error: {
    color: 'red',
    fontSize: 14,
    marginTop: 10, 
  },
});

export default LoginScreen;
