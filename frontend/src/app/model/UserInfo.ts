import {UserSettings} from './UserSettings';

export class UserInfo {
    public id: number;
    public email: string;
    public firstName: string;
    public lastName: string;
    public role: string;
    public settings: UserSettings;

    constructor(id: number, email: string, firstName: string, lastName: string, role: string, settings: UserSettings) {
        this.id = id;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.role = role;
        this.settings = settings;
    }
}
