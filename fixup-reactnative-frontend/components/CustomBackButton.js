import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { AntDesign } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native'; 

const BackButton = ({iconStyle}) => {
  const navigation = useNavigation(); 

  const handleGoBack = () => {
    navigation.goBack(); 
  };

  return (
    <TouchableOpacity onPress={handleGoBack}>
      <AntDesign name="leftcircle" size={40} color="black" style={iconStyle}/>
    </TouchableOpacity>
  );
};

export default BackButton;
