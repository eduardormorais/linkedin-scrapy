import {PeopleTableViewService} from './people-table-view.service';
import { switchMap,takeWhile } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';
import { interval, from } from 'rxjs';
import {Pesquisa} from './pesquisa.model'
import {Pessoa} from './pessoa.model'
import {Setor} from './setor.model'

@Component({
  selector: 'app-people-table-view',
  templateUrl: './people-table-view.component.html',
  styleUrls: ['./people-table-view.component.scss']
})
export class PeopleTableViewComponent implements OnInit {

  pessoas:[]
  pesquisa = new Pesquisa
  resultPesquisa:Pessoa[]
  setores:Setor[]
  atualizar:boolean
  qtdpessoas=0
  progress:number
  constructor(private peopleTableService: PeopleTableViewService  ) { }

  ngOnInit(): void {

    //  this.pessoas = [
    //    {email_status:"Catch-All", primeiroNome: "Anna Fali",cargo:'Gerênte de Projetos', email: 'annafali@gmail.com', image: 'annafali.png', localidade: 'Brasilia - DF'},
    //    {email_status:"Valid", primeiroNome: "Asiya Javayant",cargo:'Programador', email: 'asiyajavayant@gmail.com', image: 'asiyajavayant.png', localidade: 'Brasilia - DF'},
    //    {email_status:"Invalid", primeiroNome: "Bernardo Dominic",cargo:'Gerênte de Projetos', email: 'bernardodominic@gmail.com', image: 'bernardodominic.png', localidade: 'Brasilia - DF'},
    //    {email_status:"Invalid", primeiroNome: "Elwin Sharvill",cargo:'Analista de Requisitos', email: 'elwinsharvill@gmail.com', image: 'elwinsharvill.png', localidade: 'Brasilia - DF'},
    //    {email_status:"Invalid", primeiroNome: "Ioni Bowcher",cargo:'Programador', email: 'ionibowcher@gmail.com', image: 'ionibowcher.png', localidade: 'Brasilia - DF'},
    //    {email_status:"Valid", primeiroNome: "Ivan Magalhaes",cargo:'Gerênte de Projetos', email: 'ivanmagalhaes@gmail.commmmmmmmmmmmm',image: 'ivanmagalhaes.png', localidade: 'Brasilia - DF'},
    //    {email_status:"Valid", primeiroNome: "Onyama Limba",cargo:'Programador', email: 'onyamalimba@gmail.com', image: 'onyamalimba.png', localidade: 'Brasilia - DF'},
    //    {email_status:"Valid", primeiroNome: "Stephen Shaw",cargo:'Programador', email: 'stephenshaw@gmail.com', image: 'stephenshaw.png', localidade: 'Brasilia - DF'},
    //    {email_status:"Catch-All", primeiroNome: "XuXue Feng",cargo:'Analista de Requisitos', email: 'xuxuefeng@gmail.com', image: 'xuxuefeng.png', localidade: 'Brasilia - DF'}
    //  ];

    this.peopleTableService.getSetores().subscribe((resp:Setor[]) => {this.setores = resp; console.log(this.setores)})
  }

  pesquisar(){
    if(!this.atualizar === true){
      this.qtdpessoas = 0
      this.progress = 0
      console.log(this.pesquisa)
      let file
      this.peopleTableService.searching(this.pesquisa).subscribe( resp => {
        console.log(resp)
        file = resp
      })

      interval(5000).pipe(
      switchMap(() => from(this.peopleTableService.getResultSearching(file))),
      takeWhile(((response: any ) => {
          this.atualizar = false
          if(response ===0 ){
            this.atualizar=true
          }else if(response.length < this.pesquisa.qtd){
            this.pessoas = response
            this.qtdpessoas = this.pessoas.length

            this.progress = (this.qtdpessoas * 100)/this.pesquisa.qtd

            this.atualizar=true
          }else{
            this.pessoas = response
            console.log(this.pessoas)
          }
          return this.atualizar
        }))
      ).subscribe( (response:any) => {console.log("Resp -> ", response)})
    }
  }
}
