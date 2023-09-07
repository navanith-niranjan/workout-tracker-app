import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity } from 'react-native';
import AuthService from '../services/AuthService';
import { useNavigation } from '@react-navigation/native';

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
      navigation.navigate('Home');
    } 
    else {
      setError('Incorrect credentials. Please try again.');
    }
  };

  const handleForgotPassword = () => {
    navigation.navigate('ForgotPassword');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>
      <TextInput
        style={styles.input}
        placeholder="Username or Email"
        onChangeText={(text) => setEmailorUsername(text)}
        value={emailOrUsername}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        onChangeText={(text) => setPassword(text)}
        value={password}
      />
      <Button title="Login" onPress={handleLogin} />
      <TouchableOpacity onPress={handleForgotPassword}>
        <Text style={styles.forgotPasswordLink}>Forgot Password?</Text>
      </TouchableOpacity>
      {error ? (<Text style={styles.error}>{error}</Text>) : null}
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
  input: {
    width: '80%',
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingLeft: 10,
  },
  forgotPasswordLink: {
    color: 'blue', 
    textDecorationLine: 'underline', 
    marginTop: 10, 
  },
  error: {
    color: 'red',
    fontSize: 14,
    marginTop: 10, 
  },
});

export default LoginScreen;
