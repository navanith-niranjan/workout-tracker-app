import React, {useState, useEffect} from 'react';
import { NavigationContainer, useNavigation } from '@react-navigation/native';
import useCustomFonts from './components/CustomFonts';
import AuthNavigator from './navigation/AuthNavigator';
import AuthService from './services/AuthService';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function App () {
  const [initialRoute, setInitialRoute] = useState("Landing"); // Should change this into a loading screen since every time app boots up, it goes to this page intially
  const [key, setKey] = useState(0);

  useEffect(() => {
    checkToken();
  }, [])

  const checkToken = async () => {
    try {
      const token = await AsyncStorage.getItem('authToken');
      
      if (token) {
        const isTokenValid = await AuthService.verifyToken(token);
        console.log('Is Token Valid:', isTokenValid);
        if (isTokenValid) {
          setInitialRoute("Home");
        } else {
          setInitialRoute("Landing");
        }
      } else {
        setInitialRoute("Landing");
      }

      setKey(prevKey => prevKey + 1);

    } catch (error) {
      console.error('Error checking token:', error);
    }
  };

  return (
    <NavigationContainer>
      <AuthNavigator key={key} initialRoute={initialRoute}/>
    </NavigationContainer>
  );
}