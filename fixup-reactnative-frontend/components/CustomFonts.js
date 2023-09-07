import { useFonts, Montserrat_400Regular, Montserrat_600SemiBold } from '@expo-google-fonts/montserrat';

export default function useCustomFonts() {
  const [fontsLoaded, fontError] = useFonts({
    Montserrat: Montserrat_400Regular,
    'Montserrat-SemiBold': Montserrat_600SemiBold,
  });

  return { fontsLoaded, fontError };
}