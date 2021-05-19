/**
   The Luncho app.

  @author HIRANO Satoshi
  @date  2021/05/12

*/
import { autoinject, TaskQueue } from 'aurelia-framework';
import { Router, RouterConfiguration } from 'aurelia-router'
import { PLATFORM } from 'aurelia-pal';
import { Luncho } from 'luncho_typescript-aurelia/luncho';
import * as browserLocale from 'browser-locale';
import * as countryData from 'country-data';

@autoinject
export class App {
    public title: string = 'Luncho';
    public router: Router;
    public static app: App;
    show = false;
    public taskQueue: TaskQueue;
    luncho: Luncho;
    countryData = countryData
    continents = {
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'EU': 'Europe',
        'OC': 'Australia',
        'AF': 'Africa',
    }


    constructor(taskQueue: TaskQueue, router: Router, luncho: Luncho) {
        this.taskQueue = taskQueue;
        this.luncho = luncho;
        this.luncho.basePath = 'http://localhost:8000'
        App.app = this;
        this.router = router;
    }

    toggleSideNav() {
        this.show = !this.show;
    }

    configureRouter(config: RouterConfiguration, router: Router) {
        this.router = router;
        config.title = this.title;

        //config.addPipelineStep('authorize', AuthorizeStep); // add login
        config.map([
            { route: ['', 'single'], href: '/single', name: '#/single',
              moduleId: PLATFORM.moduleName('./single'),
              auth: true, nav: true, title: 'One country', },
            { route: 'countries', href: '/countries', name: '#/countries',
              moduleId: PLATFORM.moduleName('./countries'),
              auth: true, nav: true, title: 'All countries', },
            { route: 'about', href: 'about', name: 'about',
              moduleId: PLATFORM.moduleName('./about'),
              auth: true, nav: false, title: 'About', },

        ]);

        config.fallbackRoute('/');
    }
}
