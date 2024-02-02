import {View, Text, TextInput, Button} from "react-native";
import React, {useState} from "react";
import {UserFromApi} from "@/app/_schemas";
import {useAuth} from "@/context/AuthContext";
import {StyleSheet} from "react-native";
import {Link, Stack} from "expo-router";

const Login = () => {
    const [email, setEmail] = useState<string>('')
    const [password, setPassword] = useState<string>('')
    const {onLogin} = useAuth()
    const login = async () => {
        const response = await onLogin!(email, password);
        console.log("response")
        console.log(response)
        if (response && response.error) {
            alert(response.message)
        }
    }

    return (

        <View style={styles.container}>
            <View style={styles.form}>
                <TextInput style={styles.input} placeholder="Email" onChangeText={(text: string) => setEmail(text)} autoCapitalize={"none"}></TextInput>
                <TextInput style={styles.input} placeholder="Password" secureTextEntry={true} onChangeText={(text: string) => setPassword(text)} autoCapitalize={"none"}></TextInput>
                <Button title={"Login"} onPress={login}></Button>
                <Link style={styles.link} href={"/(auth)/register"}><Text>Register</Text></Link>
            </View>
        </View>
  );
};

const styles = StyleSheet.create({
    form: {
        gap: 10,
        width: "60%",
    },

    input: {
        height: 40,
        borderWidth: 1,
        borderRadius: 4,
        padding: 10,
        backgroundColor: "#fff"
    },

    container: {
        marginTop: 100,
        alignItems: "center",
        width: "100%",
    },

    link: {
        alignSelf: "center",
    }
});

export default Login;