type UserFromApi = {
    id: string;
    username: string;
    email: string;
    fullname: string;
    birthdate: Date;
    is_active: boolean;
    last_login: Date;
    registration_date: Date;
    verified: boolean;
};

type UserRegister = {
    username: string;
    email: string;
    password: string;
    fullname: string;
    birthdate: Date;
}

export type { UserFromApi, UserRegister };