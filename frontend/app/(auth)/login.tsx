import {View, Text, TextInput, TouchableOpacity} from "react-native";
import React, {useState} from "react";
import {useAuth} from "@/context/AuthContext";
import {StyleSheet} from "react-native";
import {Link} from "expo-router";

const Login = () => {
    const [email, setEmail] = useState<string>('')
    const [password, setPassword] = useState<string>('')
    const {onLogin} = useAuth()
    const login = async () => {
        try {
            await onLogin(email, password);
        }
        catch (error) {
            //@ts-ignore
            console.log(error.response)
            alert('Error login user')
        }
    }

    return (
        <View style={styles.container}>
            <View style={styles.titleContainer}>
                <Text style={styles.title}>HUCHNO</Text>
            </View>
            <View style={styles.formContainer}>
                <View style={styles.form}>
                    <TextInput style={styles.input} placeholder="Email" onChangeText={(text: string) => setEmail(text)}
                               autoCapitalize={"none"}></TextInput>
                    <TextInput style={styles.input} placeholder="Password" secureTextEntry={true}
                               onChangeText={(text: string) => setPassword(text)} autoCapitalize={"none"}></TextInput>
                    <TouchableOpacity style={styles.button} onPress={login} >
                        <Text style={styles.buttonTitle}>Login</Text>
                    </TouchableOpacity>
                    <Link style={styles.link} href={"/(auth)/register"}><Text>Register</Text></Link>
                </View>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#fff",
    },
    form: {
        width: "80%",
        padding: 20,
        borderRadius: 10,
        backgroundColor: "#fff",
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 2,
        },
        justifyContent: "center",
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
    },
    formContainer: {
        width: "100%",
        alignItems: "center",
        flex: 3,
    },
    title: {
        fontSize: 48,
        fontWeight: "bold",
        marginBottom: 20,
        color: "#FFC107",
    },
    titleContainer: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
    },
    input: {
        height: 40,
        borderWidth: 1,
        borderRadius: 4,
        padding: 10,
        marginBottom: 10,
        backgroundColor: "#fff"
    },
    link: {
        alignSelf: "center",
        marginTop: 20,
        color: "black",
    },
    button: {
        backgroundColor: "#FEDB71",
        padding: 10,
        borderRadius: 10,
        alignItems: "center",
        justifyContent: "center",
        marginTop: 10,
    },
    buttonTitle: {
        color: "black",
    }
});

export default Login;