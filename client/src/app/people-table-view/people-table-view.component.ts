import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-people-table-view',
  templateUrl: './people-table-view.component.html',
  styleUrls: ['./people-table-view.component.scss']
})
export class PeopleTableViewComponent implements OnInit {

  pessoas = []

  constructor() { }

  ngOnInit(): void {

    this.pessoas = [
      {name: "Amy Elsner",cargo:'Analista de Requisitos' , email: 'amyelsner@gmail.com', image: 'amyelsner.png', localidade: 'Brasilia - DF' },
      {name: "Anna Fali",cargo:'Gerênte de Projetos', email: 'annafali@gmail.com', image: 'annafali.png', localidade: 'Brasilia - DF'},
      {name: "Asiya Javayant",cargo:'Programador', email: 'asiyajavayant@gmail.com', image: 'asiyajavayant.png', localidade: 'Brasilia - DF'},
      {name: "Bernardo Dominic",cargo:'Gerênte de Projetos', email: 'bernardodominic@gmail.com', image: 'bernardodominic.png', localidade: 'Brasilia - DF'},
      {name: "Elwin Sharvill",cargo:'Analista de Requisitos', email: 'elwinsharvill@gmail.com', image: 'elwinsharvill.png', localidade: 'Brasilia - DF'},
      {name: "Ioni Bowcher",cargo:'Programador', email: 'ionibowcher@gmail.com', image: 'ionibowcher.png', localidade: 'Brasilia - DF'},
      {name: "Ivan Magalhaes",cargo:'Gerênte de Projetos', email: 'ivanmagalhaes@gmail.com',image: 'ivanmagalhaes.png', localidade: 'Brasilia - DF'},
      {name: "Onyama Limba",cargo:'Programador', email: 'onyamalimba@gmail.com', image: 'onyamalimba.png', localidade: 'Brasilia - DF'},
      {name: "Stephen Shaw",cargo:'Programador', email: 'stephenshaw@gmail.com', image: 'stephenshaw.png', localidade: 'Brasilia - DF'},
      {name: "XuXue Feng",cargo:'Analista de Requisitos', email: 'xuxuefeng@gmail.com', image: 'xuxuefeng.png', localidade: 'Brasilia - DF'}
    ];

  }

}
