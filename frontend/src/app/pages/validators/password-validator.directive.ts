import { AbstractControl, ValidatorFn } from '@angular/forms';

export function passwordValidator(): ValidatorFn {
    return (control: AbstractControl): { [key: string]: any } => {
        if (control.parent) {
            return control.parent.value.password !== control.value ? { 'passwordValidator': { value: control.value } } : null;
        } else {
            return null;
        }
    };
}
