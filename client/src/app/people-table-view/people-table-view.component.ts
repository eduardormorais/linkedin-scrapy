import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-people-table-view',
  templateUrl: './people-table-view.component.html',
  styleUrls: ['./people-table-view.component.css']
})
export class PeopleTableViewComponent implements OnInit {

  pessoas = []

  constructor() { }

  ngOnInit(): void {

    this.pessoas = [
      {name: "Amy Elsner", email: 'amyelsner@gmail.com', image: 'amyelsner.png'},
      {name: "Anna Fali", email: 'annafali@gmail.com', image: 'annafali.png'},
      {name: "Asiya Javayant", email: 'asiyajavayant@gmail.com', image: 'asiyajavayant.png'},
      {name: "Bernardo Dominic", email: 'bernardodominic@gmail.com', image: 'bernardodominic.png'},
      {name: "Elwin Sharvill", email: 'elwinsharvill@gmail.com', image: 'elwinsharvill.png'},
      {name: "Ioni Bowcher", email: 'ionibowcher@gmail.com', image: 'ionibowcher.png'},
      {name: "Ivan Magalhaes", email: 'ivanmagalhaes@gmail.com',image: 'ivanmagalhaes.png'},
      {name: "Onyama Limba", email: 'onyamalimba@gmail.com', image: 'onyamalimba.png'},
      {name: "Stephen Shaw", email: 'stephenshaw@gmail.com', image: 'stephenshaw.png'},
      {name: "XuXue Feng", email: 'xuxuefeng@gmail.com', image: 'xuxuefeng.png'}
    ];

  }

}
