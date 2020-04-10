import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PeopleTableViewComponent } from './people-table-view/people-table-view.component';
import {TableModule} from 'primeng/table';


@NgModule({
  declarations: [
    AppComponent,
    PeopleTableViewComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    TableModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
