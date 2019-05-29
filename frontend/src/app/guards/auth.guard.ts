import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';
import { AccountService } from '../services/account.service';
import { Injectable } from '@angular/core';
import * as appRoutes from '../constants/routes';

@Injectable()
export class AuthGuard implements CanActivate {
    constructor(private accountService: AccountService, private router: Router) {
    }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        if (this.accountService.isLoggedIn()) {
            return true;
        } else {
            this.router.navigate([appRoutes.LOGIN], {queryParams: {returnUrl: state.url}});
            return false;
        }
    }
}
