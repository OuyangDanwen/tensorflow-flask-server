import { Injectable } from '@angular/core';
import { Headers, Http, Response, RequestOptions } from '@angular/http';
import 'rxjs/Rx';
import { Observable } from 'rxjs/Observable';
import { Router } from '@angular/router';
@Injectable()

export class LoginService {
  constructor(private http: Http, private router: Router) { }

  logIn(username: string, password: string, location: [number, number]) {
    const req = { 'username': username, 'password': password, 'location': location };
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });

    return this.http.post('http://54.93.252.106:8080/api/login',
      req, options)
      .map(
      (response: Response) => {
        const data = response.json();
        this.router.navigate(['dashboard']);
        return data;
      },
    )
      .catch(
      (error: Response) => {
        const data = error.json();
        console.log(data);
        return Observable.throw(error.status);
      },
    );
  }

  register(name: string, username: string, password: string, location: [number, number]) {
    const req = { 'name': name, 'username': username, 'password': password, 'location': location };
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });

    return this.http.post('http://54.93.252.106:8080/api/register',
      req, options)
      .map(
      (response: Response) => {
        const data = response.json();
        this.router.navigate(['dashboard']);
        return data;
      },
    )
      .catch(
      (error: Response) => {
        const data = error.json();
        console.log(data);
        return Observable.throw(error.status);
      },
    );
  }

  logOut() {
    const token = localStorage.getItem('access_token');
    const headers = new Headers();
    headers.append('Authorization', 'Bearer ' + token);
    return this.http.get('http://54.93.252.106:8080/api/logout', { headers: headers })
      .map(
      (response: Response) => {
        const data = response.json();
        localStorage.removeItem('access_token');
        this.router.navigate(['login']);
        return data;
      }
      )
      .catch(
      (error: Response) => {
        return Observable.throw('Failed@\n/api/logout');
      }
      );
  }
}
