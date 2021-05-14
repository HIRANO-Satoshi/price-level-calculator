import { autoinject, TaskQueue } from 'aurelia-framework';
import { Router, RouterConfiguration } from 'aurelia-router'
import { PLATFORM } from 'aurelia-pal';
import { LunchoFast } from 'luncho-typescript-aurelia-fast/luncho-fast';
//import { LunchoApi } from './gen-openapi';
// import { HttpClient } from 'aurelia-fetch-client';
import 'tablesorter';
import 'tablesorter/dist/css/theme.materialize.min.css';
// import { Luncho, LunchoResult} from './luncho';

@autoinject
export class App {
    public title: string = 'Luncho';
    public router: Router;
    public static app: App;
    show = false;
    countries: any;
    // luncho: Luncho;
    public taskQueue: TaskQueue;
    lunchoFast: LunchoFast;


    constructor(taskQueue: TaskQueue, router: Router, lunchoFast: LunchoFast) {
        this.taskQueue = taskQueue;
        this.lunchoFast = lunchoFast;
        this.lunchoFast.basePath = 'http://localhost:8000'
        // this.luncho = new Luncho(taskQueue);
        App.app = this;
        this.router = router;
    }

    activate() {
        this.lunchoFast.countries()
            .then((countries) => {
                this.countries = countries;
        });
    }

    // attached() {
    //     this.countryCode = 'JPN';
    //     //super.attached();
    // }


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
