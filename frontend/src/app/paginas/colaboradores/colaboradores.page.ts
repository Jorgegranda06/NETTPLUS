import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { CrudPage } from '../crud/crud.page';
@Component({standalone:true,imports:[CommonModule,FormsModule,IonicModule],templateUrl:'../crud/crud.page.html'})
export class ColaboradoresPage extends CrudPage {}