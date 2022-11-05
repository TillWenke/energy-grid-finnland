import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DistributionComponent } from './distribution/distribution.component';

const routes: Routes = [
  {path: 'distribution', component: DistributionComponent},
  {path: '', redirectTo: '/', pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
