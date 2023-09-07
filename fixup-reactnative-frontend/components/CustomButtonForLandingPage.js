import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';
import useCustomFonts from '../components/CustomFonts';

const CustomButtonForLandingPage = ({ title, onPress }) => {
  const { fontsLoaded, fontError } = useCustomFonts();

  if (!fontsLoaded && !fontError) {
    return null; 
  }

    return (
      <TouchableOpacity style={styles.button} onPress={onPress}>
        <Text style={styles.buttonText}>{title}</Text>
      </TouchableOpacity>
    );
  };
  
  const styles = StyleSheet.create({
    button: {
      backgroundColor: 'black',
      paddingVertical: 15,
      paddingHorizontal: 20,
      borderRadius: 100,
      marginBottom: 10, 
      width: '80%', 
      alignItems: 'center', 
      justifyContent: 'center', 
    },
    buttonText: {
      color: 'white',
      fontFamily: 'Montserrat',
      fontSize: 16,
    },
  });
  
  export default CustomButtonForLandingPage;
  
  