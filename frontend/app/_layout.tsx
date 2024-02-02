import {AuthProvider, useAuth} from '@/context/AuthContext';
import {Link, Slot, SplashScreen, Stack} from "expo-router";
import {DarkTheme, DefaultTheme, ThemeProvider} from "@react-navigation/native";
import {useColorScheme} from "react-native";

const RootLayout = () => {
    const colorScheme = useColorScheme();

    return (
        <AuthProvider>
            <Slot></Slot>
        </AuthProvider>
    )
}

export default RootLayout;