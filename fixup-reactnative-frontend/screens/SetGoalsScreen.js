import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { setUser } from '../redux/userReducer';

const SetGoalsScreen = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.user);

  const [step, setStep] = useState(0);
  const [ft, setFt] = useState('0');
  const [inches, setInches] = useState('0');
  const [cm, setCm] = useState('0');
  const [weight, setWeight] = useState('0');
  const [selectedSex, setSelectedSex] = useState(null);
  const [selectedUnitHeight, setSelectedUnitHeight] = useState('ft');
  const [selectedUnitWeight, setSelectedUnitWeight] = useState('kg');
  const [inputValue, setInputValue] = useState('');

  const goToNextStep = () => {
    const value =
      step === 2
        ? selectedUnitHeight === 'ft'
          ? `${ft}'${inches}"`
          : `${cm} cm`
        : step === 3
        ? `${weight} ${selectedUnitWeight}`
        : inputValue.trim();

    dispatch(setUser({ ...user, [getStepKey(step)]: value }));
    setStep((prevStep) => prevStep + 1);
  };

  const goToPreviousStep = () => {
    setStep((prevStep) => (prevStep > 0 ? prevStep - 1 : 0));
  };

  const getStepKey = (step) => {
    const stepKeys = ['age', 'sex', 'height', 'weight', 'goals'];
    return stepKeys[step];
  };

  const renderInput = () => {
    switch (step) {
      case 0:
        return (
          <TextInput
            style={styles.input}
            placeholder="Enter Age"
            keyboardType="numeric"
            value={inputValue}
            onChangeText={(text) => setInputValue(text)}
          />
        );
      case 1:
        return (
          <View style={styles.sexContainer}>
            <TouchableOpacity
              style={[styles.sexButton, selectedSex === 'Male' && styles.selectedSex]}
              onPress={() => setSelectedSex('Male')}
            >
              <Text>Male</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.sexButton, selectedSex === 'Female' && styles.selectedSex]}
              onPress={() => setSelectedSex('Female')}
            >
              <Text>Female</Text>
            </TouchableOpacity>
          </View>
        );
      case 2:
        return (
          <View style={styles.heightContainer}>
            <TouchableOpacity
              style={[
                styles.unitButton,
                selectedUnitHeight === 'ft' && styles.selectedUnit,
              ]}
              onPress={() => setSelectedUnitHeight('ft')}
            >
              <Text>ft</Text>
            </TouchableOpacity>
            {selectedUnitHeight === 'ft' && (
              <>
                <TextInput
                  style={styles.input}
                  placeholder="ft"
                  keyboardType="numeric"
                  value={ft}
                  onChangeText={(text) => setFt(text)}
                />
                <TextInput
                  style={styles.input}
                  placeholder="inches"
                  keyboardType="numeric"
                  value={inches}
                  onChangeText={(text) => setInches(text)}
                />
              </>
            )}
            {selectedUnitHeight === 'cm' && (
              <TextInput
                style={styles.input}
                placeholder="cm"
                keyboardType="numeric"
                value={cm}
                onChangeText={(text) => setCm(text)}
              />
            )}
          </View>
        );
      case 3:
        return (
          <View style={styles.weightContainer}>
            <TouchableOpacity
              style={[
                styles.unitButton,
                selectedUnitWeight === 'kg' && styles.selectedUnit,
              ]}
              onPress={() => setSelectedUnitWeight('kg')}
            >
              <Text>kg</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.unitButton,
                selectedUnitWeight === 'lbs' && styles.selectedUnit,
              ]}
              onPress={() => setSelectedUnitWeight('lbs')}
            >
              <Text>lbs</Text>
            </TouchableOpacity>
            <TextInput
              style={styles.input}
              placeholder={selectedUnitWeight === 'kg' ? 'Weight in kg' : 'Weight in lbs'}
              keyboardType="numeric"
              value={weight}
              onChangeText={(text) => setWeight(text)}
            />
          </View>
        );
      case 4:
        return (
          <TextInput
            style={styles.input}
            placeholder="Enter Goals"
            value={inputValue}
            onChangeText={(text) => setInputValue(text)}
          />
        );
      default:
        return null;
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Set Goals: {getStepKey(step).toUpperCase()}</Text>
      {renderInput()}
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={goToPreviousStep} disabled={step === 0}>
          <Text>Back</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={goToNextStep}>
          <Text>Next</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center', 
      paddingHorizontal: 20,
    },
    title: {
      fontSize: 18,
      marginBottom: 20,
    },
    buttonContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      width: '100%',
      marginTop: 20,
    },
    button: {
      padding: 10,
      backgroundColor: '#ADD8E6',
      borderRadius: 5,
    },
    input: {
      height: 40,
      borderColor: 'gray',
      borderWidth: 1,
      marginBottom: 20,
      width: '100%',
      paddingHorizontal: 10,
    },
    sexContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      width: '100%',
    },
    sexButton: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      paddingVertical: 10,
      marginHorizontal: 5,
      backgroundColor: '#ADD8E6',
      borderRadius: 5,
    },
    selectedSex: {
      backgroundColor: 'lightblue',
    },
    heightContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      width: '100%',
    },
    unitButton: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      paddingVertical: 10,
      marginHorizontal: 5,
      backgroundColor: '#ADD8E6',
      borderRadius: 5,
    },
    selectedUnit: {
      backgroundColor: 'lightblue',
    },
    weightContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      width: '100%',
    },
});

export default SetGoalsScreen;
