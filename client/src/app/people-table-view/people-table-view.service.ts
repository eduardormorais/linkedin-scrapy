import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http'
import { Pesquisa } from './pesquisa.model'
import { Setor } from './setor.model';

@Injectable({
  providedIn: 'root'
})
export class PeopleTableViewService {

  constructor(private http: HttpClient) {
  }

  searching(pesquisa: Pesquisa) {
    let formData: FormData = new FormData();

    for (let campo in pesquisa) {
      if (pesquisa[campo] != undefined) {
        if (campo.toString() === "setores") {
          for (let setor of pesquisa.setores) {
            formData.append('setores', setor.nome)
          }
        } else {
          formData.append(campo.toString(), pesquisa[campo])
        }
      }
    }

    return this.http.post('https://linkedinscrapper-backend.herokuapp.com/api/pesquisa/', formData)
  }

  getSetores() {
    return this.http.get('https://linkedinscrapper-backend.herokuapp.com/api/setores/')
  }

  getResultSearching(file) {
    return this.http.get(`https://linkedinscrapper-backend.herokuapp.com/api/resultado/?fileName=${file}`)
  }

}
