import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { AntDesign } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native'; 

const StartWorkoutButton = () => {
    return (
      <TouchableOpacity style={styles.button}>
        <AntDesign name="plus" size={24} color="white" />
      </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    button: {
        width: 60,
        height: 60,
        backgroundColor: 'black',
        borderRadius: 30,
        justifyContent: 'center',
        alignItems: 'center',
        position: 'absolute',
        bottom: 20,
        right: 20,
    },
});

export default StartWorkoutButton;
