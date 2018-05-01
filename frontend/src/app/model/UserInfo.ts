export class UserInfo {
    public id: number;
    public email: string;
    public firstName: string;
    public lastName: string;
    public role: string;
    public skipTutorial: boolean;

    constructor(id: number, email: string, firstName: string, lastName: string, role: string, skipTutorial: boolean) {
        this.id = id;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.role = role;
        this.skipTutorial = skipTutorial;
    }
}
