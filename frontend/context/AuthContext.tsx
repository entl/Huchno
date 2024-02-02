import {createContext, useContext, useEffect, useState} from "react";
import {useRouter, useSegments} from "expo-router";
import axios from "axios";
import {API_HOST} from "@env";
import {UserRegister} from "@/app/_schemas";

const AuthContext = createContext<any>(null);

const TOKEN_KEY = "my-jwt";

export function useAuth() {
    return useContext(AuthContext);
}


export function AuthProvider({children}: any) {
    const rootSegment = useSegments()[0];
    const router = useRouter();
    const [access_token, setAccessToken] = useState<string | undefined>("");

    useEffect(() => {
        // const loadToken = async () => {
        //     const token = await SecureStore.getItemAsync("my-jwt");
        //     if (token) {
        //         setAccessToken(token)
        //     }
        // }
        // loadToken();
        if (access_token === undefined) return;

        if (!access_token && rootSegment !== "(auth)") {
            router.replace("/(auth)/login");
        } else if (access_token && rootSegment !== "(app)") {
            router.replace("/");

        }

    }, [access_token, rootSegment]);

    const login = async (email: string, password: string) => {
        let bodyFormData = new FormData();
        bodyFormData.append("username", email)
        bodyFormData.append("password", password)
        const result = await axios({
            method: "POST",
            url: `${API_HOST}/auth/login`,
            data: bodyFormData,
            headers: {"Content-type": "multipart/form-data"}
        });

        // await SecureStore.setItemAsync(TOKEN_KEY, result.data.access_token);

        setAccessToken(result.data.access_token);
        return result;
    }

    const logout = async() => {
        setAccessToken("")
    }

    const register = async(user_data: UserRegister) => {
            return await axios({
                method: "POST",
                url: `${API_HOST}/users/`,
                data: user_data,
                headers: {"Content-type": "application/json"}
            });
    }

    const value = {
        onLogin: login,
        onLogout: logout,
        onRegister: register,
        access_token: access_token
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}