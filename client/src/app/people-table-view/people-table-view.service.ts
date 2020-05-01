import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http'
import {Pesquisa} from './pesquisa.model'
import { Setor } from './setor.model';

@Injectable({
  providedIn: 'root'
})
export class PeopleTableViewService {

  constructor(private http: HttpClient) {
  }

  searching(pesquisa:Pesquisa){
    let formData: FormData = new FormData();
    formData.append('localidade', pesquisa.localidade)
    formData.append('cargo', pesquisa.cargo)
    formData.append('qtd', pesquisa.qtd.toString())
    for(let setor of pesquisa.setores){
      formData.append('setores', setor.nome)
    }
    return this.http.post('/api/pesquisa/', formData)
  }

  getSetores(){
    return this.http.get('/api/setores/')
  }

  getResultSearching(file){
    return this.http.get(`/api/resultado/?fileName=${file}`)
  }

}
