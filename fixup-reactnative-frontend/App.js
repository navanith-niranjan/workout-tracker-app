import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import useCustomFonts from './components/CustomFonts';
import AuthNavigator from './navigation/AuthNavigator';
import AuthService from './services/AuthService';
import AsyncStorage from '@react-native-async-storage/async-storage';
import store from './redux/store';
import { Provider, useSelector } from 'react-redux';
import { setAuthState } from './redux/authReducer';

export default function App () {
  return (
    <Provider store={store}> 
      <AppContent />
    </Provider>
  );
}

function AppContent() {
  const authState = useSelector((state) => state.auth);
  const [key, setKey] = useState(0);

  useEffect(() => {
    checkToken();
  }, [])

  const checkToken = async () => {
    try {
      const token = await AsyncStorage.getItem('authToken');
      
      console.log('Stored Token:', token);
      
      if (token) {
        const isTokenValid = await AuthService.verifyToken(token);

        console.log('Is Token Valid:', isTokenValid);
    
        if (isTokenValid) {
          store.dispatch(setAuthState({ isAuthenticated: true }));
        } else {
          store.dispatch(setAuthState({ isAuthenticated: false }));
        }
      } else {
        store.dispatch(setAuthState({ isAuthenticated: false }));
      }

      setKey(prevKey => prevKey + 1);

    } catch (error) {
      console.error('Error checking token:', error);
    }
  };

  return (
      <NavigationContainer>
        <AuthNavigator key={key} initialRoute={authState.isAuthenticated ? 'Main' : 'Landing'}/>
      </NavigationContainer>
  );
}