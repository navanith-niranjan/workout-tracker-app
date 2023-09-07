import { useFonts, Montserrat_400Regular } from '@expo-google-fonts/montserrat';

export default function useCustomFonts() {
  const [fontsLoaded, fontError] = useFonts({
    Montserrat: Montserrat_400Regular,
  });

  return { fontsLoaded, fontError };
}