import {observable, makeAutoObservable, action} from "mobx"

export default class UserStore {
    @observable
    public username: string

    constructor(username: string='Not Login!') {
        this.username = username;
        makeAutoObservable(this)
    }

    @action
    changeName= (name:string)=>{
        this.username = name
    }
}