
export function slowImport(value:any, ms = 1000){
    return new Promise(resolve=>{
        setTimeout(()=> resolve(value),ms);
    })
}