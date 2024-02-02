import {View, Text, TextInput, Button} from "react-native";
import React, {useState} from "react";
import {UserFromApi, UserRegister} from "@/app/_schemas";
import {useAuth} from "@/context/AuthContext";
import {StyleSheet} from "react-native";
import {Link, Stack} from "expo-router";
import DateTimePickerModal from 'react-native-modal-datetime-picker';

const Register = () => {
    const [userData, setUserData] = useState<UserRegister>({})
    const {onRegister} = useAuth()
    const [isDatePickerVisible, setDatePickerVisibility] = useState(false);
    const [birthdate, setBirthdate] = useState(''); // Add this line

    const register = async () => {
        try {
            await onRegister(userData);
            alert('User registered successfully')
            history.goBack()
        }
        catch (error) {
            alert('Error registering user', error.message)
        }
    }

    return (

        <View style={styles.container}>
            <View style={styles.form}>
                <TextInput style={styles.input} placeholder="Email" onChangeText={(text: string) => setUserData({...userData, email:text})} autoCapitalize={"none"}></TextInput>
                <TextInput style={styles.input} placeholder="Password" secureTextEntry={true} onChangeText={(text: string) => setUserData({...userData, password:text})} autoCapitalize={"none"}></TextInput>
                <TextInput style={styles.input} placeholder="Username" onChangeText={(text: string) => setUserData({...userData, username:text})} autoCapitalize={"none"}></TextInput>
                <TextInput style={styles.input} placeholder="Full Name" onChangeText={(text: string) => setUserData({...userData, fullname:text})} autoCapitalize={"none"}></TextInput>
                {/*<Button title="Show date picker" onPress={ () => {setDatePickerVisibility(true)}} />*/}
                <TextInput style={styles.input} placeholder={"Birthdate"} value={birthdate} onFocus={ () => {setDatePickerVisibility(true)}}></TextInput>
                <DateTimePickerModal
                    isVisible={isDatePickerVisible}
                    mode="date"
                    onConfirm = {(date) => {
                        setUserData({...userData, birthdate: date.toISOString().split('T')[0]})
                        setBirthdate(date.toISOString().split('T')[0]);
                        setDatePickerVisibility(false)
                    }}
                    onCancel={() => {
                        setDatePickerVisibility(false)
                    }}
                />
                <Button title={"Register"} onPress={register}></Button>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    form: {
        gap: 10,
        width: "60%"
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
    }
});

export default Register;