import {View, Text, TextInput, Button, TouchableOpacity} from "react-native";
import React, {useState} from "react";
import {UserFromApi, UserRegister} from "@/app/_schemas";
import {useAuth} from "@/context/AuthContext";
import {StyleSheet} from "react-native";
import DateTimePickerModal from 'react-native-modal-datetime-picker';

const Register = () => {
    const [userData, setUserData] = useState<UserRegister>({
        birthdate: new Date(),
        email: "",
        fullname: "",
        password: "",
        username: ""
    })
    const {onRegister} = useAuth()
    const [isDatePickerVisible, setDatePickerVisibility] = useState(false);
    const [birthdate, setBirthdate] = useState(''); // Add this line

    const register = async () => {
        try {
            await onRegister(userData);
            alert('User registered successfully')
        }
        catch (error) {
            //@ts-ignore
            console.log(error.response.data)
            //@ts-ignore
            alert(`Error registering user ${error.response}`)
        }
    }

    console.log(userData)

    return (

        <View style={styles.container}>
            <View style={styles.titleContainer}>
                <Text style={styles.title}>HUCHNO</Text>
            </View>
            <View style={styles.formContainer}>
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
                            //@ts-ignore
                            //sets the date of the date picker to the birthdate state, but in the format of YYYY-MM-DD
                            setUserData({...userData, birthdate: date.toISOString().split('T')[0]})
                            setBirthdate(date.toISOString().split('T')[0]);
                            setDatePickerVisibility(false)
                        }}
                        onCancel={() => {
                            setDatePickerVisibility(false)
                        }}
                    />
                    <TouchableOpacity onPress={register} style={styles.button}>
                        <Text style={styles.buttonTitle}>Register</Text>
                    </TouchableOpacity>
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

export default Register;